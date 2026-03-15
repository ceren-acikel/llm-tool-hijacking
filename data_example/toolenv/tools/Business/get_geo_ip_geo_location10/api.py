import os
import requests

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()

def get_geo_ip_geo_location10(ip: str, toolbench_rapidapi_key: str | None = None):

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."
    
    url = "https://ip-geo-location10.p.rapidapi.com/ip"
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "ip-geo-location10.p.rapidapi.com"
    }
    params = {"ip": ip}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    ip = "20.207.73.82"
    print(get_geo_ip_geo_location10(ip))