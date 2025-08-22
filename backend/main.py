import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from backend.agent import agent_response, parse_response
from backend.prompts import agent_system_prompt


app = FastAPI()

class Query(BaseModel):
    message: str
    
@app.post("/ask")
async def query_ask(query: Query):
    """
    Endpoint to handle user queries.
    
    :param query: The user's query in JSON format.
    :return: A response message based on the user's query.   
    """
    try:
        query = query.message.strip()
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
        tool_called_name, final_response = parse_response(stream)
        return {
            "message": final_response,
            "tool_called": tool_called_name
            }  
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    

if __name__=="__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port=8000, reload=True)