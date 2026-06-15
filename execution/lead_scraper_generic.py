import os
import json
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# OpenRouter model cascade — cheapest/coding models first, powerful fallbacks after.
# google/gemma-4-27b excluded (consistently returns 400).
OPENROUTER_MODELS = [
    "qwen/qwen3-coder:free",           # cheapest coding model — primary
    "openai/gpt-oss-20b:free",         # lightweight GPT-class
    "openai/gpt-oss-120b:free",        # heavier GPT fallback
    "meta-llama/llama-3.3-70b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "deepseek/deepseek-r1-0528:free",  # last resort
]

SYSTEM_PROMPT = """You are an expert cold email copywriter and business analyst. Based on the website text provided, extract three things:

1. "business_summary": A short, precise description of what the business actually does (2-3 sentences, based only on the site content).
2. "recent_data": Pull any specific recent info — blog posts, product launches, news, awards, case studies, company milestones. **Prioritize any recent updates from 2026 or any recent videos they have posted.** If none found, write "No recent data found".
3. "personalization_line": ONE single, natural-sounding opening sentence for a cold email that references something specific from business_summary or recent_data. Ideally, reference a 2026 update or one of their videos if available! Must feel human, not robotic. Examples:
   - "Saw your recent 2026 update on [X] — really impressive how you approached [Y]."
   - "Loved the recent video on your site — that approach to [W] is exactly the kind of thinking we work with."

Return ONLY valid JSON:
{"business_summary": "...", "recent_data": "...", "personalization_line": "..."}"""


def _clean_unicode(text: str) -> str:
    """Replace non-ASCII unicode chars with safe ASCII equivalents."""
    replacements = {
        "\u202f": " ",   # narrow no-break space → regular space
        "\u00a0": " ",   # non-breaking space → regular space
        "\u2011": "-",   # non-breaking hyphen → hyphen
        "\u2013": "-",   # en dash → hyphen
        "\u2014": "-",   # em dash → hyphen
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Strip any remaining non-ASCII
    return text.encode("ascii", errors="ignore").decode("ascii")

def _scrape_text(website_url: str) -> str:
    """Fetch and clean website text."""
    if not website_url.startswith("http"):
        website_url = "https://" + website_url
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(website_url, headers=headers, timeout=12)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)[:12000]


def _call_openrouter(prompt: str) -> dict:
    """
    Call OpenRouter API, cascading through free models until one succeeds.
    OpenRouter is OpenAI-compatible — just a different base_url + model name.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://zengigs.com",
        "X-Title": "ZENGIGS Lead Enrichment",
        "Content-Type": "application/json",
    }

    for model in OPENROUTER_MODELS:
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.4,
            }
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if r.status_code == 429:
                print(f"  [OpenRouter] {model} rate-limited, trying next model...")
                time.sleep(2)
                continue

            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            result = json.loads(content)
            print(f"  [OpenRouter] Used model: {model}")
            return result

        except json.JSONDecodeError:
            print(f"  [OpenRouter] {model} returned invalid JSON, trying next...")
            continue
        except Exception as e:
            print(f"  [OpenRouter] {model} failed: {e}, trying next...")
            continue

    raise RuntimeError("All OpenRouter models exhausted without a successful response.")


def generate_personalization(website_url: str, company_name: str) -> dict:
    """
    Scrape a business website and generate:
    - business_summary: what they actually do (for visual verification)
    - recent_data:      any recent news/posts found on their site
    - personalization_line: a unique, human cold email opener
    """
    fallback = {
        "business_summary": "Could not retrieve website content.",
        "recent_data": "No recent data found.",
        "personalization_line": f"Came across {company_name} and was genuinely impressed by what you're building.",
    }

    try:
        scraped_text = _scrape_text(website_url)
    except Exception as e:
        print(f"  [Scrape Error] {website_url}: {e}")
        return fallback

    prompt = f"Company: {company_name}\n\nWebsite Content:\n{scraped_text}"

    try:
        result = _call_openrouter(prompt)
        # Sanitize unicode chars that Windows charmap can't handle
        return {k: _clean_unicode(v) for k, v in result.items()}
    except Exception as e:
        print(f"  [All models failed] {e}")
        return fallback


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://apify.com"
    company = sys.argv[2] if len(sys.argv) > 2 else "Apify"
    print(f"Scraping: {url}")
    result = generate_personalization(url, company)
    print(json.dumps(result, indent=2))
