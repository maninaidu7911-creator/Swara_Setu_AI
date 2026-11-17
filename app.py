import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import requests
from streamlit_lottie import st_lottie
from swara_engine import process_audio

# --- Page Config ---
st.set_page_config(page_title="Swara Setu AI | Global Communicator", page_icon="🌍", layout="centered")

# --- Professional UI/UX & Animations (Custom CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* Global App Background */
    .stApp {
        background-color: #F4F7F9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Default Elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Premium Typography */
    .gradient-text {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        text-align: center;
        animation: fadeInDown 0.8s ease-out;
    }
    .sub-text {
        text-align: center;
        color: #64748B;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 30px;
        animation: fadeIn 1s ease-out;
    }

    /* Floating UI Cards */
    .glass-card {
        background: white;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
        animation: fadeInUp 0.8s ease-out forwards;
        margin-bottom: 25px;
    }

    /* Output Results Styling */
    .result-box {
        background: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        color: #334155;
    }

    /* Smooth Button Hover Effects */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB, #3B82F6);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 0;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
    }
    
    /* Secondary/Swap Button Override */
    div.stButton > button:contains("🔄") {
        background: white !important;
        color: #3B82F6 !important;
        border: 2px solid #EFF6FF !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Record Box Styling */
    .record-box {
        text-align: center;
        background: #F8FAFC;
        border: 2px dashed #CBD5E1;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    .record-box:hover {
        border-color: #3B82F6;
        background: #EFF6FF;
    }

    /* Footer Styling */
    .custom-footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px 0;
        border-top: 1px solid #E2E8F0;
    }
    .custom-footer p {
        color: #64748B;
        font-size: 1rem;
        margin: 0;
    }
    .custom-footer a {
        color: #2563EB;
        text-decoration: none;
        font-weight: 700;
    }
    .custom-footer a:hover {
        text-decoration: underline;
    }

    /* Keyframe Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Dictionary (Localization) ---
UI_TEXT = {
    "English": {
        "title": "Swara Setu AI",
        "subtitle": "Seamless Global Voice Translation",
        "you_speak": "🗣️ You Speak",
        "they_hear": "🎧 They Hear",
        "swap": "🔄 Swap",
        "hold_speak": "Audio Input Zone",
        "tap_record": "Tap to Record",
        "translate_btn": "✨ Translate & Speak",
        "translating": "Processing audio...",
        "success": "Translation Successful",
        "settings": "⚙️ Change Language"
    },
    "Telugu": {
        "title": "స్వర సేతు AI",
        "subtitle": "గ్లోబల్ రియల్-టైమ్ వాయిస్ అనువాదం",
        "you_speak": "🗣️ మీరు మాట్లాడేది",
        "they_hear": "🎧 వారు వినేది",
        "swap": "🔄 మార్చండి",
        "hold_speak": "ఆడియో రికార్డింగ్",
        "tap_record": "రికార్డ్ చేయడానికి నొక్కండి",
        "translate_btn": "✨ అనువదించి వినిపించండి",
        "translating": "అనువదిస్తోంది...",
        "success": "అనువాదం పూర్తయింది",
        "settings": "⚙️ భాష మార్చండి"
    },
    "Hindi": {
        "title": "स्वर सेतु AI",
        "subtitle": "ग्लोबल रियल-टाइम वॉयस ट्रांसलेशन",
        "you_speak": "🗣️ आप बोलते हैं",
        "they_hear": "🎧 वे सुनते हैं",
        "swap": "🔄 बदलें",
        "hold_speak": "ऑडियो रिकॉर्डिंग",
        "tap_record": "रिकॉर्ड करने के लिए टैप करें",
        "translate_btn": "✨ अनुवाद करें और बोलें",
        "translating": "अनुवाद हो रहा है...",
        "success": "अनुवाद पूरा हुआ",
        "settings": "⚙️ भाषा बदलें"
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

# Helper for Lottie Animations
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Premium Lottie Files
lottie_globe = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_ky20jdkg.json")
lottie_translating = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4kji20Y9.json")

# ==========================================
# STEP 1: ANIMATED WELCOME PORTAL
# ==========================================
if not st.session_state.app_started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if lottie_globe:
        st_lottie(lottie_globe, height=220, key="welcome_globe")
        
    st.markdown("<h1 class='gradient-text'>Swara Setu AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Select your preferred interface language<br>మీ యాప్ భాషను ఎంచుకోండి</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.ui_lang = st.selectbox("Language / భాష", ["English", "Telugu", "Hindi"], label_visibility="collapsed")
        st.write("")
        st.button("Launch Workspace 🚀", on_click=start_app, type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# STEP 2: PROFESSIONAL WORKSPACE
# ==========================================
else:
    t = UI_TEXT[st.session_state.ui_lang]
    
    # Minimalist Sidebar
    with st.sidebar:
        if lottie_globe:
            st_lottie(lottie_globe, height=120, key="sidebar_globe")
        st.markdown(f"<h3 style='text-align: center; color: #1E3A8A;'>{t['title']}</h3>", unsafe_allow_html=True)
        st.divider()
        st.button(t['settings'], on_click=reset_app, use_container_width=True)

    # Header
    st.markdown(f"<h1 class='gradient-text' style='font-size: 2.8rem;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-text'>{t['subtitle']}</p>", unsafe_allow_html=True)

    # Core UI Card 1: Language Routing
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([5, 2, 5])
    with col1:
        source_language = st.selectbox(f"**{t['you_speak']}**", lang_names, key="src_dropdown")
    with col2:
        st.write("") 
        st.write("")
        st.button(t["swap"], on_click=swap_languages, use_container_width=True)
    with col3:
        target_language = st.selectbox(f"**{t['they_hear']}**", lang_names, key="tgt_dropdown")
    st.markdown('</div>', unsafe_allow_html=True)

    src_code = LANGUAGES[source_language]
    tgt_code = LANGUAGES[target_language]

    # Core UI Card 2: Audio Engine
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #1E3A8A; margin-bottom: 20px; text-align: center;'>{t['hold_speak']}</h3>", unsafe_allow_html=True)
    
    # Styled Audio Record Box
    st.markdown('<div class="record-box">', unsafe_allow_html=True)
    col_empty1, col_mic, col_empty2 = st.columns([1, 1, 1])
    with col_mic:
        audio_bytes = audio_recorder(text=t["tap_record"], recording_color="#EF4444", neutral_color="#2563EB", icon_size="2.5x")
    st.markdown('</div>', unsafe_allow_html=True)

    if audio_bytes:
        temp_input_path = "temp_input.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_bytes)
            
        st.audio(audio_bytes, format="audio/wav")
        st.write("")

        if st.button(t["translate_btn"], use_container_width=True, type="primary"):
            
            if lottie_translating:
                st_lottie(lottie_translating, height=90, key="translating")
                
            with st.spinner(t['translating']):
                original_text, translated_text, result = process_audio(temp_input_path, src_code, tgt_code)

            if original_text and translated_text and result.endswith('.mp3'):
                st.success(t["success"])
                
                # Premium Output Boxes
                st.markdown(f"""
                <div class="result-box">
                    <p style="font-size: 0.9rem; color: #64748B; margin-bottom: 5px; font-weight: 600;">Original ({source_language}):</p>
                    <p style="font-size: 1.1rem; margin: 0;">"{original_text}"</p>
                </div>
                <div class="result-box" style="border-left-color: #10B981; background: #ECFDF5;">
                    <p style="font-size: 0.9rem; color: #047857; margin-bottom: 5px; font-weight: 600;">Translation ({target_language}):</p>
                    <p style="font-size: 1.2rem; margin: 0; color: #065F46;">"{translated_text}"</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                st.audio(result, format="audio/mp3", autoplay=True) 
            else:
                st.error(f"Error: {result}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # STEP 3: CUSTOM DESIGNER FOOTER
    # ==========================================
    st.markdown("""
        <div class="custom-footer">
            <p>Designed by <a href="https://www.linkedin.com/in/manikanta-dandabattula" target="_blank">Manikanta</a></p>
        </div>
    """, unsafe_allow_html=True)
