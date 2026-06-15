#!/usr/bin/env python3
"""
Reddit Lead Scraper — Free (No Apify)
Uses Reddit's public JSON API to find business owners posting about needing
video editing, content creation, social media, or automation help.

Usage:
    python execution/reddit_scraper.py
    python execution/reddit_scraper.py --subreddits smallbusiness,entrepreneur --limit 50
    python execution/reddit_scraper.py --push-to-sheet
"""

import os
import sys
import json
import time
import re
import argparse
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────

# Subreddits to search — business owners, entrepreneurs, social media managers
TARGET_SUBREDDITS = [
    "smallbusiness",
    "entrepreneur",
    "startups",
    "socialmedia",
    "marketing",
    "videography",
    "youtubers",
    "content_marketing",
    "Entrepreneur",
    "ecommerce",
]

# Keywords that indicate someone NEEDS our services
BUY_SIGNAL_KEYWORDS = [
    "looking for editor", "need editor", "need a video editor", "hire editor",
    "looking for video", "video editing help", "edit my videos", "editing my content",
    "social media manager", "content creator", "need content", "create content",
    "short form", "short-form", "reels", "tiktok editor", "youtube editor",
    "looking for someone", "hiring", "need help with", "can anyone help",
    "caption", "subtitles", "auto captions", "looking for freelancer",
    "need a freelancer", "outsource", "va needed", "virtual assistant",
    "motion graphics", "intro video", "promo video", "promotional video",
    "ugc", "user generated content", "brand video", "product video",
]

# Subreddit-specific search queries
SEARCH_QUERIES = [
    "need video editor",
    "looking for editor",
    "hire content creator",
    "need social media help",
    "video editing freelancer",
    "need someone to edit",
    "looking for social media manager",
    "UGC creator needed",
    "short form content help",
    "YouTube editor needed",
]

HEADERS = {
    "User-Agent": "ZENGIGS-LeadBot/1.0 (lead generation research; contact maxwellhutter123@gmail.com)",
    "Accept": "application/json",
}

OUTPUT_PATH = ".tmp/reddit_leads.json"


# ─── SCRAPER ──────────────────────────────────────────────────────────────────

