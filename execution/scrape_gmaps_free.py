#!/usr/bin/env python3
"""
Google Maps Scraper — Free (No Apify)
Uses requests + BeautifulSoup to search Google Maps via the Places API
(free tier: 200 free requests/month) OR via direct Google search scraping.

TARGET STRATEGY:
  - Searches for small businesses in US + UK cities
  - Prioritizes businesses that list Gmail addresses (small business owners
    without IT departments — most reachable for cold outreach)
  - Exports to JSON + Google Sheets with email status

Usage:
    python execution/scrape_gmaps_free.py --search "Marketing Agency" --location "London UK" --limit 50
    python execution/scrape_gmaps_free.py --batch --push-to-sheet
    python execution/scrape_gmaps_free.py --search "Photography Studio" --location "New York" --gmail-only
"""

import os
import sys
import json
import time
import re
import argparse
import hashlib
import requests
from datetime import datetime
from urllib.parse import quote_plus, urljoin
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────

# US cities to target
US_CITIES = [
    "New York NY", "Los Angeles CA", "Chicago IL", "Houston TX",
    "Phoenix AZ", "Philadelphia PA", "San Antonio TX", "Dallas TX",
    "Miami FL", "Austin TX", "Nashville TN", "Denver CO",
]

# UK cities to target
UK_CITIES = [
    "London UK", "Manchester UK", "Birmingham UK", "Leeds UK",
    "Glasgow UK", "Edinburgh UK", "Bristol UK", "Sheffield UK",
]

