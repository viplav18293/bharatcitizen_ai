import streamlit as st
import requests
import os
from frontend.i18n.translator import language_selector, get_text

# Configuration
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
