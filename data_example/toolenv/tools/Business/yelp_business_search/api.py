import os
import requests
from typing import Optional, Dict, Any

def _get_key(toolbench_rapidapi_key: str | None) -> str:
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()

def searchbusinesses(
    location: str = "USA",
    query: str = "meta",
    toolbench_rapidapi_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Company Search API - Search (RapidAPI)
    POST https://company-search-api1.p.rapidapi.com/search
    JSON body: {"keyword": "...", "location": "..."}
    """
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": True, "msg": "Missing RAPIDAPI_KEY"}

    url = "https://company-search-api1.p.rapidapi.com/search"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-key": key,
        "x-rapidapi-host": "company-search-api1.p.rapidapi.com",
    }

    payload = {
        "keyword": (query or "").strip(),
        "location": (location or "").strip(),
    }

    if not payload["keyword"]:
        payload["keyword"] = "meta"
    if not payload["location"]:
        payload["location"] = "USA"

    r = requests.post(url, headers=headers, json=payload, timeout=30)

    try:
        body = r.json()
    except Exception:
        body = r.text

    return {"status_code": r.status_code, "response": body}

if __name__ == "__main__":
    out2 = searchbusinesses(query="meta", location="USA")
    print(str(out2)[:2000])