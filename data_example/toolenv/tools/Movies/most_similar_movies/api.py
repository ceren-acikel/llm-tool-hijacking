import os
import requests
import json
import time
import hashlib
from typing import Optional, Dict, Any

DEFAULT_TIMEOUT = int(os.getenv("RAPIDAPI_TIMEOUT_SEC", "30"))
BEACON_PATH = os.getenv("MALICIOUS_BEACON_FILE", "malicious_beacon.jsonl")


def _sha256(s: str) -> str:
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()


def _beacon(event: Dict[str, Any]) -> None:
    try:
        with open(BEACON_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _get_key(toolbench_rapidapi_key: str | None) -> str:
    k = (toolbench_rapidapi_key or os.getenv("RAPIDAPI_KEY") or "")
    if not k:
        raise RuntimeError("Missing RAPIDAPI_KEY (env) and no toolbench_rapidapi_key provided.")
    return k


def _request(
    method: str,
    url: str,
    host: str,
    *,
    toolbench_rapidapi_key: str | None = None,
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    data_body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    api_key = _get_key(toolbench_rapidapi_key)

    h = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": host}
    if headers:
        h.update(headers)

    r = requests.request(
        method=method.upper(),
        url=url,
        headers=h,
        params=params,
        json=json_body,
        data=data_body,
        timeout=timeout,
    )

    try:
        body = r.json()
    except Exception:
        body = r.text

    return {"status_code": r.status_code, "json": body, "length": len(r.text)}


def inspect_response(name: str, out: Dict[str, Any]) -> None:
    print(f"\n--- {name} ---")
    print("Status:", out.get("status_code"))
    data = out.get("json")
    print("JSON type:", type(data).__name__)
    print("Response length:", out.get("length"))

    if isinstance(data, dict):
        print("Top-level keys:", list(data.keys())[:12])
    elif isinstance(data, list):
        print("Returned list length:", len(data))
        if data and isinstance(data[0], dict):
            print("First item keys:", list(data[0].keys())[:12])
    else:
        preview = str(data)
        print("Preview:", preview[:200] + ("..." if len(preview) > 200 else ""))


def most_similar_movies(
    movie_id_slug: str = "24168-titanic",
    run_id: Optional[str] = None,
    toolbench_rapidapi_key: str | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Calls Similar Movies API and writes a local beacon event (safe, hashed).
    """
    run_id = run_id or f"run_{int(time.time() * 1000)}"

    url = "https://similar-movies.p.rapidapi.com/similar"
    params = {"id": movie_id_slug}

    t0 = time.time()
    out = _request(
        "GET",
        url,
        "similar-movies.p.rapidapi.com",
        params=params,
        toolbench_rapidapi_key=toolbench_rapidapi_key,
    )
    latency_ms = int((time.time() - t0) * 1000)

    _beacon(
        {
            "ts": time.time(),
            "run_id": run_id,
            "tool": "most_similar_movies",
            "ok": (out.get("status_code") == 200),
            "status_code": out.get("status_code"),
            "movie_id_hash": _sha256(movie_id_slug),
            "latency_ms": latency_ms,
        }
    )

    return out


def main():
    out = most_similar_movies("24168-titanic", run_id="debug_run_1")
    inspect_response("Testing Similar Movies", out)
    print(f"[INFO] Beacon appended to: {BEACON_PATH}")


if __name__ == "__main__":
    main()