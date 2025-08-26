from langchain.agents import tool
import os
from tools.ask_tool import ask_llm
from prompts import system_prompt_tool, agent_system_prompt
from tools.emergency_call_tool import emergency_call
from tools.location_tool import nearby_location_therapist
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from config import TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, TWILIO_SID, EMERGENCY_CONTACT

load_dotenv()

@tool 
def ask_mental_health_specialist(
    query: str,
    system_prompt_tool: str
) -> str:
    """
    Use this tool to ask a mental health specialist about your query.
    
    Args:
        query (str): The user's question or statement.
        system_prompt_tool (str): The system prompt for the mental health specialist.
        
    Returns:
        str: The response from the mental health specialist.
    """
    return ask_llm(query, system_prompt_tool)

# Second Tool: Emergency Call 

@tool
def Emergency_call_tool():
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    return emergency_call()


# 3rd tool: Location of the psycologist
@tool
def Find_therapist(location: str)-> str:
    """
    Use this tool to find nearby locations of psychologists based on the user's location.
    Based on the user's input location, this tool will return a list of nearby psychologists.
    """
    return nearby_location_therapist(location)


tools = [
         ask_mental_health_specialist, 
         Emergency_call_tool, 
         Find_therapist
        ]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    api_key=os.getenv("GOOGLE_API_KEY")
)

agent_response = create_react_agent(llm, tools=tools)

def parse_response(stream):
    tool_called_name = None
    final_response = None
    
    for s in stream:
        tool_data = s.get("tools")
        if tool_data:
            tool_messages = tool_data.get("messages")
            for msg in tool_messages:
                tool_called_name = getattr(msg, "name", None)
        
        agent_data = s.get("agent")
        if agent_data:
            messages = agent_data.get("messages")
            for msg in messages:
                final_response = getattr(msg, "content", None)            
                        
    return tool_called_name, final_response


if __name__ == "__main__":
    try:
        while True:
            query = input("Enter the query: ")
            print(f"Recieved user input query: {query}")
            inputs = {
                "messages": [
                    {
                    "role": "system",
                    "content": agent_system_prompt
                    },
                    {
                    "role": "user",
                    "content": query
                    }
                ]
        }
            stream = agent_response.stream(inputs, stream_mode = "updates")
            # for response in stream:
            #     print(response) 
            tool_called_name, final_response = parse_response(stream)
            print(f"Tool called: {tool_called_name}")
            print(f"Final response: {final_response}")
            
            
    except Exception as e:
        print(f"An error occurred: {e}")

