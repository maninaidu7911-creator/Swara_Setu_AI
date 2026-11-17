import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import requests
from streamlit_lottie import st_lottie
from swara_engine import process_audio

# --- Page Config ---
st.set_page_config(page_title="Swara Setu AI", page_icon="🌐", layout="centered")

# --- Minimalist Professional CSS ---
st.markdown("""
    <style>
    /* Clean, modern background */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Hide default Streamlit branding for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Premium Button Styling */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Center align block elements */
    .center-content {
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Dictionary (Localization) ---
UI_TEXT = {
    "English": {
        "title": "🌐 Swara Setu AI",
        "subtitle": "Global Real-Time Communicator",
        "you_speak": "You Speak",
        "they_hear": "They Hear",
        "swap": "🔄 Swap",
        "hold_speak": "🎙️ Audio Input",
        "tap_record": "Tap to Record",
        "translate_btn": "Translate & Speak",
        "translating": "Processing translation...",
        "success": "Translation Successful",
        "settings": "⚙️ App Language"
    },
    "Telugu": {
        "title": "🌐 స్వర సేతు AI",
        "subtitle": "గ్లోబల్ రియల్-టైమ్ కమ్యూనికేటర్",
        "you_speak": "మీరు మాట్లాడేది",
        "they_hear": "వారు వినేది",
        "swap": "🔄 మార్చండి",
        "hold_speak": "🎙️ ఆడియో ఇన్పుట్",
        "tap_record": "రికార్డ్ చేయడానికి నొక్కండి",
        "translate_btn": "అనువదించి వినిపించండి",
        "translating": "అనువదిస్తోంది...",
        "success": "అనువాదం పూర్తయింది",
        "settings": "⚙️ యాప్ భాష"
    },
    "Hindi": {
        "title": "🌐 स्वर सेतु AI",
        "subtitle": "ग्लोबल रियल-टाइम कम्युनिकेटर",
        "you_speak": "आप बोलते हैं",
        "they_hear": "वे सुनते हैं",
        "swap": "🔄 बदलें",
        "hold_speak": "🎙️ ऑडियो इनपुट",
        "tap_record": "रिकॉर्ड करने के लिए टैप करें",
        "translate_btn": "अनुवाद करें और बोलें",
        "translating": "अनुवाद हो रहा है...",
        "success": "अनुवाद पूरा हुआ",
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

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_translate = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4kji20Y9.json")

# ==========================================
# STEP 1: CLEAN WELCOME SCREEN
# ==========================================
if not st.session_state.app_started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a; font-size: 3rem;'>🌐 Swara Setu AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;'>Select your preferred interface language<br>మీ యాప్ భాషను ఎంచుకోండి</p>", unsafe_allow_html=True)
    
    # Use columns to tightly center the dropdown and button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.ui_lang = st.selectbox("Language", ["English", "Telugu", "Hindi"], label_visibility="collapsed")
        st.write("")
        st.button("Enter Workspace", on_click=start_app, type="primary", use_container_width=True)

# ==========================================
# STEP 2: MAIN TRANSLATOR INTERFACE
# ==========================================
else:
    t = UI_TEXT[st.session_state.ui_lang]
    
    # Sidebar for changing App Language back
    with st.sidebar:
        st.button(f"🔙 {t['settings']}", on_click=reset_app, use_container_width=True)

    # Clean Header
    st.markdown(f"<h1 style='text-align: center; color: #0f172a;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>{t['subtitle']}</p>", unsafe_allow_html=True)

    # Routing Interface
    col1, col2, col3 = st.columns([2, 1, 2])
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
    
    st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Recording Section
    st.markdown(f"<h3 style='color: #334155;'>{t['hold_speak']}</h3>", unsafe_allow_html=True)
    
    col_mic, col_space = st.columns([1, 3])
    with col_mic:
        audio_bytes = audio_recorder(text=t["tap_record"], recording_color="#ef4444", neutral_color="#10b981", icon_size="2x")

    if audio_bytes:
        temp_input_path = "temp_input.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_bytes)
            
        st.audio(audio_bytes, format="audio/wav")
        st.write("")

        if st.button(t["translate_btn"], use_container_width=True, type="primary"):
            
            if lottie_translate:
                st_lottie(lottie_translate, height=80, key="translating")
                
            with st.spinner(t['translating']):
                original_text, translated_text, result = process_audio(temp_input_path, src_code, tgt_code)

            if original_text and translated_text and result.endswith('.mp3'):
                st.success(t["success"])
                st.info(f"**{source_language}:** {original_text}")
                st.success(f"**{target_language}:** {translated_text}")
                st.audio(result, format="audio/mp3", autoplay=True) 
            else:
                st.error(f"Error: {result}")
