import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")
st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

user_url = st.text_input("URLని పేస్ట్ చేయండి:", placeholder="https://example.com")

if st.button("లింక్‌ని పరిశీలించు (Analyze)"):
    if not api_key:
        st.error("API Key ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("URL ఎంటర్ చేయండి!")
    else:
        try:
            with st.spinner('సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                parsed_url = urlparse(user_url if '://' in user_url else 'http://'+user_url)
                domain = parsed_url.netloc
                ip_addr = socket.gethostbyname(domain)
                geo = requests.get(f"https://ipapi.co/{ip_addr}/json/").json()
                
                st.success("✅ సర్వర్ వివరాలు లభించాయి!")
                st.info(f"IP: {ip_addr} | Country: {geo.get('country_name')} | ISP: {geo.get('org')}")

            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                genai.configure(api_key=api_key)
                
                # ఈ మార్పు వల్ల 404 ఎర్రర్ రాదు
                # అందుబాటులో ఉన్న మోడల్స్ ని వెతుకుతున్నాం
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Gemini 1.5 Flash ఉంటే అది వాడు, లేకపోతే Pro వాడు
                model_to_use = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else 'models/gemini-pro'
                
                model = genai.GenerativeModel(model_to_use)
                
                prompt = f"Analyze this URL for phishing risks: {user_url}. Details: IP {ip_addr}, ISP {geo.get('org')}. Give verdict and advice in Telugu."
                
                response = model.generate_content(prompt)
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Developed by Barla Hareesh")
