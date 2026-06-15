#!/usr/bin/env python3
"""
LinkedIn Lead Scraper — Free (No paid API)
Scrapes LinkedIn public search results using requests + BeautifulSoup
to find decision-makers at companies who post about needing content/video work.

Strategy:
  1. Searches Google for LinkedIn profiles/posts matching our target keywords
  2. Fetches public LinkedIn profile data where available
  3. Exports to JSON + Google Sheets

Usage:
    python execution/linkedin_scraper.py
    python execution/linkedin_scraper.py --niche "social media manager" --location "United States"
    python execution/linkedin_scraper.py --push-to-sheet
"""

import os
import sys
import json
import time
import re
import argparse
import requests
from datetime import datetime
from urllib.parse import urlencode, quote_plus
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────

# Google search queries to find LinkedIn profiles of people/companies needing our services
# This uses Google's site:linkedin.com search — completely free
LINKEDIN_GOOGLE_QUERIES = [
    'site:linkedin.com "video editor" "looking for" -"I am"',
    'site:linkedin.com "content creator" "hiring" "reels OR tiktok OR youtube"',
    'site:linkedin.com "social media manager" "looking to hire" "video"',
    'site:linkedin.com "we are hiring" "video editor" "short form"',
    'site:linkedin.com "need a video editor" OR "looking for video editor"',
    'site:linkedin.com "content production" "freelancer" "video"',
    'site:linkedin.com "UGC" "video" "hiring" OR "looking for"',
    'site:linkedin.com "YouTube channel" "editor" "hiring"',
]

# Company titles to target (decision makers who buy video services)
TARGET_TITLES = [
    "Founder", "CEO", "CMO", "Head of Marketing", "Content Manager",
    "Social Media Director", "Marketing Director", "Brand Manager",
    "Creative Director", "Content Lead", "Digital Marketing Manager",
]

