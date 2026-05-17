import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")
st.title("🛡️ PhishShield: AI Analyzer")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
user_url = st.text_input("URLని ఇక్కడ పేస్ట్ చేయండి:", placeholder="google.com")

if st.button("Analyze"):
    if not api_key:
        st.error("API Key ఎంటర్ చేయండి!")
    else:
        try:
            # Server Info
            clean_url = user_url if '://' in user_url else 'http://' + user_url
            domain = urlparse(clean_url).netloc
            ip_addr = socket.gethostbyname(domain)
            st.success(f"✅ Server Found! IP: {ip_addr}")

            # AI Analysis
            genai.configure(api_key=api_key)
            # ఇక్కడ 'models/' లేకుండా నేరుగా పేరు ఇస్తున్నాం
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(f"Analyze this URL for phishing: {user_url}. Give verdict in Telugu.")
            st.info(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
