import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import requests
from streamlit_lottie import st_lottie
from swara_engine import process_audio

st.set_page_config(page_title="Swara Setu AI", page_icon="🌐", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .title-box { text-align: center; padding: 20px; background-color: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_translate = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4kji20Y9.json")

st.markdown('<div class="title-box"><h1>🌐 Swara Setu AI</h1><p style="color:gray;">Global Real-Time Communicator</p></div>', unsafe_allow_html=True)

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

# --- State Management for the Swap Button ---
if 'src_dropdown' not in st.session_state:
    st.session_state.src_dropdown = "Telugu"
if 'tgt_dropdown' not in st.session_state:
    st.session_state.tgt_dropdown = "English"

def swap_languages():
    temp = st.session_state.src_dropdown
    st.session_state.src_dropdown = st.session_state.tgt_dropdown
    st.session_state.tgt_dropdown = temp

# --- UI: Language Selection & Swap Button ---
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    source_language = st.selectbox("You Speak:", lang_names, key="src_dropdown")
with col2:
    st.write("") 
    st.write("")
    st.button("🔄 Swap", on_click=swap_languages, use_container_width=True)
with col3:
    target_language = st.selectbox("They Hear:", lang_names, key="tgt_dropdown")

src_code = LANGUAGES[source_language]
tgt_code = LANGUAGES[target_language]

st.divider()

# --- Audio Recording & Processing ---
st.write("### 🎙️ Hold to Speak")
audio_bytes = audio_recorder(text="Tap to Record", recording_color="#ff4757", neutral_color="#2ed573", icon_size="2x")

if audio_bytes:
    temp_input_path = "temp_input.wav"
    with open(temp_input_path, "wb") as f:
        f.write(audio_bytes)
        
    st.audio(audio_bytes, format="audio/wav")

    if st.button("Translate & Speak", use_container_width=True, type="primary"):
        if lottie_translate:
            st_lottie(lottie_translate, height=150, key="translating")
            
        with st.spinner(f'Translating...'):
            original_text, translated_text, result = process_audio(temp_input_path, src_code, tgt_code)

        if original_text and translated_text and result.endswith('.mp3'):
            st.info(f"**{source_language}:** {original_text}")
            st.success(f"**{target_language}:** {translated_text}")
            # Autoplay is enabled so you don't have to click play
            st.audio(result, format="audio/mp3", autoplay=True) 
        else:
            st.error(f"Error: {result}")