# Industries that need video content
TARGET_INDUSTRIES = [
    "E-commerce", "SaaS", "Media", "Entertainment", "Marketing Agency",
    "Real Estate", "Health & Wellness", "Education", "Hospitality",
    "Retail", "Beauty", "Fashion",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

OUTPUT_PATH = ".tmp/linkedin_leads.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1XhyQcGW4IDs5kzH7thoMRpPr_alEkxDEACV1A9KRtVE"


# ─── GOOGLE SEARCH FOR LINKEDIN PROFILES ─────────────────────────────────────

def google_search_linkedin(query: str, num_results: int = 10) -> list[dict]:
    """
    Uses DuckDuckGo HTML search (free, no API key) to find LinkedIn URLs.
    Falls back to a simple requests scrape if needed.
    """
    results = []

    # DuckDuckGo HTML endpoint — no API key, no rate limit hassles
    search_url = "https://html.duckduckgo.com/html/"
    params = {"q": query, "kl": "us-en"}

    try:
        resp = requests.post(search_url, data=params, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  ✗ Search returned {resp.status_code}")
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")

        for result in soup.select(".result__body")[:num_results]:
            title_el = result.select_one(".result__title")
            snippet_el = result.select_one(".result__snippet")
            url_el = result.select_one(".result__url")

            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            url = url_el.get_text(strip=True) if url_el else ""

            # Only keep LinkedIn results
            if "linkedin.com" not in url.lower() and "linkedin.com" not in title.lower():
                continue

            # Clean URL
            if not url.startswith("http"):
                url = "https://" + url

            results.append({
                "title": title,
                "snippet": snippet,
                "url": url,
            })

    except ImportError:
        print("  ⚠️  BeautifulSoup not installed. Run: pip install beautifulsoup4")
    except Exception as e:
        print(f"  ✗ Search error: {e}")

    return results


def extract_profile_info(result: dict) -> dict:
    """Extract structured info from a LinkedIn search result snippet."""
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    url = result.get("url", "")

    # Try to extract name and title from LinkedIn result format
    # Typical: "John Smith - CEO at ACME Corp | LinkedIn"
    name = ""
    job_title = ""
    company = ""

    # Parse "Name - Title at Company | LinkedIn" pattern
    title_clean = re.sub(r"\s*\|\s*LinkedIn.*$", "", title, flags=re.IGNORECASE)
    if " - " in title_clean:
        parts = title_clean.split(" - ", 1)
        name = parts[0].strip()
        rest = parts[1].strip()
        if " at " in rest.lower():
            title_parts = re.split(r" at ", rest, maxsplit=1, flags=re.IGNORECASE)
            job_title = title_parts[0].strip()
            company = title_parts[1].strip() if len(title_parts) > 1 else ""
        else:
            job_title = rest

    # Determine if this is a person or company page
    page_type = "person" if "/in/" in url else "company" if "/company/" in url else "post"

    # Check if this person is likely a decision maker
    title_lower = job_title.lower()
    is_decision_maker = any(t.lower() in title_lower for t in TARGET_TITLES)

    # Check if the snippet contains buy signals
    snippet_lower = snippet.lower()
    buy_signals = [
        "hiring", "looking for", "need", "seeking", "open to",
        "freelancer", "contractor", "video editor", "content creator"
    ]
    has_buy_signal = any(sig in snippet_lower for sig in buy_signals)

    return {
        "source": "linkedin",
        "scraped_at": datetime.now().isoformat(),
        "page_type": page_type,
        "name": name,
        "job_title": job_title,
        "company": company,
        "linkedin_url": url,
        "snippet": snippet[:500],
        "is_decision_maker": is_decision_maker,
        "has_buy_signal": has_buy_signal,
        "email_guess": guess_email(name, company) if name and company else "",
        "outreach_sent": "No",
        "notes": "",
    }


def guess_email(name: str, company: str) -> str:
    """
    Generate common email format guesses based on name + company.
    These need to be verified — treat as guesses only.
    """
    if not name or not company:
        return ""

    # Clean company name for domain guess
    company_clean = re.sub(r"[^a-zA-Z0-9]", "", company.lower().split()[0])

    name_parts = name.strip().lower().split()
    if len(name_parts) < 2:
        return ""

    first = name_parts[0]
    last = name_parts[-1]

    # Common formats
    guesses = [
        f"{first}@{company_clean}.com",
        f"{first}.{last}@{company_clean}.com",
        f"{first[0]}{last}@{company_clean}.com",
    ]
    return " | ".join(guesses[:2])  # Return top 2 guesses


# ─── GOOGLE SHEETS PUSH ───────────────────────────────────────────────────────

def push_to_sheet(leads: list[dict], sheet_url: str):
    """Push LinkedIn leads to Google Sheet."""
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
                creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open("token.json", "w") as f:
                    f.write(creds.to_json())
            else:
                print("❌ No valid Google credentials. Run create_sheet.py first.")
                return

        gc = gspread.authorize(creds)
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        ss = gc.open_by_key(sheet_id)

        try:
            ws = ss.worksheet("LinkedIn Leads")
        except gspread.exceptions.WorksheetNotFound:
            ws = ss.add_worksheet(title="LinkedIn Leads", rows=1000, cols=20)

        headers = [
            "Name", "Job Title", "Company", "LinkedIn URL", "Page Type",
            "Is Decision Maker", "Has Buy Signal", "Snippet Preview",
            "Email Guesses", "Outreach Sent", "Notes"
        ]

        rows = [headers]
        for lead in leads:
            rows.append([
                lead["name"],
                lead["job_title"],
                lead["company"],
                lead["linkedin_url"],
                lead["page_type"],
                "✅ Yes" if lead["is_decision_maker"] else "No",
                "🎯 Yes" if lead["has_buy_signal"] else "No",
                lead["snippet"][:300],
                lead["email_guess"],
                lead["outreach_sent"],
                lead["notes"],
            ])

        ws.clear()
        ws.update(values=rows, range_name=f"A1:K{len(rows)}")
        ws.format("A1:K1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.05, "green": 0.27, "blue": 0.55},
        })
        print(f"✅ Pushed {len(leads)} LinkedIn leads to 'LinkedIn Leads' tab.")

    except ImportError:
        print("⚠️  gspread not installed. Skipping sheet push.")
    except Exception as e:
        print(f"❌ Sheet push failed: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LinkedIn lead scraper via Google search")
    parser.add_argument("--queries", default="",
                        help="Comma-separated custom LinkedIn Google queries")
    parser.add_argument("--results-per-query", type=int, default=15,
                        help="Results per search query (default: 15)")
    parser.add_argument("--output", default=OUTPUT_PATH,
                        help="Output JSON path")
    parser.add_argument("--push-to-sheet", action="store_true",
                        help="Push to Google Sheet after scraping")
    parser.add_argument("--sheet-url", default=SHEET_URL,
                        help="Google Sheet URL")
    parser.add_argument("--decision-makers-only", action="store_true",
                        help="Only keep leads identified as decision makers")
    args = parser.parse_args()

    queries = LINKEDIN_GOOGLE_QUERIES
    if args.queries:
        queries = [q.strip() for q in args.queries.split(",") if q.strip()]

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    all_leads = {}  # Deduplicate by URL
    print(f"\n🔗 LinkedIn Lead Scraper — {len(queries)} queries")
    print("=" * 60)

    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Searching: {query[:70]}...")
        results = google_search_linkedin(query, num_results=args.results_per_query)
        print(f"  Found {len(results)} LinkedIn results")

        for result in results:
            url = result.get("url", "")
            if url and url not in all_leads:
                lead = extract_profile_info(result)
                all_leads[url] = lead

        time.sleep(3)  # Be nice to DuckDuckGo

    leads = list(all_leads.values())

    # Sort: decision makers with buy signals first
    leads.sort(key=lambda x: (
        x["is_decision_maker"] and x["has_buy_signal"],
        x["is_decision_maker"],
        x["has_buy_signal"]
    ), reverse=True)

    # Filter if requested
    if args.decision_makers_only:
        leads = [l for l in leads if l["is_decision_maker"]]
        print(f"\n🎯 Filtered to {len(leads)} decision-maker leads")

    # Stats
    decision_makers = sum(1 for l in leads if l["is_decision_maker"])
    with_signals = sum(1 for l in leads if l["has_buy_signal"])
    hot_leads = sum(1 for l in leads if l["is_decision_maker"] and l["has_buy_signal"])

    print(f"\n{'='*60}")
    print(f"✅ Total unique leads:   {len(leads)}")
    print(f"🎯 Decision makers:      {decision_makers}")
    print(f"📣 With buy signals:     {with_signals}")
    print(f"🔥 HOT leads (both):     {hot_leads}")

    # Save JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {args.output}")

    # Sample output
    if leads:
        sample = leads[0]
        print(f"\n📋 Top Lead:")
        print(f"   Name:    {sample['name'] or '(Company/Post)'}")
        print(f"   Title:   {sample['job_title']}")
        print(f"   Company: {sample['company']}")
        print(f"   URL:     {sample['linkedin_url']}")
        print(f"   Signal:  {'🔥 HOT' if sample['is_decision_maker'] and sample['has_buy_signal'] else '📣 Warm'}")

    # Push to sheet
    if args.push_to_sheet and leads:
        print(f"\n📤 Pushing to Google Sheet...")
        push_to_sheet(leads, args.sheet_url)

    return leads


if __name__ == "__main__":
    main()
