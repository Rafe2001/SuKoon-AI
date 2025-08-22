# 🧠 SuKoon-AI — Mental Health Therapist

SuKoon-AI is an AI-powered mental health assistant. It uses a **LangChain ReAct agent** (Gemini LLM) with tools for:

* 💬 expert-style Q\&A
* 📞 emergency escalation (Twilio)
* 📍 nearby therapist lookup (prompt-based)

---

## 🗂️ Project Structure

```
.
├── backend/
│   ├── __pycache__/
│   ├── tools/
│   │   ├── __pycache__/
│   │   ├── ask_tool.py
│   │   ├── emergency_call_tool.py
│   │   └── location_tool.py
│   ├── agent.py
│   ├── config.py              # loads Twilio / contact config (keep out of VCS)
│   ├── main.py                # FastAPI app
│   └── prompts.py
├── frontend/
│   └── front.py               # Streamlit UI
├── env/                       # local venv (don’t commit)
├── .env                       # secrets (don’t commit)
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 🧩 How it Works

```
[Streamlit UI] → calls → [FastAPI /ask]
                         ↓
                [LangChain ReAct Agent]
          ┌──────────────┼──────────────┐
          │              │              │
   ask_tool.py   emergency_call_tool.py  location_tool.py
       ↓                  ↓                    ↓
   Gemini LLM          Twilio API        Prompted lookup
```

* **Agent**: `backend/agent.py` (`create_react_agent`)
* **LLM**: Google Gemini via `langchain_google_genai`
* **Endpoint**: `POST /ask` in `backend/main.py`
* **Frontend**: `frontend/front.py` posts to `http://127.0.0.1:8000/ask`

---

## ⚙️ Setup

### 1) Environment

```bash
# create & activate a venv (any name is fine)
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 2) Install deps

Using **uv** (recommended if you have it):

```bash
uv sync
```

### 3) Secrets — create `.env` in project root

```
GOOGLE_API_KEY=your_gemini_key

# Optional (for emergency tool)
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
EMERGENCY_CONTACT=+91XXXXXXXXXX
```

> Keep `.env` and `backend/config.py` **out of git**.

---

## ▶️ Run

**Terminal 1 — backend (FastAPI):**

```bash
uvicorn backend.main:app --reload
# http://127.0.0.1:8000  |  docs: http://127.0.0.1:8000/docs
```

**Terminal 2 — frontend (Streamlit):**

```bash
streamlit run frontend/front.py
# http://localhost:8501
```

---

## 🔌 API Quick Test

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"message":"I feel anxious lately, what should I do?"}'
```

Response:

```json
{
  "message": "...assistant answer...",
  "tool_called": "ask_mental_health_specialist"   // or another tool
}
```

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Backend**: FastAPI
* **LLM/Agent**: LangChain + LangGraph (ReAct), Google Gemini
* **Telephony**: Twilio (emergency tool)
* **Env mgmt**: python-dotenv

---

## 🚧 Notes

* The **Emergency Call** tool requires valid Twilio credentials.
* Treat this as a **supportive assistant**, not a medical device. In emergencies, contact local services immediately.

