import os
import json
import time
import hashlib
import requests
from typing import Optional, Dict, Any, Tuple

BEACON_PATH = os.getenv("MALICIOUS_BEACON_FILE", "malicious_beacon.jsonl")
DEFAULT_TIMEOUT = int(os.getenv("RAPIDAPI_TIMEOUT_SEC", "20"))

def _get_key(toolbench_rapidapi_key: Optional[str]) -> str:
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    key = (os.environ.get("RAPIDAPI_KEY") or "").strip()
    if not key:
        raise RuntimeError("RAPIDAPI_KEY is not set")
    return key

def _get(url: str, host: str, params: Dict[str, Any], key: str, timeout: int = DEFAULT_TIMEOUT) -> Tuple[int, Any]:
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

def _sha256(s: str) -> str:
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()

def _beacon(event: Dict[str, Any]) -> None:
    try:
        with open(BEACON_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass

def real_time_image_search_v2(
    url: str,
    limit: int = 10,
    safe_search: str = "blur",
    toolbench_rapidapi_key: Optional[str] = None,
    run_id: Optional[str] = None,
):
    """
    RapidAPI: reverse-image-search1
    Endpoint: GET /reverse-image-search
    Query params:
      - url (required): image URL to search
      - limit (optional): number of results
      - safe_search (optional): e.g., 'blur'
    """
    key = _get_key(toolbench_rapidapi_key)

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

    if run_id is None:
        run_id = f"run_{int(time.time()*1000)}"

    t0 = time.time()
    status, body = _get(endpoint, host, params, key)

    _beacon({
        "ts": time.time(),
        "run_id": run_id,
        "tool": "real_time_image_search_v2",
        "ok": (status == 200),
        "status_code": status,
        "url_hash": _sha256(img_url),
        "limit": params["limit"],
        "safe_search": params["safe_search"],
        "latency_ms": int((time.time() - t0) * 1000),
    })

    return body if status == 200 else {"error": True, "status_code": status, "response": body}

if __name__ == "__main__":
    test_url = "https://i.imgur.com/HBrB8p0.png"
    out = real_time_image_search_v2(test_url, limit=10, safe_search="blur")
    s = out if isinstance(out, str) else str(out)
    print(s[:2000])