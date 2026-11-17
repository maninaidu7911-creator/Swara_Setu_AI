import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import requests
from streamlit_lottie import st_lottie
from swara_engine import process_audio

# --- Page Config ---
st.set_page_config(page_title="Swara Setu AI | Global Communicator", page_icon="🌍", layout="centered")

# --- Minimalist Professional CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .main-title {
        color: #1E3A8A;
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }

    div.stButton > button {
        background: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background: #1D4ED8;
    }
    
    div.stButton > button:contains("🔄") {
        background: white !important;
        color: #2563EB !important;
        border: 1px solid #CBD5E1 !important;
    }

    .custom-footer {
        text-align: center;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid #E2E8F0;
        color: #64748B;
    }
    .custom-footer a {
        color: #2563EB;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Dictionary ---
UI_TEXT = {
    "English": {
        "title": "Swara Setu AI",
        "subtitle": "Global Real-Time Voice Translation",
        "you_speak": "You Speak:",
        "they_hear": "They Hear:",
        "swap": "🔄 Swap",
        "hold_speak": "Audio Input",
        "tap_record": "Tap to Record",
        "translate_btn": "Translate Audio",
        "translating": "Processing...",
        "success": "Translation Successful",
        "settings": "⚙️ Change App Language"
    },
    "Telugu": {
        "title": "స్వర సేతు AI",
        "subtitle": "గ్లోబల్ రియల్-టైమ్ వాయిస్ అనువాదం",
        "you_speak": "మీరు మాట్లాడేది:",
        "they_hear": "వారు వినేది:",
        "swap": "🔄 మార్చండి",
        "hold_speak": "ఆడియో రికార్డింగ్",
        "tap_record": "రికార్డ్ చేయడానికి నొక్కండి",
        "translate_btn": "అనువదించండి",
        "translating": "అనువదిస్తోంది...",
        "success": "అనువాదం పూర్తయింది",
        "settings": "⚙️ భాష మార్చండి"
    },
    "Hindi": {
        "title": "स्वर सेतु AI",
        "subtitle": "ग्लोबल रियल-टाइम वॉयस ट्रांसलेशन",
        "you_speak": "आप बोलते हैं:",
        "they_hear": "वे सुनते हैं:",
        "swap": "🔄 बदलें",
        "hold_speak": "ऑडियो इनपुट",
        "tap_record": "रिकॉर्ड करने के लिए टैप करें",
        "translate_btn": "अनुवाद करें",
        "translating": "अनुवाद हो रहा है...",
        "success": "अनुवाद पूरा हुआ",
        "settings": "⚙️ भाषा बदलें"
    }
}

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

# --- State Management ---
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

# ==========================================
# STEP 1: CLEAN WELCOME SCREEN
# ==========================================
if not st.session_state.app_started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>Swara Setu AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Select your preferred interface language<br>మీ యాప్ భాషను ఎంచుకోండి</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.ui_lang = st.selectbox("Language / భాష", ["English", "Telugu", "Hindi"], label_visibility="collapsed")
        st.write("")
        st.button("Launch App", on_click=start_app, type="primary", use_container_width=True)

# ==========================================
# STEP 2: PROFESSIONAL WORKSPACE
# ==========================================
else:
    t = UI_TEXT[st.session_state.ui_lang]
    
    with st.sidebar:
        st.button(t['settings'], on_click=reset_app, use_container_width=True)

    st.markdown(f"<h1 class='main-title'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-title'>{t['subtitle']}</p>", unsafe_allow_html=True)

    # 1. Language Selectors
    col1, col2, col3 = st.columns([5, 2, 5])
    with col1:
        source_language = st.selectbox(f"**{t['you_speak']}**", lang_names, key="src_dropdown")
    with col2:
        st.write("") 
        st.write("")
        st.button(t["swap"], on_click=swap_languages, use_container_width=True)
    with col3:
        target_language = st.selectbox(f"**{t['they_hear']}**", lang_names, key="tgt_dropdown")

    src_code = LANGUAGES[source_language]
    tgt_code = LANGUAGES[target_language]

    st.divider()

    # 2. Audio Input
    st.markdown(f"<h3 style='text-align: center; color: #1E3A8A;'>{t['hold_speak']}</h3>", unsafe_allow_html=True)
    
    col_e1, col_mic, col_e2 = st.columns([1, 1, 1])
    with col_mic:
        audio_bytes = audio_recorder(text=t["tap_record"], recording_color="#EF4444", neutral_color="#2563EB", icon_size="2x")

    # 3. Processing & Output
    if audio_bytes:
        temp_input_path = "temp_input.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_bytes)
            
        st.audio(audio_bytes, format="audio/wav")
        st.write("")

        if st.button(t["translate_btn"], use_container_width=True, type="primary"):
            with st.spinner(t['translating']):
                original_text, translated_text, result = process_audio(temp_input_path, src_code, tgt_code)

            if original_text and translated_text and result.endswith('.mp3'):
                st.success(t["success"])
                st.info(f"**{source_language}:** {original_text}")
                st.success(f"**{target_language}:** {translated_text}")
                st.audio(result, format="audio/mp3", autoplay=True) 
            else:
                st.error(f"Error: {result}")

    # ==========================================
    # STEP 3: CUSTOM FOOTER
    # ==========================================
    st.markdown("""
        <div class="custom-footer">
            Designed by <a href="https://www.linkedin.com/in/manikanta-dandabattula" target="_blank">Manikanta</a>
        </div>
    """, unsafe_allow_html=True)
