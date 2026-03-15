import os
import requests

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()

def real_time_finance_data(
    query: str,
    page: int = 1,
    country: str = "US",
    toolbench_rapidapi_key: str | None = None
):
    """
    Real-Time Finance Data (RapidAPI)
    """
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."

    url = "https://real-time-finance-data.p.rapidapi.com/search"
    querystring = {"query": query, "page": page, "country": country}

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=20)
    try:
        return response.json()
    except:
        return response.text
    

if __name__ == "__main__":
    out2 = real_time_finance_data("Apple stock", page=1, country="US")
    print(out2 if isinstance(out2, str) else str(out2)[:2000])