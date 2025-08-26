from langchain_tavily import TavilySearch, TavilyMap
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv

load_dotenv()


os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


def nearby_location_therapist(location: str) -> str:
    """
    Fetch top 3 therapists/psychologists nearby the given location using Tavily Search API.
    
    Args:
        location (str): The location to search for therapists
        
    Returns:
        str: Formatted string with therapist information
    """
    try:
        print(f"DEBUG: Starting search for location: {location}")
        
        # Validate input
        if not location or not location.strip():
            return "Please provide a valid location to search for therapists."
        
        query = f"Top psychologists therapists mental health professionals near {location} contact details address phone"
        print(f"DEBUG: Search query: {query}")
        
        # Initialize search
        search = TavilySearch(max_results=3)
        
        # Execute search and get response
        response = search.invoke({"query": query})
        print(f"DEBUG: Raw response type: {type(response)}")
        print(f"DEBUG: Raw response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
        
        # FIXED: Proper response handling
        if not response:
            return f"No therapists found near {location}. Please try a different location."
        
        if isinstance(response, dict) and "results" in response:
            results = response["results"]
        elif isinstance(response, list):
            results = response
        else:
            print(f"DEBUG: Unexpected response format: {response}")
            return f"Unable to process search results for {location}. Please try again."
        
        if not results:
            return f"No therapists found near {location}. Please try searching for a nearby city."
        
        print(f"DEBUG: Found {len(results)} results")
        
        # Format the results
        formatted_output = f"Here are mental health professionals near {location}:\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "Mental Health Professional") if isinstance(result, dict) else str(result)
            content = result.get("content", "No details available") if isinstance(result, dict) else ""
            url = result.get("url", "") if isinstance(result, dict) else ""
            
            # Clean up content
            if content:
                # Remove excessive whitespace and format nicely
                content = content.replace("\n", " ").replace("  ", " ").strip()
                if len(content) > 300:
                    content = content[:300] + "..."
            
            formatted_output += f"{i}. {title}\n"
            if content:
                formatted_output += f"   Details: {content}\n"
            if url:
                formatted_output += f"   Website: {url}\n"
            formatted_output += "\n"
        
        formatted_output += "Please verify contact information and check availability before making appointments.\n"
        formatted_output += "For immediate mental health crisis support, contact local emergency services."
        
        print(f"DEBUG: Returning formatted output ({len(formatted_output)} characters)")
        return formatted_output
        
    except Exception as e:
        error_msg = f"Error searching for therapists: {str(e)}"
        print(f"DEBUG: Exception occurred: {error_msg}")
        import traceback
        traceback.print_exc()
        return f"I'm sorry, I encountered an issue while searching for therapists near {location}. Please try again or contact local mental health services."


