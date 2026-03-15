import json
import re
import html
from pathlib import Path
from typing import Any, Dict, Optional, List

import requests

BASE_DIR = Path(__file__).resolve().parent
TOOL_JSON_ROOT = (BASE_DIR / "../tool_jsons").resolve()
print("[DEBUG] TOOL_JSON_ROOT =", TOOL_JSON_ROOT)
TIMEOUT = 25


RAPIDAPI_TOOL_PAGES = {
    "api_shopping": "https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data",
    "yelp_business_search": "https://rapidapi.com/remote-skills-remote-skills-default/api/company-search-api1",
    "principalapis_timeseries": "https://rapidapi.com/principalapis/api/currency-conversion-and-exchange-rates",
    "fast_price_crypto_from": "https://rapidapi.com/apiwizard/api/fast-price-exchange-rates",
    "currency_converter_pro_latest_rates": "https://rapidapi.com/Dezento/api/currency-converter-pro1",
    "exchangerate_api_latest_usd": "https://rapidapi.com/exchangerateapi/api/exchangerate-api",
    "get_asset_profile": "https://rapidapi.com/mbzkrm/api/realtime-stock-data",
    "get_stock_recommendations": "https://rapidapi.com/3b-data-3b-data-default/api/yahoo-finance-real-time1",
    "get_latest_exchange_rates": "https://rapidapi.com/coderog-coderog-default/api/currency-exchange-rate-api1",
    "enterprise_values": "https://rapidapi.com/contact-8Fn44oGJQx/api/financial-modeling-prep",
    "alpha_vantage_daily": "https://rapidapi.com/alphavantage/api/alpha-vantage",
    "get_geo_ip9": "https://rapidapi.com/abdheshnayak/api/ip-geo-location9",
    "get_ipwhois": "https://rapidapi.com/xakageminato/api/ip-geolocation-ipwhois-io",
    "get_geo_ip_geo_location10": "https://rapidapi.com/tjdh-tjdh-default/api/ip-geo-location10",
    "get_geo_find_ip_info": "https://rapidapi.com/Chetan11dev/api/ip-geolocation-find-ip-location-and-ip-info",
    "get_geo_api6": "https://rapidapi.com/oceanrock/api/ip-geolocation-api6",
    "list_idealista_properties": "https://rapidapi.com/apidojo/api/idealista2",
    "list_us_properties": "https://rapidapi.com/apidojo/api/realty-in-us",
    "list_zoopla_properties": "https://rapidapi.com/apidojo/api/zoopla",
    "search_news": "https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-news-data",
    "real_time_finance_data": "https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-finance-data",
    "real_time_image_search": "https://rapidapi.com/letscrape-6bRBa3QguO5/api/reverse-image-search1",
    "real_time_web_search": "https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-web-search",
    "get_streaming_show": "https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/streaming-availability",
    "imdb_cast_titles": "https://rapidapi.com/rapidapi-org1-rapidapi-org-default/api/imdb236",
    "list_netflix_titles": "https://rapidapi.com/robotfa-robotfa-default/api/netflix-movies-and-tv-shows1",
    "movie_genres": "https://rapidapi.com/jakash1997/api/advanced-movie-search",
    "similar_movies": "https://rapidapi.com/animeslayerquiz/api/similar-movies"
}

CLONES = {
    "yelp_business_search": ["yelp_business_search_v2", "near_me_business_search"],
    "real_time_web_search": ["real_time_web_search_v2", "best_web_search"],
    "real_time_image_search": ["real_time_image_search_v2"],
    "search_news": ["search_news_v2", "latest_news"],
    "real_time_finance_data": ["real_time_finance_data_v2", "finance_search"],
    "similar_movies": ["most_similar_movies"]
}


MAX_CHARS = 1200 

def clean_text(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)          
    s = re.sub(r"\s+", " ", s).strip()      
    if MAX_CHARS and len(s) > MAX_CHARS:
        s = s[:MAX_CHARS].rstrip() + "…"
    return s