def search_reddit(subreddit: str, query: str, limit: int = 25, sort: str = "new") -> list[dict]:
    """Search a subreddit using Reddit's free public JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": query,
        "restrict_sr": "true",  # Only search this subreddit
        "sort": sort,
        "limit": limit,
        "t": "month",  # Posts from last month
    }

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code == 429:
            print(f"  ⚠️  Rate limited on r/{subreddit}. Waiting 30s...")
            time.sleep(30)
            resp = requests.get(url, headers=HEADERS, params=params, timeout=15)

        if resp.status_code != 200:
            print(f"  ✗ r/{subreddit} returned {resp.status_code}")
            return []

        data = resp.json()
        posts = data.get("data", {}).get("children", [])
        return [p["data"] for p in posts if p.get("kind") == "t3"]

    except Exception as e:
        print(f"  ✗ Error fetching r/{subreddit}: {e}")
        return []


def get_hot_posts(subreddit: str, limit: int = 25) -> list[dict]:
    """Get hot/new posts from a subreddit directly."""
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    params = {"limit": limit}

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        posts = data.get("data", {}).get("children", [])
        return [p["data"] for p in posts if p.get("kind") == "t3"]
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return []


def is_relevant_post(post: dict) -> bool:
    """Check if a post signals someone needs video/content services."""
    title = (post.get("title") or "").lower()
    text = (post.get("selftext") or "").lower()
    combined = title + " " + text

    # Must match at least one buy signal keyword
    for kw in BUY_SIGNAL_KEYWORDS:
        if kw.lower() in combined:
            return True
    return False


def extract_contact_hints(post: dict) -> dict:
    """Try to extract any contact info mentioned in the post."""
    text = (post.get("selftext") or "") + " " + (post.get("title") or "")

    # Email pattern
    emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)

    # Website pattern
    websites = re.findall(r"https?://(?:www\.)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s]*)?", text)
    # Filter out reddit/imgur links
    websites = [w for w in websites if not any(x in w for x in ["reddit.com", "imgur.com", "i.redd.it"])]

    return {
        "emails_found": ", ".join(set(emails)) if emails else "",
        "websites_found": ", ".join(set(websites[:3])) if websites else "",
    }


def format_post(post: dict) -> dict:
    """Format a Reddit post into a clean lead record."""
    contact_hints = extract_contact_hints(post)

    # Parse timestamp
    created_utc = post.get("created_utc", 0)
    try:
        posted_at = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        posted_at = ""

    return {
        "source": "reddit",
        "scraped_at": datetime.now().isoformat(),
        "subreddit": post.get("subreddit", ""),
        "title": post.get("title", ""),
        "body": (post.get("selftext") or "")[:1000],  # Truncate long posts
        "author": post.get("author", ""),
        "reddit_url": f"https://reddit.com{post.get('permalink', '')}",
        "score": post.get("score", 0),
        "num_comments": post.get("num_comments", 0),
        "posted_at": posted_at,
        "flair": post.get("link_flair_text", ""),
        "emails_found": contact_hints["emails_found"],
        "websites_found": contact_hints["websites_found"],
        "outreach_sent": "No",
        "notes": "",
    }


# ─── GOOGLE SHEETS PUSH ───────────────────────────────────────────────────────

def push_to_sheet(leads: list[dict], sheet_url: str):
    """Push Reddit leads to a Google Sheet tab."""
    try:
        import gspread
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = None
        if os.path.exists("token.json"):
            with open("token.json", "r") as f:
                token_data = json.load(f)
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open("token.json", "w") as f:
                    f.write(creds.to_json())
            else:
                print("❌ No valid Google credentials. Run create_sheet.py first.")
                return

        client = gspread.authorize(creds)
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        spreadsheet = client.open_by_key(sheet_id)

        try:
            ws = spreadsheet.worksheet("Reddit Leads")
        except gspread.exceptions.WorksheetNotFound:
            ws = spreadsheet.add_worksheet(title="Reddit Leads", rows=1000, cols=20)

        headers = [
            "Subreddit", "Title", "Author", "Reddit URL", "Posted At",
            "Score", "Comments", "Body (Preview)", "Flair",
            "Emails Found", "Websites Found", "Outreach Sent", "Notes"
        ]

        rows = [headers]
        for lead in leads:
            rows.append([
                f"r/{lead['subreddit']}",
                lead["title"],
                f"u/{lead['author']}",
                lead["reddit_url"],
                lead["posted_at"],
                lead["score"],
                lead["num_comments"],
                lead["body"][:300],
                lead["flair"],
                lead["emails_found"],
                lead["websites_found"],
                lead["outreach_sent"],
                lead["notes"],
            ])

        ws.clear()
        ws.update(values=rows, range_name=f"A1:M{len(rows)}")
        ws.format("A1:M1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.1, "green": 0.1, "blue": 0.2},
        })
        print(f"✅ Pushed {len(leads)} Reddit leads to 'Reddit Leads' tab.")

    except ImportError:
        print("⚠️  gspread not installed. Skipping sheet push.")
    except Exception as e:
        print(f"❌ Sheet push failed: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Reddit lead scraper — no Apify needed")
    parser.add_argument("--subreddits", default=",".join(TARGET_SUBREDDITS[:5]),
                        help="Comma-separated subreddits to search")
    parser.add_argument("--queries", default=",".join(SEARCH_QUERIES[:4]),
                        help="Comma-separated search queries")
    parser.add_argument("--limit", type=int, default=25,
                        help="Posts per subreddit per query (default: 25)")
    parser.add_argument("--output", default=OUTPUT_PATH,
                        help="Output JSON file path")
    parser.add_argument("--push-to-sheet", action="store_true",
                        help="Push results to Google Sheet")
    parser.add_argument("--sheet-url",
                        default="https://docs.google.com/spreadsheets/d/1XhyQcGW4IDs5kzH7thoMRpPr_alEkxDEACV1A9KRtVE",
                        help="Google Sheet URL")
    args = parser.parse_args()

    subreddits = [s.strip() for s in args.subreddits.split(",") if s.strip()]
    queries = [q.strip() for q in args.queries.split(",") if q.strip()]

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    all_posts = {}  # Deduplicate by post ID
    total_fetched = 0

    print(f"\n🔍 Reddit Lead Scraper — {len(subreddits)} subreddits × {len(queries)} queries")
    print("=" * 60)

    for subreddit in subreddits:
        print(f"\n📌 r/{subreddit}")
        for query in queries:
            print(f"   Searching: '{query}'...")
            posts = search_reddit(subreddit, query, limit=args.limit)
            relevant = [p for p in posts if is_relevant_post(p)]
            for p in relevant:
                post_id = p.get("id", "")
                if post_id and post_id not in all_posts:
                    all_posts[post_id] = format_post(p)
                    total_fetched += 1

            print(f"   Found {len(relevant)} relevant out of {len(posts)} posts")
            time.sleep(2)  # Respect rate limits

    leads = list(all_posts.values())
    # Sort by score (most upvoted = most active = better signal)
    leads.sort(key=lambda x: x.get("score", 0), reverse=True)

    print(f"\n{'='*60}")
    print(f"✅ Total unique qualified leads: {len(leads)}")

    # Save to JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {args.output}")

    # Print sample
    if leads:
        sample = leads[0]
        print(f"\n📋 Top Lead:")
        print(f"   r/{sample['subreddit']} — {sample['title'][:80]}")
        print(f"   Author: u/{sample['author']} | Score: {sample['score']}")
        print(f"   URL: {sample['reddit_url']}")
        if sample["emails_found"]:
            print(f"   📧 Email found: {sample['emails_found']}")
        if sample["websites_found"]:
            print(f"   🌐 Website: {sample['websites_found']}")

    # Push to sheet if requested
    if args.push_to_sheet and leads:
        print(f"\n📤 Pushing to Google Sheet...")
        push_to_sheet(leads, args.sheet_url)

    return leads


if __name__ == "__main__":
    main()
