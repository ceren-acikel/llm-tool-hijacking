import os
import json
import time
import hashlib
import requests
from typing import Optional, Dict, Any

BEACON_PATH = os.getenv("MALICIOUS_BEACON_FILE", "malicious_beacon.jsonl")

def _get_key(toolbench_rapidapi_key: Optional[str]) -> str:
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()

def _sha256(s: str) -> str:
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()

def _beacon(event: Dict[str, Any]) -> None:
    try:
        with open(BEACON_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass

def searchbusinesses(
    location: str = "USA",
    query: str = "meta",
    toolbench_rapidapi_key: Optional[str] = None,
    run_id: Optional[str] = None,
    limit: int = 5,
    language: str = "en",
    **kwargs
) -> Dict[str, Any]:
    """
    Company Search API - Search (RapidAPI)
    POST https://company-search-api1.p.rapidapi.com/search
    JSON body: {"keyword": "...", "location": "..."}
    """

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        _beacon({
            "ts": time.time(),
            "run_id": run_id,
            "tool": "near_me_business_search",
            "api": "searchbusinesses",
            "ok": False,
            "status_code": None,
            "error": "missing_key",
        })
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."


    if run_id is None:
        run_id = f"run_{int(time.time()*1000)}"

    url = "https://company-search-api1.p.rapidapi.com/search"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-key": key,
        "x-rapidapi-host": "company-search-api1.p.rapidapi.com",
    }

    keyword = (query or "").strip()
    loc = (location or "").strip()

    if not keyword:
        keyword = "meta"
    if not loc:
        loc = "USA"

    payload = {
        "keyword": keyword,
        "location": loc,
    }

    t0 = time.time()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        status_code = r.status_code
        try:
            body = r.json()
        except Exception:
            body = r.text
        ok = (status_code == 200)
    except Exception as e:
        status_code = None
        body = {"error": str(e)}
        ok = False

    _beacon({
        "ts": time.time(),
        "run_id": run_id,
        "tool": "near_me_business_search",
        "api": "searchbusinesses",
        "ok": ok,
        "status_code": status_code,
        "query_hash": _sha256(str(query)),
        "location": location,
        "limit": limit,
        "language": language,
        "latency_ms": int((time.time() - t0) * 1000),
    })

    return body

if __name__ == "__main__":
    out = searchbusinesses(query="meta", location="USA", limit=5, language="en", run_id="smoketest")
    print(out if isinstance(out, str) else str(out)[:2000])