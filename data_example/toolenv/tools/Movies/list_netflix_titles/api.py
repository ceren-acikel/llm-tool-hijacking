import os
import requests

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") or ""
DEFAULT_TIMEOUT = int(os.getenv("RAPIDAPI_TIMEOUT_SEC", "30"))


def _request(method: str, url: str, host: str, *, params=None, json_body=None, data_body=None, headers=None, timeout=DEFAULT_TIMEOUT):
    h = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": host}
    if headers:
        h.update(headers)

    r = requests.request(
        method=method.upper(),
        url=url,
        headers=h,
        params=params,
        json=json_body,
        data=data_body,
        timeout=timeout
    )

    try:
        body = r.json()
    except Exception:
        body = r.text

    return {"status_code": r.status_code, "json": body, "length": len(r.text)}


def inspect_response(name: str, out: dict):
    """
    Safe debug print for dict/list responses.
    """
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


def list_netflix_titles(
    page=1,
    country="US",
    type="movie",
    genre=None,
    toolbench_rapidapi_key: str | None = None
):
    url = "https://netflix-movies-and-tv-shows1.p.rapidapi.com/list"
    toolbench_rapidapi_key = RAPIDAPI_KEY

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": toolbench_rapidapi_key
    }

    form_data = {
        "page": page,
        "country": country,
        "type": type
    }

    if genre:
        form_data["genre"] = genre

    return _request(
        method="POST",
        url=url,
        host="netflix-movies-and-tv-shows1.p.rapidapi.com",
        data_body=form_data,
        headers=headers
    )


if __name__ == "__main__":
    inspect_response("Testing Netflix List", list_netflix_titles(page=1, country="US", type="movie"))