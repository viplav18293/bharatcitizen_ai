import streamlit as st
import requests
import os
import subprocess
import sys
import time
from frontend.i18n.translator import language_selector, get_text

# Configuration
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")


def backend_is_available() -> bool:
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False


def ensure_backend_running() -> bool:
    if backend_is_available():
        return True

    if API_URL not in {"http://localhost:8000", "http://127.0.0.1:8000"}:
        return False

    if not st.session_state.get("backend_autostart_attempted"):
        st.session_state.backend_autostart_attempted = True
        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=BACKEND_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )

    for _ in range(20):
        if backend_is_available():
            return True
        time.sleep(0.5)

    return False

st.set_page_config(page_title="BharatAI Citizen Assistant", page_icon="🇮🇳", layout="wide")

# Sidebar
language_selector()
st.sidebar.title("Official Links")
st.sidebar.write("Get help from official sources:")
st.sidebar.markdown("""
- [UIDAI (Aadhaar)](https://uidai.gov.in)
- [NTA (Exams)](https://nta.ac.in)
- [Passport Seva](https://passportindia.gov.in)
- [India Code (Laws)](https://indiacode.nic.in)
- [PM Kisan](https://pmkisan.gov.in)
""")

st.title(get_text("title"))
st.write("Your AI-powered copilot for Indian government services.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input(get_text("ask_input")):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(get_text("thinking")):
            try:
                if not ensure_backend_running():
                    raise RuntimeError("Backend is not running on port 8000.")

                # Backend endpoint: /api/v1/chat
                response = requests.post(f"{API_URL}/api/v1/chat", json={
                    "message": prompt, 
                    "history": [],
                    "language": st.session_state.get("language", "en")
                })
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    st.markdown(answer)
                    
                    if portal_link := data.get("official_portal_link"):
                        st.link_button(get_text("visit_portal"), portal_link)
                        
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend at {API_URL}: {e}")
                st.info("Ensure the FastAPI backend is running.")
