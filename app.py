import streamlit as st
import socket
import requests
import google.generativeai as genai
from urllib.parse import urlparse

# 1. పేజీ సెట్టింగ్స్ మరియు అందమైన డిజైన్
st.set_page_config(page_title="PhishShield AI", page_icon="🛡️")

# నీ పాత యాప్ లో ఉన్న CSS స్టైలింగ్
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ PhishShield: AI Phishing Analyzer")
st.markdown("---")

# 2. సైడ్‌బార్ కాన్ఫిగరేషన్
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.markdown("[Get API Key Here](https://aistudio.google.com/app/apikey)")
st.sidebar.markdown("---")
st.sidebar.write("Developed by: Barla Hareesh")

# 3. యూజర్ ఇన్‌పుట్
user_url = st.text_input("URLని ఇక్కడ పేస్ట్ చేయండి:", placeholder="https://example.com")

if st.button("Analyze"):
    if not api_key:
        st.error("దయచేసి API Keyని ఎంటర్ చేయండి!")
    elif not user_url:
        st.warning("URL ఎంటర్ చేయండి!")
    else:
        try:
            with st.spinner('సర్వర్ వివరాలను సేకరిస్తున్నాను...'):
                # URL క్లీనింగ్
                clean_url = user_url if '://' in user_url else 'http://' + user_url
                parsed_url = urlparse(clean_url)
                domain = parsed_url.netloc
                
                # IP Address మరియు సర్వర్ వివరాలు
                ip_addr = socket.gethostbyname(domain)
                geo = requests.get(f"https://ipapi.co/{ip_addr}/json/").json()
                
                st.success("✅ సర్వర్ వివరాలు లభించాయి!")
                
                # పాత కోడ్ లాగా బాక్సుల్లో చూపించడం
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**IP Address:** {ip_addr}")
                    st.info(f"**City:** {geo.get('city', 'Unknown')}")
                with col2:
                    st.info(f"**Country:** {geo.get('country_name', 'Unknown')}")
                    st.info(f"**ISP:** {geo.get('org', 'Unknown')}")

            # 4. AI భద్రతా నివేదిక
            st.markdown("---")
            st.subheader("🤖 AI భద్రతా నివేదిక")
            
            with st.spinner('AI విశ్లేషిస్తోంది...'):
                genai.configure(api_key=api_key)
                
                # ఎర్రర్ రాకుండా ఉండటానికి మోడల్ సెలెక్షన్
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Act as a Cyber Security Expert. Analyze this URL for phishing risks: {user_url}. 
                Details: IP {ip_addr}, Location {geo.get('city')}, {geo.get('country_name')}. 
                Provide a verdict and advice in Telugu.
                """
                
                response = model.generate_content(prompt)
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed by Barla Hareesh")
