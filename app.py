import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# ... (పాత కోడ్ అలాగే ఉంచు) ...

if st.button("Analyze"):
    # ... (సర్వర్ వివరాల కోడ్ అలాగే ఉంచు) ...
    
    try:
        genai.configure(api_key=api_key)
        
        # ఇక్కడ మార్పు చేయాలి: 
        # పాత పద్ధతి: model = genai.GenerativeModel('gemini-pro')
        # కొత్త పద్ధతి (ఇది వాడు):
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        prompt = f"Analyze this URL for phishing risks: {user_url}. Give a report in Telugu."
        
        # ఇక్కడ కూడా చిన్న మార్పు:
        response = model.generate_content(prompt)
        st.write(response.text)
        
    except Exception as ai_error:
        # ఒకవేళ 1.5-flash రాకపోతే, ఇది ప్రయత్నించు
        try:
            model = genai.GenerativeModel(model_name="gemini-1.0-pro")
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")
