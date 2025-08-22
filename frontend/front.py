# Step1: Setup Streamlit
import streamlit as st
import requests


BACKEND_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="SuKoon-AI", 
                   layout="wide")
st.title("SuKoon-AI: A Mental Health Therapist")

# Initialize chat history in chat session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
# Step2: User is able to ask the questions
user_input = st.text_input("Ask a question:", key="user_input")
if user_input:
    st.session_state.chat_history.append({"role": "user", 
                                          "content": user_input})
    response = requests.post(
        BACKEND_URL, json={"message": user_input}
    ).json()  # Assuming the backend returns a JSON response with the answer
    #response = "I'm here to help you please ask me any query."
    st.session_state.chat_history.append({"role": "assistant", 
                                          "content": f"{response['message']}\n, Tool called: {response['tool_called']}"})
    
# Step3: Show response from backend

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.write(f"**User:** {msg['content']}")
    else:
        st.write(f"**Assistant:** {msg['content']}")
    