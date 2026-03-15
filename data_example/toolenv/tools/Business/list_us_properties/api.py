import os
import requests

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()


def list_us_properties(postal_code="90004", toolbench_rapidapi_key: str | None = None):
    
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."
    
    url = "https://realty-in-us.p.rapidapi.com/properties/v3/list"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "realty-in-us.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    payload = {
        "limit": 200,
        "offset": 0,
        "postal_code": postal_code,
        "status": ["for_sale", "ready_to_build"],
        "sort": {"direction": "desc", "field": "list_date"}
    }

    r = requests.post(url, headers=headers, json=payload)
    return {
        "status_code": r.status_code,
        "json": r.json(),
        "length": len(r.text)
    }


if __name__ == "__main__":
    realty = list_us_properties()
    print("Realty status:", realty["status_code"])
    print("Realty keys:", list(realty["json"].keys())[:10])