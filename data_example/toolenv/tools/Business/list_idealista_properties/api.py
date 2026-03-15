import os
import requests


def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()


def list_idealista_properties(toolbench_rapidapi_key: str | None = None):
    
    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."
    
    url = "https://idealista2.p.rapidapi.com/properties/list"

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "idealista2.p.rapidapi.com"
    }

    params = {
        "numPage": 1,
        "maxItems": 40,
        "locationId": "0-EU-IT-RM-01-001-097-09-003",
        "sort": "asc",
        "locale": "en",
        "operation": "rent",
        "country": "it"
    }

    response = requests.get(url, headers=headers, params=params)

    return {
        "status_code": response.status_code,
        "json": response.json(),
        "length": len(response.text)
    }


if __name__ == "__main__":
    idealista = list_idealista_properties()
    print("Idealista status:", idealista["status_code"])
    print("Items returned:", len(idealista["json"].get("elementList", [])))