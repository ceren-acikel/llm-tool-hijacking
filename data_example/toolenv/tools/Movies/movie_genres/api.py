import os
import requests

DEFAULT_TIMEOUT = int(os.getenv("RAPIDAPI_TIMEOUT_SEC", "30"))


def _get_key(toolbench_rapidapi_key: str | None):
    k = (toolbench_rapidapi_key or os.getenv("RAPIDAPI_KEY") or "").strip()
    if not k:
        raise RuntimeError("Missing RAPIDAPI_KEY (env) and no toolbench_rapidapi_key provided.")
    return k


def _request(
    method: str,
    url: str,
    host: str,
    *,
    toolbench_rapidapi_key: str | None = None,
    params=None,
    json_body=None,
    data_body=None,
    headers=None,
    timeout: int = DEFAULT_TIMEOUT,
):
    api_key = _get_key(toolbench_rapidapi_key)

    h = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": host,
    }
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


def inspect_response(name: str, out: dict):
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


def movie_genres(toolbench_rapidapi_key: str | None = None, **kwargs):
    url = "https://advanced-movie-search.p.rapidapi.com/genre/movie/list"
    return _request(
        "GET",
        url,
        "advanced-movie-search.p.rapidapi.com",
        toolbench_rapidapi_key=toolbench_rapidapi_key,
    )


if __name__ == "__main__":
    inspect_response("Testing Genres", movie_genres())