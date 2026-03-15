import os
import requests

RAPIDAPI_HOST = "currency-converter-pro1.p.rapidapi.com"
ENDPOINT = "/convert"

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and str(toolbench_rapidapi_key).strip():
        return str(toolbench_rapidapi_key).strip()
    return os.getenv("RAPIDAPI_KEY") or os.getenv("TOOLBENCH_RAPIDAPI_KEY") or ""

import os
import requests

RAPIDAPI_HOST = "currency-converter-pro1.p.rapidapi.com"
ENDPOINT = "/convert"

def currency_converter_pro_latest_rates(
    from_currency: str,
    to_currency: str,
    amount: float,
    toolbench_rapidapi_key: str | None = None
):
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."

    url = f"https://{RAPIDAPI_HOST}{ENDPOINT}"

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        return {
            "error": "",
            "response": r.text,
            "status_code": r.status_code,
        }
    except Exception as e:
        return {"error": str(e), "response": ""}


if __name__ == "__main__":
    res = currency_converter_pro_latest_rates(
        from_currency="USD",
        to_currency="EUR",
        amount=100,
    )

    print(res)