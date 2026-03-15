import os
import requests


def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return os.environ.get("RAPIDAPI_KEY") or "".strip()

def real_time_amazon_search(
    query: str="iphone",
    page: int = 1,
    country: str = "US",
    toolbench_rapidapi_key: str | None = None
):
    """
    Search products on Amazon (Real-Time Amazon Data API)
    """

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."
    
    querystring = {
        "query": query,
        "page": page,
        "country": country
    }

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


if __name__ == "__main__":

    out1 = real_time_amazon_search("iphone", page=1, country="US")
    print(out1 if isinstance(out1, str) else str(out1)[:2000])