# ZENGIGS Knowledge Base — Index

> This file is the content-oriented catalog of the entire ZENGIGS wiki.  
> The LLM reads this first to locate relevant pages before drilling into them.  
> Updated automatically on every ingest, query, or lint pass.

---

## Entities

| Page | Summary | Source Count |
|------|---------|:------------:|
| [ZENGIGS](entities/zengigs.md) | The ZENGIGS VA brand — mission, service pillars, pricing, and positioning. | 1 |

## Concepts

| Page | Summary |
|------|---------|
| [VA Service Pillars](concepts/service_pillars.md) | AI & Automation, Media Production, Social Media Strategy — the three execution pillars. |
| [30-Day Roadmap](concepts/30_day_roadmap.md) | The "Zero Leads to Fully Booked" 30-day launch plan from the VA Blueprint. |
| [Pricing Tiers](concepts/pricing_tiers.md) | Starter ($480/mo), Growth ($940/mo), Premium ($1800/mo) packages. |
| [Cold Outreach Playbook](concepts/cold_outreach.md) | Lead scraping → personalization → SMTP sending → follow-up sequences. |
| [Proposal Framework](concepts/proposal_framework.md) | Discovery call → problem/benefit expansion → PandaDoc generation. |

## Sources

| Source | Type | Ingested |
|--------|------|----------|
| [VA_Business_Blueprint_2025.pdf](../raw/VA_Business_Blueprint_2025.pdf) | PDF | 2026-05-10 |
| [Agentic Workflows](../.tmp/Agentic%20Workflows/) | Reference repo | 2026-05-11 |
| [Karpathy Second Brain Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Methodology | 2026-05-11 |

## Directives (SOPs)

| Directive | Script(s) | Status |
|-----------|-----------|--------|
| [01_portfolio_and_profiles](../directives/01_portfolio_and_profiles.md) | — | Active |
| [02_cold_outreach_system](../directives/02_cold_outreach_system.md) | `cold_email_sender.py`, `lead_scraper.py` | Upgrading |
| [03_sales_and_onboarding](../directives/03_sales_and_onboarding.md) | — | Active |
| [04_social_media_strategy](../directives/04_social_media_strategy.md) | — | Active |
| [05_lead_scraping](../directives/05_lead_scraping.md) | `scrape_leads.py` | NEW |

## Execution Scripts

| Script | Purpose | Dependencies |
|--------|---------|-------------|
| `lead_scraper.py` | Standardize raw lead CSV exports | `csv`, `argparse` |
| `cold_email_sender.py` | Automated SMTP cold email with rate limiting | `smtplib`, `dotenv` |
| `kpi_tracker.py` | Daily metric logging to CSV | `csv`, `datetime` |
| `scrape_leads.py` | Apify lead scraping pipeline | `apify-client`, `dotenv` |

---

*Last updated: 2026-05-11*
