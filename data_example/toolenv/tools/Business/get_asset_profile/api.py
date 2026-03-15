import os
import requests

RAPIDAPI_HOST = "realtime-stock-data.p.rapidapi.com"
ENDPOINT = "/finance-analytics/aapl"

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return os.getenv("RAPIDAPI_KEY") or ""

def get_asset_profile(ticker: str = "AAPL", toolbench_rapidapi_key: str | None = None):
    """
    Auto-generated ToolBench wrapper.
    No query params required for this endpoint.
    """
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": "missing rapidapi key", "response": ""}

    url = f"https://{RAPIDAPI_HOST}{ENDPOINT}"

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)
        return {
            "error": "",
            "response": r.text,
            "status_code": r.status_code
        }
    except Exception as e:
        return {"error": str(e), "response": ""}
    
if __name__ == "__main__":
    res = get_asset_profile(ticker="AAPL")
    print(res)