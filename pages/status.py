import streamlit as st
import os
import sys

# Ensure backend directory is in path
BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.services.rag_service import rag_service

st.set_page_config(page_title="BharatAI System Status", page_icon="⚙️")

st.title("System Status")

def check_backend():
    try:
        rag_service.initialize_once()
        health = rag_service.get_health()
        return health["status"] in ["online", "degraded"], health
    except Exception as e:
        return False, {"error": str(e)}

is_healthy, status = check_backend()

if is_healthy:
    st.success("Backend Reachable (In-Process)")
    st.json(status)
else:
    st.error("Backend Offline or Degraded")
    st.write("Could not initialize the internal backend services.")

st.subheader("Components")
st.write("Running directly in Streamlit (No external API calls)")
