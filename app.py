import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# 1. పేజీ సెట్టింగ్స్ (అందమైన డిజైన్ కోసం)
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️", layout="centered")

# Custom CSS for styling (నీ పాత యాప్ లాగే కనిపిస్తుంది)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.write("Cyber Security Expert AI ద్వారా ఏదైనా లింక్‌ని తనిఖీ చేయండి.")
st.markdown("---")

# 2. సైడ్‌బార్ సెట్టింగ్స్
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
st.sidebar.markdown("[Get API Key Here](https://aistudio.google.com/app/apikey)")
st.sidebar.markdown("---")
st.sidebar.caption("Developed by: Barla Hareesh")

# 3. యూజర్ ఇన్‌పుట్
user_url = st.text_input("🔗 URLని ఇక్కడ పేస్ట్ చేయండి (e.g., google.com):", placeholder="https://example.com")

if st.button("లింక్‌ని పరిశీలించు (Analyze)"):
    if not api_key:
        st.error("❌ దయచేసి సైడ్‌బార్‌లో Gemini API Keyని ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("⚠️ దయచేసి ఒక URLని ఎంటర్ చేయండి!")
    else:
        try:
            with st.spinner('🔍 సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                # URL క్లీనింగ్
                clean_url = user_url if '://' in user_url else 'http://' + user_url
                parsed_url = urlparse(clean_url)
                domain = parsed_url.netloc
                
                # IP Details
                ip_addr = socket.gethostbyname(domain)
                geo = requests.get(f"https://ipapi.co/{ip_addr}/json/").json()
                
                st.success("✅ సర్వర్ వివరాలు లభించాయి!")
                
                # సర్వర్ వివరాలను కాలమ్స్‌లో చూపించడం
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("IP Address", ip_addr)
                    st.write(f"**City:** {geo.get('city', 'Unknown')}")
                with c2:
                    st.metric("Country", geo.get('country_name', 'Unknown'))
                    st.write(f"**ISP:** {geo.get('org', 'Unknown')}")

            # 4. AI విశ్లేషణ (పక్కాగా పనిచేసే Gemini 1.5 Flash)
            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                genai.configure(api_key=api_key)
                
                # లేటెస్ట్ స్టేబుల్ మోడల్
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Act as a Cyber Security Expert. Analyze this website for phishing risks:
                URL: {user_url}
                IP: {ip_addr}
                Location: {geo.get('city')}, {geo.get('country_name')}
                ISP: {geo.get('org')}
                
                Provide a report in Telugu language:
                1. Verdict (Safe/Suspicious/Dangerous)
                2. Reasons for the verdict.
                3. Safety tips for the user.
                """
                
                response = model.generate_content(prompt)
                st.info(response.text)

        except Exception as e:
            # Fallback to Gemini Pro if Flash fails
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Analyze {user_url} for phishing. Telugu report.")
                st.info(response.text)
            except:
                st.error(f"Error: {e}")
                st.info("చిట్కా: URL సరిగ్గా ఉందో లేదో చూడండి.")

st.markdown("---")
st.caption("© 2026 PhishShield AI | Awareness Project by Barla Hareesh")
