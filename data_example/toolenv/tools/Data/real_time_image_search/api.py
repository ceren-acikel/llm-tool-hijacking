import os
import requests
from typing import Optional, Dict, Any, Tuple


def _get_key(toolbench_rapidapi_key: Optional[str]) -> str:
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()


def _get(url: str, host: str, params: Dict[str, Any], key: str, timeout: int = 20) -> Tuple[int, Any]:
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": host,
    }
    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    try:
        body = r.json()
    except Exception:
        body = r.text
    return r.status_code, body


def real_time_image_search(
    url: str,
    limit: int = 10,
    safe_search: str = "blur",
    toolbench_rapidapi_key: Optional[str] = None,
):
    """
    RapidAPI: reverse-image-search1
    Endpoint: GET /reverse-image-search
    Query params:
      - url (required): image URL to search
      - limit (optional): number of results (e.g., 10)
      - safe_search (optional): e.g., 'blur'
    """
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": True, "msg": "Missing RAPIDAPI_KEY"}

    img_url = (url or "").strip()
    if not img_url:
        return {"error": True, "msg": "Missing required parameter: url"}

    endpoint = "https://reverse-image-search1.p.rapidapi.com/reverse-image-search"
    host = "reverse-image-search1.p.rapidapi.com"

    
    params = {
        "url": img_url,
        "limit": int(limit) if limit is not None else 10,
        "safe_search": (safe_search or "blur").strip(),
    }

    status, body = _get(endpoint, host, params, key)
    return body if status == 200 else {"error": True, "status_code": status, "response": body}


if __name__ == "__main__":
    test_url = "https://i.imgur.com/HBrB8p0.png"
    out = real_time_image_search(test_url, limit=10, safe_search="blur")
    s = out if isinstance(out, str) else str(out)
    print(s[:2000])