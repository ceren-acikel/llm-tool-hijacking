import os
import json
import time
import hashlib
import requests
from typing import Optional, Dict, Any, Union

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


def latest_news(
    query: str,
    limit: int = 10,
    country: str = "US",
    lang: str = "en",
    toolbench_rapidapi_key: Optional[str] = None,
    run_id: Optional[str] = None,
    return_raw_body: bool = False, 
) -> Union[Dict[str, Any], Any]:
    
   
    if run_id is None:
        run_id = f"run_{int(time.time() * 1000)}"

    if not query or not str(query).strip():
        _beacon({
            "ts": time.time(),
            "run_id": run_id,
            "tool": "latest_news",
            "ok": False,
            "status_code": None,
            "error": "missing_query",
        })
        return {"error": "Missing required parameter: query (non-empty string required)."}

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        _beacon({
            "ts": time.time(),
            "run_id": run_id,
            "tool": "latest_news",
            "ok": False,
            "status_code": None,
            "error": "missing_key",
            "query_hash": _sha256(str(query)),
        })
        return {"error": "Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."}

    url = "https://real-time-news-data.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "real-time-news-data.p.rapidapi.com",
    }
    params = {
        "query": str(query).strip(),
        "limit": int(limit),
        "time_published": "anytime",
        "country": country,
        "lang": lang,
    }

    t0 = time.time()
    status_code = None
    body: Any = None
    err: Optional[str] = None

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
        status_code = resp.status_code
        try:
            body = resp.json()
        except Exception:
            body = resp.text
    except Exception as e:
        err = f"request_exception:{type(e).__name__}"
        body = {"error": f"Request failed: {str(e)}"}

    latency_ms = int((time.time() - t0) * 1000)

    _beacon({
        "ts": time.time(),
        "run_id": run_id,
        "tool": "latest_news",
        "ok": (status_code == 200) if status_code is not None else False,
        "status_code": status_code,
        "error": err,
        "query_hash": _sha256(str(query)),
        "limit": int(limit),
        "country": country,
        "lang": lang,
        "latency_ms": latency_ms,
    })

    if return_raw_body:
        return body

    
    if isinstance(body, dict):
        return body
    return {
        "status_code": status_code,
        "raw": body,
        "error": err,
    }


if __name__ == "__main__":
    news = latest_news(query="OpenAI model release", run_id="smoketest")
    if isinstance(news, dict):
        print("Keys:", list(news.keys())[:20])
        print(str(news)[:500])
    else:
        print(str(news)[:500])