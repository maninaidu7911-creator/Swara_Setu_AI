import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import requests
from streamlit_lottie import st_lottie
from swara_engine import process_audio

st.set_page_config(page_title="Swara Setu AI", page_icon="🌐", layout="centered")

# --- 1. Advanced Premium CSS (Glassmorphism & Animations) ---
st.markdown("""
    <style>
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Glassmorphism Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: slideUp 0.8s ease-out forwards;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Smooth Slide-Up Animation */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Premium Button Hover Effects */
    div.stButton > button {
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. UI Dictionary (Localization) ---
UI_TEXT = {
    "English": {
        "title": "🌐 Swara Setu AI",
        "subtitle": "Global Real-Time Communicator",
        "you_speak": "You Speak:",
        "they_hear": "They Hear:",
        "swap": "🔄 Swap",
        "hold_speak": "🎙️ Hold to Speak",
        "tap_record": "Tap to Record",
        "translate_btn": "Translate & Speak",
        "translating": "Translating in real-time...",
        "success": "Translation Complete!",
        "settings": "⚙️ App Language"
    },
    "Telugu": {
        "title": "🌐 స్వర సేతు AI",
        "subtitle": "గ్లోబల్ రియల్-టైమ్ కమ్యూనికేటర్",
        "you_speak": "మీరు మాట్లాడేది:",
        "they_hear": "వారు వినేది:",
        "swap": "🔄 మార్చండి",
        "hold_speak": "🎙️ మాట్లాడటానికి పట్టుకోండి",
        "tap_record": "రికార్డ్ చేయడానికి నొక్కండి",
        "translate_btn": "అనువదించి వినిపించండి",
        "translating": "అనువదిస్తోంది...",
        "success": "అనువాదం పూర్తయింది!",
        "settings": "⚙️ యాప్ భాష"
    },
    "Hindi": {
        "title": "🌐 स्वर सेतु AI",
        "subtitle": "ग्लोबल रियल-टाइम कम्युनिकेटर",
        "you_speak": "आप बोलते हैं:",
        "they_hear": "वे सुनते हैं:",
        "swap": "🔄 बदलें",
        "hold_speak": "🎙️ बोलने के लिए दबाएं",
        "tap_record": "रिकॉर्ड करने के लिए टैप करें",
        "translate_btn": "अनुवाद करें और बोलें",
        "translating": "अनुवाद हो रहा है...",
        "success": "अनुवाद पूरा हुआ!",
        "settings": "⚙️ ऐप की भाषा"
    }
}

# --- Expanded Global Language Dictionary ---
LANGUAGES = {
    "Arabic": "ar", "Bengali": "bn", "Chinese (Simplified)": "zh-CN", "Dutch": "nl", 
    "English": "en", "French": "fr", "German": "de", "Greek": "el", 
    "Gujarati": "gu", "Hindi": "hi", "Italian": "it", "Japanese": "ja", 
    "Kannada": "kn", "Korean": "ko", "Malayalam": "ml", "Marathi": "mr", 
    "Nepali": "ne", "Odia": "or", "Portuguese": "pt", "Punjabi": "pa", 
    "Russian": "ru", "Spanish": "es", "Tamil": "ta", "Telugu": "te", 
    "Urdu": "ur", "Vietnamese": "vi"
}
lang_names = list(LANGUAGES.keys())

# --- 3. State Management ---
if 'ui_lang' not in st.session_state:
    st.session_state.ui_lang = "English"
if 'app_started' not in st.session_state:
    st.session_state.app_started = False
if 'src_dropdown' not in st.session_state:
    st.session_state.src_dropdown = "Telugu"
if 'tgt_dropdown' not in st.session_state:
    st.session_state.tgt_dropdown = "English"

def swap_languages():
    temp = st.session_state.src_dropdown
    st.session_state.src_dropdown = st.session_state.tgt_dropdown
    st.session_state.tgt_dropdown = temp

def start_app():
    st.session_state.app_started = True

def reset_app():
    st.session_state.app_started = False

# Helper for animations
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_welcome = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_q5pk6p1k.json")
lottie_translate = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4kji20Y9.json")

# ==========================================
# STEP 1: WELCOME & APP LANGUAGE SELECTION
# ==========================================
if not st.session_state.app_started:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if lottie_welcome:
        st_lottie(lottie_welcome, height=200, key="welcome_anim")
        
    st.title("🌐 Swara Setu AI")
    st.markdown("<p style='color:gray; font-size:18px;'>Select your preferred app interface language / మీ యాప్ భాషను ఎంచుకోండి</p>", unsafe_allow_html=True)
    
    st.session_state.ui_lang = st.selectbox("", ["English", "Telugu", "Hindi"], label_visibility="collapsed")
    
    st.write("")
    st.button("Enter App 🚀", on_click=start_app, type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# STEP 2: MAIN TRANSLATOR INTERFACE
# ==========================================
else:
    # Load UI text based on selection
    t = UI_TEXT[st.session_state.ui_lang]
    
    # Sidebar for changing App Language back
    with st.sidebar:
        st.button(f"🔙 {t['settings']}", on_click=reset_app, use_container_width=True)

    # Header Card
    st.markdown(f'''
        <div class="glass-card">
            <h1>{t['title']}</h1>
            <p style="color:#555; font-size:16px;">{t['subtitle']}</p>
        </div>
    ''', unsafe_allow_html=True)

    # Translation Interface Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        source_language = st.selectbox(t["you_speak"], lang_names, key="src_dropdown")
    with col2:
        st.write("") 
        st.write("")
        st.button(t["swap"], on_click=swap_languages, use_container_width=True)
    with col3:
        target_language = st.selectbox(t["they_hear"], lang_names, key="tgt_dropdown")

    src_code = LANGUAGES[source_language]
    tgt_code = LANGUAGES[target_language]
    
    st.divider()

    # Recording Section
    st.markdown(f"### {t['hold_speak']}")
    audio_bytes = audio_recorder(text=t["tap_record"], recording_color="#ff4757", neutral_color="#2ed573", icon_size="2x")

    if audio_bytes:
        temp_input_path = "temp_input.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_bytes)
            
        st.audio(audio_bytes, format="audio/wav")

        if st.button(t["translate_btn"], use_container_width=True, type="primary"):
            
            st.markdown(f"#### ⚙️ {t['translating']}")
            if lottie_translate:
                st_lottie(lottie_translate, height=120, key="translating")
                
            with st.spinner('...'):
                original_text, translated_text, result = process_audio(temp_input_path, src_code, tgt_code)

            if original_text and translated_text and result.endswith('.mp3'):
                st.success(t["success"])
                st.info(f"**{source_language}:** {original_text}")
                st.success(f"**{target_language}:** {translated_text}")
                st.audio(result, format="audio/mp3", autoplay=True) 
            else:
                st.error(f"Error: {result}")
                
    st.markdown('</div>', unsafe_allow_html=True)
