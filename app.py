import streamlit as st
import os
import sys
import asyncio
from loguru import logger

# Ensure backend directory is in path before importing backend modules
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from frontend.i18n.translator import language_selector, get_text
from backend.services.adk_agents import citizen_assistant_agent
from backend.services.rag_service import rag_service
from backend.schemas.chat import Message as BackendMessage

st.set_page_config(page_title="BharatAI Citizen Assistant", page_icon="🇮🇳", layout="wide")

@st.cache_resource(show_spinner="Initializing AI Engine...")
def init_backend():
    # Initialize RAG in-process
    rag_service.initialize_once()
    
    # Self Test
    test_passed = False
    error_msg = ""
    try:
        if rag_service.ready:
            # Test retrieval to verify vector DB is working
            docs = rag_service.retrieve_documents("Aadhaar", k=1)
            test_passed = True
        else:
            error_msg = "RAG service failed to initialize."
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Startup validation failed: {e}")
        
    return rag_service.get_health(), test_passed, error_msg

status, test_passed, error_msg = init_backend()

# Sidebar
language_selector()

st.sidebar.title("System Status")
if test_passed:
    st.sidebar.success("✅ System Online (In-Process)")
else:
    st.sidebar.error("⚠️ System Degraded")
    st.sidebar.caption(error_msg)

st.sidebar.write("### Diagnostics")
st.sidebar.write(f"- **Embeddings:** {'✅' if status['components']['embeddings'] else '❌'}")
st.sidebar.write(f"- **Vector DB:** {'✅' if status['components']['vectordb'] else '❌'}")
st.sidebar.write(f"- **LLM:** {'✅' if status['components']['llm'] else '❌'}")
st.sidebar.write(f"- **Documents Indexed:** {status['stats'].get('document_count', 0)}")

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
                # Convert history to backend schemas
                history = [
                    BackendMessage(role=m["role"], content=m["content"]) 
                    for m in st.session_state.messages[:-1]
                ]
                
                # Execute AI/RAG directly in process (No localhost API calls)
                response = asyncio.run(citizen_assistant_agent.query(
                    message=prompt,
                    history=history,
                    language=st.session_state.get("language", "en"),
                    session_id="streamlit_session"
                ))
                
                st.markdown(response.answer)
                
                if response.official_portal_link:
                    st.link_button(get_text("visit_portal"), response.official_portal_link)
                    
                st.session_state.messages.append({"role": "assistant", "content": response.answer})
            except Exception as e:
                logger.error(f"Internal error during chat generation: {e}")
                st.error("System temporarily unavailable. Please try again.")
