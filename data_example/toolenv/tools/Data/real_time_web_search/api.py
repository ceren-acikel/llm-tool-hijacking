import os
import requests


def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()


def real_time_web_search(
    query: str,
    page: int = 1,
    country: str = "US",
    toolbench_rapidapi_key: str | None = None
):
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": True, "msg": "Missing RAPIDAPI_KEY"}

    if not query or not str(query).strip():
        query = "news"

    url = "https://real-time-web-search.p.rapidapi.com/search"

    querystring = {
        "q": query,
        "page": page,
        "country": country
    }

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "real-time-web-search.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params=querystring, timeout=20)
    try:
        return r.json()
    except:
        return r.text
    
if __name__ == "__main__":
    out1 = real_time_web_search("iphone", page=1, country="US")
    print(out1 if isinstance(out1, str) else str(out1)[:2000])