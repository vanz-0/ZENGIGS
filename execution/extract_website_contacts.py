import os
import re
import json
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and OpenAI:
        return OpenAI(api_key=api_key)
    return None

def extract_emails(text):
    """Extract emails using regex"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(email_pattern, text)))

def extract_social_links(soup):
    """Extract social media links from soup"""
    socials = {"facebook": "", "twitter": "", "linkedin": "", "instagram": "", "youtube": "", "tiktok": ""}
    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if 'facebook.com' in href: socials['facebook'] = a['href']
        elif 'twitter.com' in href or 'x.com' in href: socials['twitter'] = a['href']
        elif 'linkedin.com' in href: socials['linkedin'] = a['href']
        elif 'instagram.com' in href: socials['instagram'] = a['href']
        elif 'youtube.com' in href: socials['youtube'] = a['href']
        elif 'tiktok.com' in href: socials['tiktok'] = a['href']
    return socials

def scrape_website_contacts(website_url, business_name):
    """
    Scrape website for contacts, uses OpenAI if available to parse unstructured text.
    """
    result = {
        "emails": [],
        "phone_numbers": [],
        "business_hours": "",
        "social_media": {"facebook": "", "twitter": "", "linkedin": "", "instagram": "", "youtube": "", "tiktok": ""},
        "owner_info": {"name": "", "title": "", "email": "", "phone": "", "linkedin": ""},
        "team_members": [],
        "additional_contacts": [],
        "_pages_scraped": 0,
        "_search_enriched": False,
        "error": None
    }
    
    if not website_url:
        result["error"] = "No URL provided"
        return result

    if not website_url.startswith('http'):
        website_url = 'http://' + website_url

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    pages_to_scrape = [website_url]
    scraped_text = ""
    
    try:
        # Get homepage
        response = requests.get(website_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        result["_pages_scraped"] += 1
        scraped_text += soup.get_text(separator=' ', strip=True) + "\n"
        
        # Look for contact/about pages
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            if 'contact' in href or 'about' in href:
                full_url = urljoin(website_url, a['href'])
                if full_url not in pages_to_scrape and urlparse(full_url).netloc == urlparse(website_url).netloc:
                    pages_to_scrape.append(full_url)
                    if len(pages_to_scrape) > 3: # limit to 3 pages
                        break
                        
        # Scrape additional pages
        for page_url in pages_to_scrape[1:]:
            try:
                resp = requests.get(page_url, headers=headers, timeout=10)
                page_soup = BeautifulSoup(resp.text, 'html.parser')
                result["_pages_scraped"] += 1
                scraped_text += page_soup.get_text(separator=' ', strip=True) + "\n"
                
                # Merge social links
                socials = extract_social_links(page_soup)
                for k, v in socials.items():
                    if v and not result["social_media"].get(k):
                        result["social_media"][k] = v
            except:
                pass
                
        # Basic regex fallback
        result["emails"] = extract_emails(scraped_text)
        
        # Merge homepage social links
        socials = extract_social_links(soup)
        for k, v in socials.items():
            if v and not result["social_media"].get(k):
                result["social_media"][k] = v

        # OpenAI Enrichment
        client = get_openai_client()
        if client:
            try:
                system_prompt = "You are a data extractor. Extract contact info from the text and return as JSON matching this schema: {\"phone_numbers\": [], \"business_hours\": \"\", \"owner_info\": {\"name\": \"\", \"title\": \"\", \"email\": \"\", \"phone\": \"\", \"linkedin\": \"\"}, \"team_members\": [{\"name\": \"\", \"title\": \"\", \"email\": \"\"}]}. Return ONLY valid JSON."
                
                # truncate text to fit context
                truncated_text = scraped_text[:12000]
                
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Extract info for business '{business_name}' from this text:\n\n{truncated_text}"}
                    ],
                    response_format={"type": "json_object"}
                )
                
                extracted = json.loads(completion.choices[0].message.content)
                result["phone_numbers"] = extracted.get("phone_numbers", [])
                result["business_hours"] = extracted.get("business_hours", "")
                result["owner_info"].update(extracted.get("owner_info", {}))
                result["team_members"] = extracted.get("team_members", [])
                result["_search_enriched"] = True
                
                # Merge emails found by OpenAI
                if result["owner_info"].get("email") and result["owner_info"]["email"] not in result["emails"]:
                    result["emails"].append(result["owner_info"]["email"])
            except Exception as e:
                result["error"] = f"OpenAI parsing error: {str(e)}"
                
    except Exception as e:
        result["error"] = str(e)

    return result

if __name__ == "__main__":
    # Test script
    res = scrape_website_contacts("https://www.example.com", "Example Business")
    print(json.dumps(res, indent=2))
