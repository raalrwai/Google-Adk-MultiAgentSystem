import os
import requests
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(r"C:\Users\Rami Alrwais\Desktop\GoogleADK\.env")  # Adjust if needed
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
CSE_ID = os.getenv("GOOGLE_SEARCH_CSE_ID")


def google_search(query: str, num_results: int = 5) -> dict:
    """
    Perform a Google Custom Search.
    Returns structured dict similar to stock price tool:
    {
        ok: True/False,
        query: str,
        results: list of {title, link, snippet},
        error: str (optional)
    }
    """
    if not API_KEY or not CSE_ID:
        return {
            "ok": False,
            "query": query,
            "error": "API_KEY or CSE_ID not set correctly."
        }

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        results = [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            } for item in items
        ]

        return {
            "ok": True,
            "query": query,
            "results": results
        }

    except requests.exceptions.RequestException as e:
        return {
            "ok": False,
            "query": query,
            "error": str(e)
        }


if __name__ == "__main__":
    query = input("Enter search query: ").strip()
    if not query:
        print({"ok": False, "error": "Query cannot be empty."})
    else:
        output = google_search(query)
        print(output)
