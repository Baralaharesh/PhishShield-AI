import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")
st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

# సైడ్‌బార్
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# యూజర్ ఇన్‌పుట్
user_url = st.text_input("URLని ఇక్కడ పేస్ట్ చేయండి:", placeholder="google.com")

if st.button("Analyze"):
    if not api_key:
        st.error("ముందుగా API Keyని ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("URL ఎంటర్ చేయలేదు!")
    else:
        try:
            with st.spinner('సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                # URL క్లీనింగ్
                clean_url = user_url if '://' in user_url else 'http://' + user_url
                domain = urlparse(clean_url).netloc
                ip_addr = socket.gethostbyname(domain)
                geo = requests.get(f"https://ipapi.co/{ip_addr}/json/").json()
                
                st.success("✅ సర్వర్ వివరాలు లభించాయి!")
                st.info(f"**IP:** {ip_addr} | **Country:** {geo.get('country_name')} | **ISP:** {geo.get('org')}")

            # AI విశ్లేషణ
            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                genai.configure(api_key=api_key)
                
                # మోడల్ పేరును అత్యంత జాగ్రత్తగా ఇస్తున్నాం
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Analyze this URL for phishing risks: {user_url}. Give verdict and tips in Telugu."
                
                response = model.generate_content(prompt)
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Developed by Barla Hareesh")
