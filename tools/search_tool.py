# search_tool.py
import os
import requests


def web_search(query: str) -> str:
    """Useful for searching the web for current information."""
    api_key = os.getenv("SEARCHAPI_API_KEY")
    if not api_key:
        return "Error: SEARCHAPI_API_KEY environment variable not set."

    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract organic results
        results = data.get("organic_results", [])
        if not results:
            return "No results found."
            
        formatted_results = "\n\n".join(
            [f"Title: {res.get('title')}\nLink: {res.get('link')}\nSnippet: {res.get('snippet')}" 
             for res in results[:5]]
        )
        return formatted_results
    except Exception as e:
        return f"Search failed: {str(e)}"