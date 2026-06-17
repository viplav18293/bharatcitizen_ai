import streamlit as st
import requests
import os

st.set_page_config(page_title="BharatAI System Status", page_icon="⚙️")

st.title("System Status")

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

def check_backend():
    try:
        response = requests.get(f"{backend_url}/api/v1/health/", timeout=2)
        return response.status_code == 200, response.json()
    except:
        return False, None

is_healthy, status = check_backend()

if is_healthy:
    st.success("Backend Reachable")
    st.json(status)
else:
    st.error("Backend Offline")
    st.write(f"Could not connect to {backend_url}. Ensure the backend is running.")

st.subheader("Components")
st.write(f"Backend URL: {backend_url}")
