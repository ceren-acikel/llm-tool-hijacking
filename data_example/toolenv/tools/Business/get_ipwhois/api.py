import os
import requests

def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()
    
def get_ipwhois(ip: str, toolbench_rapidapi_key: str | None = None):

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return "ERROR: Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."

    url = "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "ip-geolocation-ipwhois-io.p.rapidapi.com",
    }

    params = {"ip": ip} 

    r = requests.get(url, headers=headers, params=params, timeout=30)

    print("status:", r.status_code)
    print("body:", r.text[:300])

    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    ip = "20.207.73.82"
    print(get_ipwhois(ip))