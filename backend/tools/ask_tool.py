import sys
from groq import Groq
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def ask_llm(prompt: str, system_prompt: str)-> str:
    client = Groq()
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    top_p=0.9
    )
    return chat_completion.choices[0].message.content


# print(ask_llm("What's your name?", system_prompt))