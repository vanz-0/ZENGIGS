#!/usr/bin/env python3
"""
Reddit Lead Scraper — via Apify (automation-lab/reddit-scraper)
Uses Apify to bypass Reddit's 403 blocks on the public JSON API.

Usage:
    python execution/reddit_scraper.py
    python execution/reddit_scraper.py --limit 50
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

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN", "")
ACTOR_ID = "automation-lab~reddit-scraper"
APIFY_BASE = "https://api.apify.com/v2"

# Subreddits to search
TARGET_SUBREDDITS = [
    "smallbusiness",
    "entrepreneur",
    "startups",
    "socialmedia",
    "marketing",
    "videography",
    "youtubers",
    "content_marketing",
    "ecommerce",
]

# Search queries
SEARCH_QUERIES = [
    "need more sales calls",
    "website not converting",
    "looking for video editor",
    "need social media manager",
    "cold email help",
    "seo help needed",
    "need a bookkeeper",
    "looking for appointment setter",
]

# Buy-signal keywords for post filtering
BUY_SIGNAL_KEYWORDS = [
    "seo audit", "need seo help", "website redesign", "web design help",
    "bounce rate", "landing page conversion",
    "google ads help", "facebook ads roas", "need social media manager",
    "content creator needed", "need video editor", "tiktok editor",
    "youtube editor", "podcast editor",
    "need more leads", "sales calls", "cold email strategy",
    "email deliverability", "crm setup", "hubspot setup",
    "lead generation agency", "appointment setter",
    "zapier expert", "make.com", "ai chatbot", "customer service bot",
    "bookkeeping help", "virtual assistant needed", "hiring va",
    "need a freelancer", "outsource",
]

OUTPUT_PATH = ".tmp/reddit_leads.json"


# ─── APIFY RUNNER ─────────────────────────────────────────────────────────────

def run_apify_actor(input_data: dict, timeout_secs: int = 120) -> list[dict]:
    """Run an Apify actor synchronously and return the dataset items."""
    if not APIFY_TOKEN:
        print("ERROR: APIFY_API_TOKEN not set in .env")
        return []

    run_url = f"{APIFY_BASE}/acts/{ACTOR_ID}/run-sync-get-dataset-items"
    params = {"token": APIFY_TOKEN, "timeout": timeout_secs, "memory": 256}

    print(f"  Calling Apify actor '{ACTOR_ID}'...")
    try:
        resp = requests.post(run_url, json=input_data, params=params, timeout=timeout_secs + 30)
        if resp.status_code == 201 or resp.status_code == 200:
            return resp.json() if isinstance(resp.json(), list) else []
        else:
            print(f"  Apify returned {resp.status_code}: {resp.text[:300]}")
            return []
    except requests.exceptions.Timeout:
        print("  Apify run timed out.")
        return []
    except Exception as e:
        print(f"  Apify error: {e}")
        return []


# ─── FILTERING & FORMATTING ───────────────────────────────────────────────────

def is_relevant_post(post: dict) -> bool:
    """Check if a post signals someone needs video/content/marketing services."""
    title = (post.get("title") or "").lower()
    text = (post.get("body") or post.get("selftext") or "").lower()
    combined = title + " " + text
    for kw in BUY_SIGNAL_KEYWORDS:
        if kw.lower() in combined:
            return True
    return False


def extract_contact_hints(text: str) -> dict:
    """Extract emails and websites from post text."""
    emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    websites = re.findall(r"https?://(?:www\.)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s]*)?", text)
    websites = [w for w in websites if not any(x in w for x in ["reddit.com", "imgur.com", "i.redd.it"])]
    return {
        "emails_found": ", ".join(set(emails)) if emails else "",
        "websites_found": ", ".join(set(websites[:3])) if websites else "",
    }


def format_post(post: dict) -> dict:
    """Normalize an Apify Reddit post into a clean lead record."""
    raw_text = (post.get("body") or post.get("selftext") or "")
    raw_title = (post.get("title") or "")
    contact = extract_contact_hints(raw_text + " " + raw_title)

    # Apify timestamps may come as ISO strings or unix
    posted_at = ""
    ts = post.get("createdAt") or post.get("created_utc")
    if ts:
        try:
            if isinstance(ts, (int, float)):
                posted_at = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            else:
                posted_at = str(ts)
        except Exception:
            pass

    subreddit = post.get("subreddit") or post.get("communityName") or ""
    permalink = post.get("url") or post.get("permalink") or ""
    if permalink and not permalink.startswith("http"):
        permalink = f"https://reddit.com{permalink}"

    return {
        "source": "reddit",
        "scraped_at": datetime.now().isoformat(),
        "subreddit": subreddit,
        "title": raw_title,
        "body": raw_text[:1000],
        "author": post.get("author") or post.get("username") or "",
        "reddit_url": permalink,
        "score": post.get("score") or post.get("upvotes") or 0,
        "num_comments": post.get("numberOfComments") or post.get("num_comments") or 0,
        "posted_at": posted_at,
        "flair": post.get("flair") or post.get("link_flair_text") or "",
        "emails_found": contact["emails_found"],
        "websites_found": contact["websites_found"],
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
                print("No valid Google credentials. Run create_sheet.py first.")
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
        print(f"Pushed {len(leads)} Reddit leads to 'Reddit Leads' tab.")

    except ImportError:
        print("gspread not installed. Skipping sheet push.")
    except Exception as e:
        print(f"Sheet push failed: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Reddit lead scraper via Apify")
    parser.add_argument("--subreddits", default=",".join(TARGET_SUBREDDITS[:5]),
                        help="Comma-separated subreddits to search")
    parser.add_argument("--queries", default=",".join(SEARCH_QUERIES[:4]),
                        help="Comma-separated search queries")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts per query (default: 25)")
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

    all_posts = {}  # Deduplicate by post URL
    total_fetched = 0

    print(f"\nReddit Lead Scraper via Apify")
    print(f"{len(subreddits)} subreddits x {len(queries)} queries")
    print("=" * 60)

    for subreddit in subreddits:
        for query in queries:
            print(f"\n  r/{subreddit} | '{query}'")

            actor_input = {
                "searchQueries": [query],
                "subreddits": [subreddit],
                "maxPosts": args.limit,
                "sort": "new",
                "time": "month",
            }

            raw_posts = run_apify_actor(actor_input, timeout_secs=90)
            relevant = [p for p in raw_posts if is_relevant_post(p)]

            for p in relevant:
                key = p.get("url") or p.get("id") or p.get("title", "")[:80]
                if key and key not in all_posts:
                    all_posts[key] = format_post(p)
                    total_fetched += 1

            print(f"  Found {len(relevant)} relevant out of {len(raw_posts)} posts")
            time.sleep(1)  # Small pause between actor calls

    leads = list(all_posts.values())
    leads.sort(key=lambda x: x.get("score", 0), reverse=True)

    print(f"\n{'='*60}")
    print(f"Total unique qualified leads: {len(leads)}")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"Saved to {args.output}")

    if leads:
        sample = leads[0]
        print(f"\nTop Lead:")
        print(f"  r/{sample['subreddit']} - {sample['title'][:80]}")
        print(f"  Author: u/{sample['author']} | Score: {sample['score']}")
        print(f"  URL: {sample['reddit_url']}")
        if sample["emails_found"]:
            print(f"  Email found: {sample['emails_found']}")
        if sample["websites_found"]:
            print(f"  Website: {sample['websites_found']}")

    if args.push_to_sheet and leads:
        print(f"\nPushing to Google Sheet...")
        push_to_sheet(leads, args.sheet_url)

    return leads


if __name__ == "__main__":
    main()
