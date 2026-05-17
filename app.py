import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# 1. వెబ్‌సైట్ ప్రాథమిక సెట్టింగ్స్
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")

st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

# 2. సైడ్‌బార్ - API Key మరియు సెట్టింగ్స్
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.info("కీ కోసం ఇక్కడ చూడండి: [Google AI Studio](https://aistudio.google.com/app/apikey)")

# 3. యూజర్ ఇంటర్‌ఫేస్
st.write("### ఏదైనా లింక్‌ని ఇక్కడ స్కాన్ చేయండి 👇")
user_url = st.text_input("URLని పేస్ట్ చేయండి (e.g., google.com):", placeholder="https://example.com")

if st.button("లింక్‌ని పరిశీలించు (Analyze)"):
    if not api_key:
        st.error("దయచేసి సైడ్‌బార్‌లో మీ Gemini API Keyని ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("లింక్ ఏదీ ఎంటర్ చేయలేదు!")
    else:
        try:
            with st.spinner('సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                # URL నుండి డొమైన్ పేరును తీయడం
                clean_url = user_url if '://' in user_url else 'http://' + user_url
                parsed_url = urlparse(clean_url)
                domain = parsed_url.netloc
                
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

            # 4. AI విశ్లేషణ (Security Report)
            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక (Security Report)")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                genai.configure(api_key=api_key)
                
                # 404 ఎర్రర్ రాకుండా ఉండటానికి ఆటోమేటిక్ మోడల్ సెలెక్షన్
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    test_response = model.generate_content("test") # టెస్ట్ రన్
                except:
                    model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"""
                Act as a Cyber Security Expert. Analyze this URL for phishing or security risks:
                URL: {user_url}
                IP: {ip_addr}
                Location: {geo.get('city')}, {geo.get('country_name')}
                ISP: {geo.get('org')}
                
                Provide a report in Telugu language including:
                1. Verdict (Safe/Suspicious/Dangerous)
                2. Reasons for the verdict.
                3. Safety advice for the user.
                """
                
                response = model.generate_content(prompt)
                st.info(response.text)

        except Exception as e:
            st.error(f"క్షమించండి! వివరాలు సేకరించలేకపోయాను. URL సరిగ్గా ఉందో లేదో చూడండి. \n(Error: {e})")

st.markdown("---")
st.caption("Developed by Barla Hareesh | Powered by Gemini AI")
