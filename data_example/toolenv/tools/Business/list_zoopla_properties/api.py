import os
import requests


def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()


def list_zoopla_properties(toolbench_rapidapi_key: str | None = None):
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."

    url = "https://zoopla.p.rapidapi.com/properties/v2/list"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "zoopla.p.rapidapi.com"
    }
    params = {
        "locationValue": "Oxford, Oxfordshire",
        "locationIdentifier": "oxford",
        "category": "residential",
        "furnishedState": "Any",
        "sortOrder": "newest_listings",
        "page": 1
    }

    r = requests.get(url, headers=headers, params=params)
    return {
        "status_code": r.status_code,
        "json": r.json(),
        "length": len(r.text)
    }

if __name__ == "__main__":

        zoopla = list_zoopla_properties()
        print("Zoopla status:", zoopla["status_code"])
        print("Zoopla keys:", list(zoopla["json"].keys())[:10])
