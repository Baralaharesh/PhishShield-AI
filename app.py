import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")
st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

user_url = st.text_input("URLని ఇక్కడ పేస్ట్ చేయండి:", placeholder="google.com")

if st.button("Analyze"):
    if not api_key:
        st.error("Please enter API Key!")
    else:
        try:
            # Server Side Details
            clean_url = user_url if '://' in user_url else 'http://' + user_url
            domain = urlparse(clean_url).netloc
            ip_addr = socket.gethostbyname(domain)
            st.success(f"Server Found! IP: {ip_addr}")

            # AI Side Details
            genai.configure(api_key=api_key)
            
            # ఇక్కడ మనం 404 ఎర్రర్ రాకుండా జాగ్రత్త పడుతున్నాం
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Analyze this URL for phishing risks: {user_url}. Give a report in Telugu."
            
            try:
                response = model.generate_content(prompt)
                st.write(response.text)
            except:
                # ఒకవేళ Flash పనిచేయకపోతే Pro ని వాడుతుంది
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Developed by Barla Hareesh")
