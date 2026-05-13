# Directive 05: Lead Scraping & Enrichment Pipeline

## Goal
Scrape B2B leads from public sources (Apify, Google Maps), normalize the data into a unified schema, and optionally enrich with verified email addresses. The final output is synchronized to the Supabase `leads` table and exported to a CSV.

## Architecture
- **Layer 1 (Directive)**: This document.
- **Layer 2 (Orchestration)**: System logic reading inputs and calling execution tools.
- **Layer 3 (Execution)**: `execution/pipeline_orchestrator.py`, `execution/scrape_leads.py`

## Inputs
| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query` | Yes | Search query (e.g., "SaaS Founders") |
| `--location` | Yes | Geographic target (e.g., "United States") |
| `--max_items` | No | Max results to scrape (default: 50) |
| `--no-email-filter`| No | Skip email validation filter during scrape |

## Process Flow

1. **Initialization & Scrape**
   - Execute `execution/pipeline_orchestrator.py --action scrape --query "<Query>" --location "<Location>"`
   - Script triggers Apify actor `code_crafter/leads-finder`.
   - Handles retries (up to 3x) for Apify timeouts.

2. **Normalization**
   - Raw JSON output is automatically normalized by the pipeline into a standard schema: `email, first_name, last_name, company, website, location, niche, status`.
   - Missing names drop the lead unless `status` is marked 'for_enrichment'.

3. **Data Synchronization (Supabase)**
   - Normalized leads are bulk-upserted into the Supabase `public.leads` table.
   - Deduplication is handled natively via the `email` UNIQUE constraint in Supabase.

4. **[OPTIONAL] Email Enrichment**
   - If `--enrich` flag is passed, missing emails are sent to Hunter.io or AnyMailFinder API.

## Cost Analysis (Tracking)
The system calculates cost dynamically after each run:
- **Apify leads-finder**: ~$0.01 per lead
- **Email enrichment**: ~$0.01 per successful API hit
- The total cost is logged to the CLI output. *Rule: Maximum budget per run is $10 unless overridden.*

## Error Handling & Rate Limiting
- **Apify API Errors**: The script implements exponential backoff (2s, 4s, 8s) if the API fails to respond.
- **Database Connection Errors**: If Supabase is unreachable, data falls back to a `.tmp/leads_backup.json` file.
- **Empty Results**: Broaden the query or change the location. Log the failed query to prevent future repeats.

## Learnable Patterns (Continuous Improvement)
- **Pattern**: Queries with "Consultant" yield higher bounce rates than "Agency".
- **Pattern**: Use `--no-email-filter` for initial wide-net scrapes, then enrich only the highly relevant leads to save Apify costs.
- **Pattern**: Always ensure the niche matches the `query` parameter exactly for accurate personalization downstream.

## Outputs
- **Primary**: Supabase `leads` table updated.
- **Secondary**: `execution/leads.csv` (for legacy/manual processes).
- **Temporary**: `.tmp/` folder contains raw JSON exports (safe to delete).
