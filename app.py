import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import requests
from swara_engine import process_audio

# --- Page Config ---
st.set_page_config(page_title="Swara Setu AI", page_icon="🌐", layout="centered")

# --- Minimalist CSS (Only for hiding watermarks and footer) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .custom-footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(128, 128, 128, 0.2);
        font-size: 0.9rem;
        color: gray;
    }
    .custom-footer a {
        color: #2563EB;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Dictionary ---
UI_TEXT = {
    "English": {
        "title": "Swara Setu AI",
        "subtitle": "Global Real-Time Voice Translation",
        "you_speak": "🗣️ You Speak:",
        "they_hear": "🎧 They Hear:",
        "swap": "🔄 Swap Languages",
        "hold_speak": "🎙️ Audio Input",
        "tap_record": "Tap to Record",
        "translate_btn": "✨ Translate",
        "translating": "Processing audio...",
        "success": "Translation Successful",
        "settings": "⚙️ App Settings"
    },
    "Telugu": {
        "title": "స్వర సేతు AI",
        "subtitle": "గ్లోబల్ రియల్-టైమ్ వాయిస్ అనువాదం",
        "you_speak": "🗣️ మీరు మాట్లాడేది:",
        "they_hear": "🎧 వారు వినేది:",
        "swap": "🔄 భాష మార్చండి",
        "hold_speak": "🎙️ ఆడియో రికార్డింగ్",
        "tap_record": "రికార్డ్ చేయడానికి నొక్కండి",
        "translate_btn": "✨ అనువదించండి",
        "translating": "అనువదిస్తోంది...",
        "success": "అనువాదం పూర్తయింది",
        "settings": "⚙️ యాప్ సెట్టింగ్స్"
    },
    "Hindi": {
        "title": "स्वर सेतु AI",
        "subtitle": "ग्लोबल रियल-टाइम वॉयस ट्रांसलेशन",
        "you_speak": "🗣️ आप बोलते हैं:",
        "they_hear": "🎧 वे सुनते हैं:",
        "swap": "🔄 भाषा बदलें",
        "hold_speak": "🎙️ ऑडियो इनपुट",
        "tap_record": "रिकॉर्ड करने के लिए टैप करें",
        "translate_btn": "✨ अनुवाद करें",
        "translating": "अनुवाद हो रहा है...",
        "success": "अनुवाद पूरा हुआ",
        "settings": "⚙️ ऐप सेटिंग्स"
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
# STEP 1: MOBILE-FRIENDLY WELCOME SCREEN
# ==========================================
if not st.session_state.app_started:
    st.write("<br>", unsafe_allow_html=True)
    st.title("🌐 Swara Setu AI")
    st.markdown("#### Select interface language")
    st.caption("మీ యాప్ భాషను ఎంచుకోండి / अपनी भाषा चुनें")
    
    st.write("")
    st.session_state.ui_lang = st.selectbox("Language / భాష", ["English", "Telugu", "Hindi"], label_visibility="collapsed")
    st.write("")
    st.button("Launch App 🚀", on_click=start_app, type="primary", use_container_width=True)

# ==========================================
# STEP 2: PROFESSIONAL MOBILE WORKSPACE
# ==========================================
else:
    t = UI_TEXT[st.session_state.ui_lang]
    
    # Sidebar for reset
    with st.sidebar:
        st.button(t['settings'], on_click=reset_app, use_container_width=True)

    # Clean Native Headers
    st.title(f"🌐 {t['title']}")
    st.caption(t['subtitle'])
    st.divider()

    # Mobile Layout: Stacked Dropdowns with Swap Button in the middle
    source_language = st.selectbox(t['you_speak'], lang_names, key="src_dropdown")
    
    st.button(t["swap"], on_click=swap_languages, use_container_width=True)
    
    target_language = st.selectbox(t['they_hear'], lang_names, key="tgt_dropdown")

    src_code = LANGUAGES[source_language]
    tgt_code = LANGUAGES[target_language]

    st.divider()

    # Audio Section
    st.subheader(t['hold_speak'])
    
    # Centered Audio Box
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        audio_bytes = audio_recorder(text=t["tap_record"], recording_color="#FF4B4B", neutral_color="#1E88E5", icon_size="2x")

    # Processing & Output
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
                
                # Clean Output Boxes
                st.info(f"**{source_language}:**\n\n{original_text}")
                st.success(f"**{target_language}:**\n\n{translated_text}")
                
                st.audio(result, format="audio/mp3", autoplay=True) 
            else:
                st.error(f"Error: {result}")

    # ==========================================
    # STEP 3: CUSTOM FOOTER
    # ==========================================
    st.markdown("""
        <div class="custom-footer">
            Designed by <a href="https://www.linkedin.com/in/dandabattula-manikanta" target="_blank">Manikanta</a>
        </div>
    """, unsafe_allow_html=True)
