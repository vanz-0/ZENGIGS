# Directive: AI API Usage & Fallback Rules

## Rule 1: Always Use the Cheapest Coding Model First

When calling any AI API for code-generation, JSON extraction, or text processing tasks:
- **Primary model**: `qwen/qwen3-coder:free` via OpenRouter — it is a dedicated coding model and is free.
- **Secondary**: `openai/gpt-oss-20b:free` — lightweight GPT-class, good for structured JSON.
- **Tertiary**: `openai/gpt-oss-120b:free` — heavier GPT fallback.
- Only escalate to larger/paid models if the task explicitly requires it.

## Rule 2: OpenRouter is the Universal AI Fallback

**Any time an AI API call fails** (rate limit, auth error, model unavailable, quota exceeded), the system must fall back to **OpenRouter**.

- OpenRouter endpoint: `https://openrouter.ai/api/v1/chat/completions`
- OpenRouter key: stored in `.env` as `OPENROUTER_API_KEY`
- OpenRouter is OpenAI-API-compatible — just change `base_url` and `model`.
- OpenRouter cascades through our model list automatically (see `execution/lead_scraper_generic.py`).

### Applies to all scripts:
- `execution/lead_scraper_generic.py` — ✅ already uses OpenRouter cascade
- `execution/enrich_leads.py` — uses `lead_scraper_generic.py` (covered)
- Any future scripts that call an AI API must follow the same pattern.

## Rule 3: Verified Free Model Cascade (as of June 2026)

```python
OPENROUTER_MODELS = [
    "qwen/qwen3-coder:free",           # PRIMARY — cheapest coding model
    "openai/gpt-oss-20b:free",         # lightweight GPT-class
    "openai/gpt-oss-120b:free",        # heavier GPT fallback
    "meta-llama/llama-3.3-70b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "deepseek/deepseek-r1-0528:free",  # last resort
]
```

> **Note**: `google/gemma-4-27b-it:free` returns 400 Bad Request — do not use.

## Rule 4: Unicode Safety on Windows

All AI-generated text must be sanitized before writing to file or database on Windows:
```python
def _clean_unicode(text: str) -> str:
    return text.encode("ascii", errors="ignore").decode("ascii")
```
This strips narrow no-break spaces (`\u202f`) and other non-ASCII characters that Windows charmap can't handle.
