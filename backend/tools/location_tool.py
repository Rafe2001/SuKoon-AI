from langchain_tavily import TavilySearch, TavilyMap
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "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")

def nearby_location_therapist(location: str):
    """
    Fetch top 3 therapists/psychologists nearby the given location using Tavily Search API.
    """
    query = f"Provide me the details of Top psychologists or therapists near {location}."
    
    search = TavilySearch(
        max_results=3
    )
    response = search.invoke({"query": query})
    results = []
    for res in response["results"]:
        results.append({
            "name": res.get("title"),
            "address": res.get("content").split(";")[0],  # first part usually has address/clinic info
            "contact_info": ";".join(res.get("content").split(";")[1:]),  # rest can include phone, details
            "url": res.get("url")
        })
    return results

print(nearby_location_therapist("New York"))