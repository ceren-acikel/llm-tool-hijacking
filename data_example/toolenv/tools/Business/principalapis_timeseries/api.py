import os
import requests

RAPIDAPI_HOST = "currency-conversion-and-exchange-rates.p.rapidapi.com"
ENDPOINT = "/timeseries"   # time-series endpoint

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return os.getenv("RAPIDAPI_KEY") or os.getenv("TOOLBENCH_RAPIDAPI_KEY") or ""

def principalapis_timeseries(
    start_date: str,
    end_date: str,
    base: str = "USD",
    symbols: str = "EUR,GBP,TRY",
    toolbench_rapidapi_key: str | None = None,
):
    """
    Time-Series — Track how rates changed over any custom date range.

    Required:
      - start_date (YYYY-MM-DD)
      - end_date   (YYYY-MM-DD)

    Optional:
      - base    (default: USD)
      - symbols (default: None)  e.g. "EUR,GBP,TRY"
    """

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {"error": "missing rapidapi key", "response": ""}

    if not start_date or not end_date:
        return {"error": "missing required parameter(s): start_date, end_date", "response": ""}

    url = f"https://{RAPIDAPI_HOST}{ENDPOINT}"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "base": base,
    }

    if symbols and symbols != "None":
        params["symbols"] = symbols

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        return {"error": "", "response": r.text, "status_code": r.status_code}
    except Exception as e:
        return {"error": str(e), "response": ""}


if __name__ == "__main__":
    res = principalapis_timeseries(
        start_date="2025-01-01",
        end_date="2025-01-10",
        base="USD",
        symbols="EUR,TRY",
    )
    print(res)