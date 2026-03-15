import os
import requests

RAPIDAPI_HOST = "financial-modeling-prep.p.rapidapi.com"
ENDPOINT_TEMPLATE = "/v3/enterprise-values/{symbol}"

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return (
        os.getenv("RAPIDAPI_KEY")
        or os.getenv("TOOLBENCH_RAPIDAPI_KEY")
        or ""
    )

def enterprise_values(
        symbol: str = "AAPL",
        period: str = "quarter",
        toolbench_rapidapi_key: str | None = None):
    """
    Fetch enterprise values for a stock.

    Query parameters:
        - symbol (e.g., "AAPL")
        - period ("quarter" or "annual")
    """

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": "missing rapidapi key", "response": ""}

    endpoint = ENDPOINT_TEMPLATE.format(symbol=symbol)
    url = f"https://{RAPIDAPI_HOST}{endpoint}"

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    params = {
        "period": period
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
            "parsed": parsed
        }

    except Exception as e:
        return {"error": str(e), "response": ""}


if __name__ == "__main__":
    res = enterprise_values(symbol="AAPL", period="quarter")
    print(res)