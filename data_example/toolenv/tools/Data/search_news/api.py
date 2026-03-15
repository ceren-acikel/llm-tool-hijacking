import os
import requests


def _get_key(toolbench_rapidapi_key: str | None):
    if toolbench_rapidapi_key and toolbench_rapidapi_key.strip():
        return toolbench_rapidapi_key.strip()
    return (os.environ.get("RAPIDAPI_KEY") or "").strip()


def search_news(
    query: str,
    limit: int = 10,
    country: str = "US",
    lang: str = "en",
    toolbench_rapidapi_key: str | None = None
):
    """
    Search real-time news.
    query: REQUIRED non-empty string
    """

    if not query or not str(query).strip():
        return {
            "error": "Missing required parameter: query (non-empty string required)."
        }

    key = _get_key(toolbench_rapidapi_key)
    if not key:
        return {
            "error": "Missing RAPIDAPI_KEY (set env var or pass toolbench_rapidapi_key)."
        }

    url = "https://real-time-news-data.p.rapidapi.com/search"

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "real-time-news-data.p.rapidapi.com"
    }

    params = {
        "query": query.strip(),
        "limit": limit,
        "time_published": "anytime",
        "country": country,
        "lang": lang
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


if __name__ == "__main__":
    news = search_news(query="OpenAI model release")
    print(news)