# Business types that are likely to need video/content/social media services
# and are small enough to use Gmail
TARGET_NICHES = [
    # Content & Media
    "Marketing Agency",
    "Social Media Agency",
    "Photography Studio",
    "Video Production Company",
    "Content Creation Studio",
    # Local businesses with social media presence
    "Real Estate Agent",
    "Fitness Studio",
    "Personal Trainer",
    "Beauty Salon",
    "Restaurant",
    "Boutique",
    "Event Planner",
    "Wedding Photographer",
    # Professional services
    "Life Coach",
    "Business Coach",
    "Financial Advisor",
    "Dental Clinic",
    "Law Firm",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

OUTPUT_PATH = ".tmp/gmaps_free_leads.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1XhyQcGW4IDs5kzH7thoMRpPr_alEkxDEACV1A9KRtVE"


# ─── WEBSITE EMAIL EXTRACTOR ─────────────────────────────────────────────────

def extract_emails_from_url(url: str, timeout: int = 10) -> list[str]:
    """Fetch a website and extract all email addresses."""
    if not url or not url.startswith("http"):
        return []

    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return []

        text = resp.text

        # Find all emails
        emails = re.findall(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
            text
        )

        # Deduplicate and filter noise
        clean_emails = []
        seen = set()
        for email in emails:
            email_lower = email.lower()
            # Skip image references, template placeholders, etc.
            if any(x in email_lower for x in [
                ".png", ".jpg", ".gif", ".svg", ".css", ".js",
                "example.com", "yourdomain", "domain.com", "email@",
                "sentry.io", "w3.org", "schema.org"
            ]):
                continue
            if email_lower not in seen:
                seen.add(email_lower)
                clean_emails.append(email)

        return clean_emails[:10]  # Max 10 per site

    except Exception:
        return []


def is_gmail(email: str) -> bool:
    """Check if an email is a Gmail address."""
    return email.lower().endswith("@gmail.com")


def extract_contact_page_emails(base_url: str) -> list[str]:
    """Try to find emails on /contact, /about, /about-us pages."""
    all_emails = []

    # Try common contact pages
    contact_paths = ["/contact", "/contact-us", "/about", "/about-us", "/team"]
    for path in contact_paths:
        url = base_url.rstrip("/") + path
        try:
            emails = extract_emails_from_url(url, timeout=8)
            all_emails.extend(emails)
            if emails:
                break  # Found emails, stop looking
        except Exception:
            pass

    return all_emails


# ─── GOOGLE SEARCH FOR BUSINESSES ────────────────────────────────────────────

def search_businesses_via_google(niche: str, location: str, limit: int = 20) -> list[dict]:
    """
    Use DuckDuckGo to find businesses via search.
    Searches for: "niche" in "location" site:maps.google.com OR direct business search
    """
    query = f'"{niche}" in "{location}" contact email'
    search_url = "https://html.duckduckgo.com/html/"

    try:
        resp = requests.post(
            search_url,
            data={"q": query, "kl": "us-en"},
            headers=HEADERS,
            timeout=15
        )
        if resp.status_code != 200:
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        for r in soup.select(".result__body")[:limit]:
            title_el = r.select_one(".result__title")
            snippet_el = r.select_one(".result__snippet")
            url_el = r.select_one(".result__url")

            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            raw_url = url_el.get_text(strip=True) if url_el else ""

            if not raw_url:
                continue

            # Skip aggregator/directory sites
            skip_domains = [
                "yelp.com", "yellowpages.com", "tripadvisor.com",
                "facebook.com", "instagram.com", "twitter.com",
                "wikipedia.org", "linkedin.com", "reddit.com",
                "maps.google.com",
            ]
            if any(d in raw_url.lower() for d in skip_domains):
                continue

            if not raw_url.startswith("http"):
                raw_url = "https://" + raw_url

            results.append({
                "title": title,
                "snippet": snippet,
                "website": raw_url,
                "niche": niche,
                "location": location,
            })

        return results

    except ImportError:
        print("  ⚠️  BeautifulSoup not installed. Run: pip install beautifulsoup4")
        return []
    except Exception as e:
        print(f"  ✗ Search error: {e}")
        return []


# ─── GOOGLE PLACES API (Free tier) ───────────────────────────────────────────

def search_via_places_api(query: str, location: str, limit: int = 20) -> list[dict]:
    """
    Use Google Places Text Search API (free: 200 requests/month).
    Requires GOOGLE_PLACES_API_KEY in .env
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return []

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in {location}",
        "key": api_key,
        "language": "en",
    }

    results = []
    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        if data.get("status") not in ["OK", "ZERO_RESULTS"]:
            print(f"  ⚠️  Places API: {data.get('status')} — {data.get('error_message', '')}")
            return []

        for place in data.get("results", [])[:limit]:
            # Get website via Place Details
            place_id = place.get("place_id")
            website = ""
            phone = ""

            if place_id:
                detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
                detail_resp = requests.get(detail_url, params={
                    "place_id": place_id,
                    "fields": "website,formatted_phone_number,formatted_address",
                    "key": api_key,
                }, timeout=10)
                detail = detail_resp.json().get("result", {})
                website = detail.get("website", "")
                phone = detail.get("formatted_phone_number", "")
                time.sleep(0.1)

            results.append({
                "business_name": place.get("name", ""),
                "address": place.get("formatted_address", ""),
                "rating": place.get("rating", 0),
                "review_count": place.get("user_ratings_total", 0),
                "website": website,
                "phone": phone,
                "place_id": place_id,
                "niche": query,
                "location": location,
                "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
            })

    except Exception as e:
        print(f"  ✗ Places API error: {e}")

    return results


# ─── MAIN SCRAPER ─────────────────────────────────────────────────────────────

def scrape_niche_location(niche: str, location: str, limit: int = 20,
                          gmail_only: bool = False) -> list[dict]:
    """Scrape a niche + location and enrich with emails."""
    print(f"   Searching: '{niche}' in {location}...")

    # Try Places API first if key exists, else fall back to search
    raw_results = []

    if os.getenv("GOOGLE_PLACES_API_KEY"):
        raw_results = search_via_places_api(niche, location, limit)
        if raw_results:
            print(f"   ✅ Places API: {len(raw_results)} results")
    
    if not raw_results:
        # Fall back to DuckDuckGo search
        search_results = search_businesses_via_google(niche, location, limit)
        print(f"   🔍 Web search: {len(search_results)} results")

        # Convert search results to lead format
        for r in search_results:
            raw_results.append({
                "business_name": r["title"],
                "address": r.get("location", location),
                "rating": 0,
                "review_count": 0,
                "website": r["website"],
                "phone": "",
                "place_id": hashlib.md5(r["website"].encode()).hexdigest()[:12],
                "niche": niche,
                "location": location,
                "google_maps_url": "",
                "snippet": r.get("snippet", ""),
            })

    # Enrich with email scraping
    enriched = []
    for biz in raw_results:
        website = biz.get("website", "")
        lead_id = biz.get("place_id", hashlib.md5(website.encode()).hexdigest()[:12])

        emails = []
        gmail_emails = []

        if website:
            print(f"   📧 Checking {website[:50]}...")
            # Try homepage first
            homepage_emails = extract_emails_from_url(website)
            # Try contact page
            contact_emails = extract_contact_page_emails(website)

            all_found = list(set(homepage_emails + contact_emails))
            gmail_emails = [e for e in all_found if is_gmail(e)]
            other_emails = [e for e in all_found if not is_gmail(e)]

            # Prioritize Gmail
            emails = gmail_emails + other_emails

        lead = {
            "lead_id": lead_id,
            "scraped_at": datetime.now().isoformat(),
            "source": "gmaps_free",
            "niche": biz.get("niche", niche),
            "location": biz.get("location", location),
            "business_name": biz.get("business_name", ""),
            "address": biz.get("address", ""),
            "phone": biz.get("phone", ""),
            "website": website,
            "rating": biz.get("rating", 0),
            "review_count": biz.get("review_count", 0),
            "google_maps_url": biz.get("google_maps_url", ""),
            "all_emails": ", ".join(emails),
            "gmail_addresses": ", ".join(gmail_emails),
            "has_gmail": len(gmail_emails) > 0,
            "email_count": len(emails),
            "outreach_sent": "No",
            "reply_received": "No",
            "notes": "",
        }

        # Apply Gmail filter if requested
        if gmail_only and not lead["has_gmail"]:
            continue

        enriched.append(lead)
        time.sleep(1)  # Polite crawling

    return enriched


# ─── GOOGLE SHEETS PUSH ───────────────────────────────────────────────────────

def push_to_sheet(leads: list[dict], sheet_url: str):
    """Push GMaps free leads to Google Sheet."""
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
                print("❌ No valid credentials.")
                return

        gc = gspread.authorize(creds)
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        ss = gc.open_by_key(sheet_id)

        tab_name = "GMaps Leads (Free)"
        try:
            ws = ss.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            ws = ss.add_worksheet(title=tab_name, rows=2000, cols=20)

        headers = [
            "Business Name", "Niche", "Location", "Phone", "Website",
            "Rating", "Reviews", "All Emails", "Gmail Addresses",
            "Has Gmail?", "Email Count", "Google Maps URL",
            "Outreach Sent", "Reply Received", "Notes"
        ]

        rows = [headers]
        for lead in leads:
            rows.append([
                lead["business_name"],
                lead["niche"],
                lead["location"],
                lead["phone"],
                lead["website"],
                lead["rating"],
                lead["review_count"],
                lead["all_emails"],
                lead["gmail_addresses"],
                "✅ Yes" if lead["has_gmail"] else "No",
                lead["email_count"],
                lead["google_maps_url"],
                lead["outreach_sent"],
                lead["reply_received"],
                lead["notes"],
            ])

        ws.clear()
        ws.update(values=rows, range_name=f"A1:O{len(rows)}")
        ws.format("A1:O1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.0, "green": 0.5, "blue": 0.3},
        })
        print(f"✅ Pushed {len(leads)} leads to '{tab_name}' tab.")

    except Exception as e:
        print(f"❌ Sheet push failed: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Google Maps business scraper — finds Gmail-using businesses in US/UK"
    )
    parser.add_argument("--search", default="",
                        help="Single niche to search (e.g. 'Marketing Agency')")
    parser.add_argument("--location", default="",
                        help="Single location (e.g. 'London UK')")
    parser.add_argument("--limit", type=int, default=20,
                        help="Results per search (default: 20)")
    parser.add_argument("--batch", action="store_true",
                        help="Run all niches × all US+UK cities")
    parser.add_argument("--us-only", action="store_true",
                        help="Only search US cities")
    parser.add_argument("--uk-only", action="store_true",
                        help="Only search UK cities")
    parser.add_argument("--gmail-only", action="store_true",
                        help="Only keep leads with Gmail addresses found")
    parser.add_argument("--niches", default="",
                        help="Comma-separated list of niches to search")
    parser.add_argument("--output", default=OUTPUT_PATH,
                        help="Output JSON path")
    parser.add_argument("--push-to-sheet", action="store_true",
                        help="Push results to Google Sheet")
    parser.add_argument("--sheet-url", default=SHEET_URL,
                        help="Google Sheet URL")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Build search plan
    if args.batch:
        niches = TARGET_NICHES[:5]  # Start with top 5 niches for batch
        if args.us_only:
            cities = US_CITIES[:4]
        elif args.uk_only:
            cities = UK_CITIES[:4]
        else:
            cities = US_CITIES[:2] + UK_CITIES[:2]
    elif args.search and args.location:
        niches = [args.search]
        cities = [args.location]
    elif args.search:
        niches = [args.search]
        cities = US_CITIES[:2] + UK_CITIES[:2]
    else:
        # Default: top niches in key cities
        niches = TARGET_NICHES[:3]
        cities = ["New York NY", "Los Angeles CA", "London UK"]

    if args.niches:
        niches = [n.strip() for n in args.niches.split(",") if n.strip()]

    all_leads = {}  # Deduplicate by lead_id

    total_searches = len(niches) * len(cities)
    print(f"\n🗺️  Google Maps Lead Scraper (Free) — {total_searches} searches planned")
    print(f"   Niches:    {', '.join(niches)}")
    print(f"   Cities:    {', '.join(cities)}")
    print(f"   Gmail only: {'Yes' if args.gmail_only else 'No'}")
    print("=" * 60)

    for niche in niches:
        for city in cities:
            results = scrape_niche_location(
                niche=niche,
                location=city,
                limit=args.limit,
                gmail_only=args.gmail_only,
            )
            for lead in results:
                lead_id = lead.get("lead_id", "")
                if lead_id and lead_id not in all_leads:
                    all_leads[lead_id] = lead

            print(f"   ✅ {niche} in {city}: {len(results)} leads")
            time.sleep(2)

    leads = list(all_leads.values())

    # Sort: Gmail leads first, then by review count
    leads.sort(key=lambda x: (x.get("has_gmail", False), x.get("review_count", 0)), reverse=True)

    # Stats
    gmail_count = sum(1 for l in leads if l.get("has_gmail"))
    with_any_email = sum(1 for l in leads if l.get("all_emails"))

    print(f"\n{'='*60}")
    print(f"✅ Total unique leads:     {len(leads)}")
    print(f"📧 With Gmail addresses:  {gmail_count}")
    print(f"📬 With any email:        {with_any_email}")
    print(f"🔕 No email found:        {len(leads) - with_any_email}")

    # Save
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {args.output}")

    if leads:
        sample = leads[0]
        print(f"\n📋 Top Lead:")
        print(f"   Business: {sample['business_name']}")
        print(f"   Location: {sample['location']}")
        print(f"   Website:  {sample['website']}")
        if sample.get("gmail_addresses"):
            print(f"   📧 Gmail: {sample['gmail_addresses']}")
        elif sample.get("all_emails"):
            print(f"   📧 Email: {sample['all_emails'][:80]}")

    if args.push_to_sheet and leads:
        print(f"\n📤 Pushing to Google Sheet...")
        push_to_sheet(leads, args.sheet_url)

    return leads


if __name__ == "__main__":
    main()
