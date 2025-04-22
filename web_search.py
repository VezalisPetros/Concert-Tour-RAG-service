import os
from serpapi import GoogleSearch

from dotenv import load_dotenv

load_dotenv()

def extract_artist_name(query: str) -> str:
    # Grab first capitalized words (naive artist extraction)
    words = query.split()
    capitalized = [word for word in words if word[0].isupper() and word.lower() not in ["Is", "Are", "Where", "When", "Will"]]
    return " ".join(capitalized[:2]) if capitalized else query

def search_artist_tour(user_query: str) -> str:
    artist = extract_artist_name(user_query)
    query = f"{artist} 2025 2026 concert tour schedule"
    #api_key = os.getenv("SERPAPI_KEY")
    api_key="e8263931862b6ec52894b8c8f24d45038dc2fc1e5fd05b2cb92cdd57373ed64f"

    if not api_key:
        return "❌ SerpAPI key not found in .env"

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        return f"❌ Web search failed: {str(e)}"

    if "organic_results" not in results:
        return "🤔 Couldn't find relevant info online."

    snippets = [r.get("snippet", "") for r in results["organic_results"][:3]]
    filtered = [s for s in snippets if "2025" in s or "2026" in s]

    if not filtered:
        return "🔍 No clear tour details found online."

    return "🌐 Retrieved via web search\n\n" + "\n".join(filtered)
