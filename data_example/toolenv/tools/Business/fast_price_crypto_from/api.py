import os
import requests

RAPIDAPI_HOST = "fast-price-exchange-rates.p.rapidapi.com"
ENDPOINT = "/api/v1/convert-rates/fiat/from"

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return os.getenv("RAPIDAPI_KEY") or ""

def fast_price_crypto_from(
    detailed: str = "false",
    currency: str = "USD",
    toolbench_rapidapi_key: str | None = None):
    """
    Auto-generated ToolBench wrapper.
    Example params:
        detailed=false
        currency=USD
    """
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": "missing rapidapi key", "response": ""}

    url = f"https://{RAPIDAPI_HOST}{ENDPOINT}"

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    params = {
        "detailed": detailed,
        "currency": currency,
    }

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
    res = fast_price_crypto_from(
        detailed="false",
        currency="USD"
    )
    print(res)