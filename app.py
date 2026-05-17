import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# 1. వెబ్‌సైట్ సెట్టింగ్స్ (పేజీ టైటిల్ మరియు ఐకాన్)
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")

st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

# 2. యూజర్ నుండి Gemini API Key తీసుకోవడం (Security కోసం)
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.info("Get your key from: [Google AI Studio](https://aistudio.google.com/app/apikey)")

# 3. మెయిన్ ఇంటర్‌ఫేస్
st.write("### ఏదైనా లింక్‌ని ఇక్కడ స్కాన్ చేయండి 👇")
user_url = st.text_input("URLని పేస్ట్ చేయండి:", placeholder="https://example.com")

if st.button("లింక్‌ని పరిశీలించు (Analyze)"):
    if not api_key:
        st.error("ముందుగా సైడ్‌బార్‌లో మీ Gemini API Keyని ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("లింక్ ఏదీ ఎంటర్ చేయలేదు!")
    else:
        try:
            with st.spinner('సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                # URL నుండి డొమైన్ పేరును తీయడం
                parsed_url = urlparse(user_url)
                domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
                
                # IP Address కనుక్కోవడం
                ip_addr = socket.gethostbyname(domain)
                
                # IP ద్వారా లొకేషన్ వివరాలు
                geo = requests.get(f"https://ipapi.co/{ip_addr}/json/").json()
                
                # రిజల్ట్స్ డిస్‌ప్లే
                st.success("✅ సర్వర్ వివరాలు లభించాయి!")
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**IP Address:** \n{ip_addr}")
                    st.info(f"**City:** \n{geo.get('city', 'N/A')}")
                with col2:
                    st.info(f"**Country:** \n{geo.get('country_name', 'N/A')}")
                    st.info(f"**ISP:** \n{geo.get('org', 'N/A')}")

            # AI విశ్లేషణ (Threat Analysis)
            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక (Security Report)")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"""
                Act as a Cyber Security Expert. Analyze this URL and its server details:
                URL: {user_url}
                IP: {ip_addr}
                Location: {geo.get('city')}, {geo.get('country_name')}
                ISP: {geo.get('org')}
                
                Tell me:
                1. Is it Safe, Suspicious, or Dangerous?
                2. Reason for your verdict.
                3. Advice for the user.
                Keep it concise.
                """
                
                response = model.generate_content(prompt)
                st.write(response.text)

        except Exception as e:
            st.error(f"క్షమించండి! వివరాలు సేకరించలేకపోయాను. URL సరిగ్గా ఉందో లేదో చూడండి. \n(Error: {e})")

st.markdown("---")
st.caption("Developed for Cyber Security Awareness | Powered by Gemini AI")
