import streamlit as st
from frontend.i18n.translations import translations

def get_text(key):
    lang = st.session_state.get("language", "en")
    return translations.get(lang, translations["en"]).get(key, key)

def language_selector():
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    langs = {"en": "🌐 English", "hi": "🌐 हिन्दी", "te": "🌐 తెలుగు"}
    
    selected_lang = st.sidebar.selectbox(
        get_text("lang_selector"),
        options=list(langs.keys()),
        format_func=lambda x: langs[x],
        index=list(langs.keys()).index(st.session_state.language)
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
