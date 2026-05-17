import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# 1. వెబ్‌సైట్ సెట్టింగ్స్
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")
st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

# 2. సైడ్‌బార్
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 3. యూజర్ ఇన్‌పుట్
user_url = st.text_input("URLని పేస్ట్ చేయండి (e.g., google.com):", placeholder="https://example.com")

if st.button("Analyze"):
    if not api_key:
        st.error("ముందుగా API Keyని ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("లింక్ ఏదీ ఎంటర్ చేయలేదు!")
    else:
        try:
            with st.spinner('సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                # URL క్లీనింగ్
                clean_url = user_url if '://' in user_url else 'http://' + user_url
                parsed_url = urlparse(clean_url)
                domain = parsed_url.netloc
                
                # IP Details
                ip_addr = socket.gethostbyname(domain)
                geo = requests.get(f"https://ipapi.co/{ip_addr}/json/").json()
                
                st.success("✅ సర్వర్ వివరాలు లభించాయి!")
                st.info(f"**IP:** {ip_addr} | **Country:** {geo.get('country_name')} | **ISP:** {geo.get('org')}")

            # 4. AI విశ్లేషణ (Updated Logic)
            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                # API కాన్ఫిగరేషన్
                genai.configure(api_key=api_key)
                
                # ఇక్కడ మనం నేరుగా మోడల్ ఆబ్జెక్ట్‌ని క్రియేట్ చేస్తున్నాం
                # నీ Logs లో ఉన్న ఎర్రర్ ప్రకారం ఈ కింది పద్ధతి కరెక్ట్:
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                
                prompt = f"""
                Act as a Cyber Security Expert. Analyze this URL for phishing risks:
                URL: {user_url}
                IP: {ip_addr}
                Location: {geo.get('city')}, {geo.get('country_name')}
                
                Give a detailed report in Telugu including verdict and safety tips.
                """
                
                # కంటెంట్ జనరేట్ చేయడం
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("AI విశ్లేషణ పూర్తయింది!")
                    st.write(response.text)
                else:
                    st.error("AI నుండి సమాధానం రాలేదు. దయచేసి మళ్ళీ ప్రయత్నించండి.")

        except Exception as e:
            # ఒకవేళ 1.5-flash రాకపోతే, gemini-pro ని ప్రయత్నించేలా చిన్న fallback
            try:
                model = genai.GenerativeModel(model_name="gemini-pro")
                response = model.generate_content(prompt)
                st.write(response.text)
            except:
                st.error(f"Error: {e}")
                st.info("చిట్కా: మీ API Key కరెక్ట్ గా ఉందో లేదో ఒకసారి AI Studio లో చూడండి.")

st.markdown("---")
st.caption("Developed by Barla Hareesh | Powered by Gemini AI")
