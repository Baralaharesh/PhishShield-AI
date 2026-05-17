import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")
st.title("🛡️ PhishShield: AI Analyzer")
st.markdown("---")

# సైడ్‌బార్
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# యూజర్ ఇన్‌పుట్
user_url = st.text_input("URLని ఇక్కడ పేస్ట్ చేయండి:", placeholder="google.com")

if st.button("Analyze"):
    if not api_key:
        st.error("ముందుగా API Keyని ఎంటర్ చేయండి!")
    else:
        try:
            # సర్వర్ వివరాలు
            clean_url = user_url if '://' in user_url else 'http://' + user_url
            domain = urlparse(clean_url).netloc
            ip_addr = socket.gethostbyname(domain)
            st.success(f"✅ Server Found! IP: {ip_addr}")

            # AI విశ్లేషణ
            genai.configure(api_key=api_key)
            
            # ఇక్కడ 'models/' లేకుండా నేరుగా పేరు ఇవ్వాలి
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Analyze this URL for phishing risks: {user_url}. Give verdict and tips in Telugu."
            response = model.generate_content(prompt)
            
            st.markdown("### 🤖 AI భద్రతా నివేదిక")
            st.info(response.text)

        except Exception as e:
            # ఒకవేళ flash పనిచేయకపోతే pro ని ప్రయత్నిస్తుంది
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Analyze: {user_url} in Telugu.")
                st.info(response.text)
            except:
                st.error(f"Error: {e}")

st.caption("Developed by Barla Hareesh")
