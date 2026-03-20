import os

try:
    import streamlit as st
    key = st.secrets.get("GROQ_API_KEY", None)
    if key:
        GROQ_API_KEY = key
    else:
        raise KeyError("Not in secrets")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")