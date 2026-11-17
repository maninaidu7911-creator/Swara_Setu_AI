import streamlit as st
import os
import requests
from streamlit_lottie import st_lottie
from swara_engine import process_audio

# --- Page Config ---
st.set_page_config(page_title="Swara Setu AI", page_icon="🌐", layout="centered")

# --- Premium Native CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu, header, footer {visibility: hidden;}

    /* Premium Typography */
    .hero-title {
        font-weight: 800;
        font-size: 3.5rem;
        text-align: center;
        background: linear-gradient(90deg, #2563EB, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInDown 0.8s ease-out;
        margin-bottom: 0px;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #475569;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 5px;
        margin-bottom: 35px;
        animation: fadeIn 1.2s ease-in;
    }

    /* Floating Glassmorphism Cards */
    .glass-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 25px;
        animation: slideUp 0.6s ease-out forwards;
    }

    /* Premium Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }
    
    /* Swap Button Override */
    div.stButton > button:contains("🔄") {
        background: white !important;
        color: #2563eb !important;
        border: 2px solid #eff6ff !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Results Box Styling */
    div[data-testid="stInfo"], div[data-testid="stSuccess"] {
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        background: #F8FAFC;
        color: #334155;
    }

    /* Custom Designer Footer */
    .designer-footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(128,128,128, 0.2);
    }
    .designer-footer p {
        color: #64748B;
        font-size: 0.95rem;
    }
    .designer-footer a {
        color: #9333EA;
        font-weight: 800;
        text-decoration: none;
    }
    .designer-footer a:hover {
        color: #2563EB;
        text-decoration: underline;
    }

    /* Animations */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Dictionary ---
UI_TEXT = {
    "English": {
        "subtitle": "Global Real-Time Voice Translation",
        "you_speak": "🗣️ You Speak:",
        "they_hear": "🎧 They Hear:",
        "swap": "🔄 Swap",
        "hold_speak": "🎙️ Tap to Record Audio",
        "translate_btn": "✨ Translate & Speak",
        "translating": "Processing audio...",
        "success": "Translation Successful",
        "settings": "⚙️ Language"
    },
    "Telugu": {
        "subtitle": "గ్లోబల్ రియల్-టైమ్ వాయిస్ అనువాదం",
        "you_speak": "🗣️ మీరు మాట్లాడేది:",
        "they_hear": "🎧 వారు వినేది:",
        "swap": "🔄 మార్చండి",
        "hold_speak": "🎙️ ఆడియో రికార్డ్ చేయడానికి నొక్కండి",
        "translate_btn": "✨ అనువదించి వినిపించండి",
        "translating": "అనువదిస్తోంది...",
        "success": "అనువాదం పూర్తయింది",
        "settings": "⚙️ భాష"
    },
    "Hindi": {
        "subtitle": "ग्लोबल रियल-टाइम वॉयस ट्रांसलेशन",
        "you_speak": "🗣️ आप बोलते हैं:",
        "they_hear": "🎧 वे सुनते हैं:",
        "swap": "🔄 बदलें",
        "hold_speak": "🎙️ ऑडियो रिकॉर्ड करने के लिए टैप करें",
        "translate_btn": "✨ अनुवाद करें और बोलें",
        "translating": "अनुवाद हो रहा है...",
        "success": "अनुवाद पूरा हुआ",
        "settings": "⚙️ भाषा"
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

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_wave = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4kji20Y9.json")

# ==========================================
# STEP 1: WELCOME SCREEN
# ==========================================
if not st.session_state.app_started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>Swara Setu AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Select your preferred interface language<br>మీ యాప్ భాషను ఎంచుకోండి</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.ui_lang = st.selectbox("Language / భాష", ["English", "Telugu", "Hindi"], label_visibility="collapsed")
        st.write("")
        st.button("Launch App 🚀", on_click=start_app, type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# STEP 2: PROFESSIONAL WORKSPACE
# ==========================================
else:
    t = UI_TEXT[st.session_state.ui_lang]
    
    with st.sidebar:
        st.button(f"{t['settings']}", on_click=reset_app)

    st.markdown("<h1 class='hero-title'>Swara Setu AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='hero-subtitle'>{t['subtitle']}</p>", unsafe_allow_html=True)

    # Core Panel 1: Language Routing
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([5, 2, 5])
    with col1:
        source_language = st.selectbox(f"**{t['you_speak']}**", lang_names, key="src_dropdown")
    with col2:
        st.write("") 
        st.write("")
        st.button(t["swap"], on_click=swap_languages)
    with col3:
        target_language = st.selectbox(f"**{t['they_hear']}**", lang_names, key="tgt_dropdown")
    st.markdown('</div>', unsafe_allow_html=True)

    src_code = LANGUAGES[source_language]
    tgt_code = LANGUAGES[target_language]

    # Core Panel 2: Native Big Audio Button
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Streamlit's new native audio input creates a massive, fully clickable UI exactly like your sketch
    audio_value = st.audio_input(t['hold_speak'])

    if audio_value:
        audio_bytes = audio_value.read()
        temp_input_path = "temp_input.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_bytes)
            
        st.write("")

        if st.button(t["translate_btn"], type="primary"):
            
            if lottie_wave:
                st_lottie(lottie_wave, height=80, key="translating")
                
            with st.spinner(t['translating']):
                original_text, translated_text, result = process_audio(temp_input_path, src_code, tgt_code)

            if original_text and translated_text and result.endswith('.mp3'):
                st.success(t["success"])
                
                # Output using Streamlit's native info/success boxes with custom styling
                st.info(f"**Original ({source_language}):**\n\n{original_text}")
                st.success(f"**Translation ({target_language}):**\n\n{translated_text}")
                
                st.write("")
                st.audio(result, format="audio/mp3", autoplay=True) 
            else:
                st.error(f"Error: {result}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Custom Footer
    st.markdown("""
        <div class="designer-footer">
            <p>Designed by <a href="https://www.linkedin.com/in/dandabattula-manikanta" target="_blank">Manikanta</a></p>
        </div>
    """, unsafe_allow_html=True)


