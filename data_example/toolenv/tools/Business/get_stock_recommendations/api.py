import os
import requests

RAPIDAPI_HOST = "yahoo-finance-real-time1.p.rapidapi.com"
ENDPOINT = "/stock/get-recommendations"

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return (
        os.getenv("RAPIDAPI_KEY")
        or ""
    )

def get_stock_recommendations(
        symbols: str = "GOOG",
        toolbench_rapidapi_key: str | None = None):
    """
    Required parameter:
        symbols (STRING)
    Example:
        symbols="GOOG"
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
        "symbols": symbols,
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)

        parsed = None
        try:
            parsed = r.json()
        except Exception:
            pass

        return {
            "error": "",
            "status_code": r.status_code,
            "response": r.text,
            "parsed": parsed,
        }

    except Exception as e:
        return {"error": str(e), "response": ""}


if __name__ == "__main__":
    res = get_stock_recommendations(symbols="GOOG")
    print("status_code:", res.get("status_code"))
    print("parsed:", res.get("parsed"))