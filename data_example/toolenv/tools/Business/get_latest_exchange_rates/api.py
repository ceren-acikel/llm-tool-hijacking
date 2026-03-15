import os
import requests

RAPIDAPI_HOST = "currency-exchange-rate-api1.p.rapidapi.com"
ENDPOINT = "/latest"

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return os.getenv("RAPIDAPI_KEY") or ""

def get_latest_exchange_rates(toolbench_rapidapi_key: str | None = None, **kwargs):
    """
    ToolBench wrapper.
    kwargs -> query params (e.g., base="EUR", symbols="USD,GBP", etc.)
    """
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": "missing rapidapi key", "response": ""}

    url = f"https://{RAPIDAPI_HOST}{ENDPOINT}"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    params = {k: v for k, v in kwargs.items() if v is not None}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        return {
            "error": "",
            "response": r.text,
            "status_code": r.status_code
        }
    except Exception as e:
        return {"error": str(e), "response": ""}

if __name__ == "__main__":
    print(get_latest_exchange_rates(base="EUR"))