def fetch_html(url: str) -> str:
    r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def extract_next_data(html_text: str) -> Optional[Dict[str, Any]]:

    m = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None

def find_first(obj: Any, key_candidates: set) -> Optional[str]:
   
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in key_candidates and isinstance(v, str) and v.strip():
                return v
            found = find_first(v, key_candidates)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_first(item, key_candidates)
            if found:
                return found
    return None

def extract_meta_description(html_text: str) -> Optional[str]:
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html_text, re.IGNORECASE)
    if m:
        return m.group(1)
    return None

def locate_tool_json(tool_name: str) -> Optional[Path]:
    matches = list(TOOL_JSON_ROOT.rglob(f"{tool_name}.json"))
    return matches[0] if matches else None

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Extraction logic
def extract_descriptions_from_rapidapi(page_url: str) -> Dict[str, str]:
    """
    output:
      - tool_description
      - api_description
    """
    html_text = fetch_html(page_url)
    next_data = extract_next_data(html_text)


    tool_desc_raw = None
    api_desc_raw = None

    if next_data:
        
        tool_desc_raw = find_first(next_data, {"description", "shortDescription", "tagline", "summary"})
        api_desc_raw = find_first(next_data, {"endpointDescription", "description", "shortDescription"})


    if not tool_desc_raw:
        tool_desc_raw = extract_meta_description(html_text)

    if not api_desc_raw:
        api_desc_raw = tool_desc_raw  

    return {
        "tool_description": clean_text(tool_desc_raw or ""),
        "api_description": clean_text(api_desc_raw or ""),
    }


def apply_descriptions_to_tool_json(tool_json, tool_desc, api_desc):
    tool_json["tool_description"] = tool_desc

    api_list = tool_json.get("api_list", [])
    for api in api_list:
        api["description"] = api_desc          
        api["api_description"] = api_desc      

    return tool_json

def debug_existing_tools():
    files = list(TOOL_JSON_ROOT.rglob("*.json"))
    names = {p.stem for p in files}
    print(f"[DEBUG] Found {len(names)} tool jsons under {TOOL_JSON_ROOT}")
    missing = [k for k in RAPIDAPI_TOOL_PAGES.keys() if k not in names]
    if missing:
        print("[DEBUG] Missing tool jsons for these RAPIDAPI_TOOL_PAGES keys:")
        for k in missing:
            close = sorted([n for n in names if k in n or n in k])[:5]
            print(f"  - {k} (close: {close})")
    else:
        print("[DEBUG] All RAPIDAPI_TOOL_PAGES keys exist as json filenames.")

def main():
    debug_existing_tools()
    updated = 0

    for tool_name, page_url in RAPIDAPI_TOOL_PAGES.items():
        tool_path = locate_tool_json(tool_name)
        if not tool_path:
            print(f"[WARN] tool json not found for: {tool_name}")
            continue

        descs = extract_descriptions_from_rapidapi(page_url)
        if not descs["tool_description"]:
            print(f"[WARN] empty description extracted for: {tool_name} (url={page_url})")
            continue

        # benign update
        benign = load_json(tool_path)
        benign = apply_descriptions_to_tool_json(benign, descs["tool_description"], descs["api_description"])
        save_json(tool_path, benign)
        print(f"[OK] updated benign: {tool_name} -> {tool_path}")
        updated += 1

        # clones update (copy EXACT same strings)
        for clone_name in CLONES.get(tool_name, []):
            clone_path = locate_tool_json(clone_name)
            if not clone_path:
                print(f"[WARN] clone json not found for: {clone_name}")
                continue
            clone = load_json(clone_path)
            clone = apply_descriptions_to_tool_json(clone, descs["tool_description"], descs["api_description"])
            save_json(clone_path, clone)
            print(f"[OK] copied to clone: {clone_name} -> {clone_path}")
            updated += 1

    print(f"\nDone. Updated files: {updated}")


if __name__ == "__main__":
    main()