# Lead Scraping & Enrichment

## Goal
Scrape B2B leads from public sources (Apify, Google Maps), normalize the data, and optionally enrich with verified email addresses. Deliver clean, actionable lead lists ready for outreach.

## Inputs
| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query` | Yes | Search query (e.g., "Coaches", "SaaS Founders") |
| `--location` | Yes | Geographic target (e.g., "United States") |
| `--max_items` | No | Max results to scrape (default: 25) |
| `--output_prefix` | No | Filename prefix (default: "leads") |
| `--no-email-filter` | No | Skip email validation filter (faster, more results) |

## Tools/Scripts
- Script: `execution/scrape_leads.py` (Apify lead scraping)
- Script: `execution/lead_scraper.py` (CSV normalization)
- Dependencies: `apify-client`, `python-dotenv`

## Process

1. **Test Scrape**
   - Run: `python execution/scrape_leads.py --query "Coaches" --location "United States" --max_items 25`
   - Output: `.tmp/test_leads.json`

2. **Verification**
   - Read `.tmp/test_leads.json`.
   - Check if ≥80% of leads match the target industry.
   - **Pass**: Proceed to full scrape.
   - **Fail**: Refine query or location, re-run test.

3. **Full Scrape**
   - Run: `python execution/scrape_leads.py --query "Coaches" --location "United States" --max_items 200`
   - Output: `.tmp/leads_[timestamp].json`

4. **Normalize to CSV**
   - Run: `python execution/lead_scraper.py --input .tmp/leads_[timestamp].json --output execution/leads.csv`
   - Standardizes fields: `first_name`, `last_name`, `email`, `company`, `website`, `location`.

5. **[OPTIONAL] Email Enrichment**
   - If emails are missing, use AnyMailFinder or Hunter.io API.
   - Requires `ANYMAILFINDER_API_KEY` in `.env`.

## Outputs (Deliverables)
- **Primary**: `execution/leads.csv` — clean, normalized lead file ready for `cold_email_sender.py`.
- **Intermediate** (not deliverables): `.tmp/test_leads.json`, `.tmp/leads_*.json`.

## Cost Considerations
| Component | Cost per lead |
|-----------|---------------|
| Apify leads-finder | ~$0.01-0.02 |
| Email enrichment (optional) | ~$0.01 |
| **Total** | **~$0.01-0.03** |

For 200 leads: ~$2-6 total.

## Edge Cases
- **No leads found**: Apify returns empty list. → Broaden search query.
- **API Error**: Check `APIFY_API_TOKEN` in `.env`.
- **Duplicate leads**: `lead_scraper.py` deduplicates by email address.
- **Missing names**: Skip leads without `first_name` — they can't be personalized.

## Learnings
- Use `--no-email-filter` for initial scrapes, then enrich later for better coverage.
- Location should be specific (city/state) for local businesses, broad (country) for remote services.
- Apify's `code_crafter/leads-finder` actor is the most reliable for B2B contacts.
