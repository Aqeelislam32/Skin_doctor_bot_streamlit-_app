import os
from datetime import datetime
import streamlit as st
from speech import transcribe_audio
from vision import analyze_skin
from tts import text_to_speech
from utils import ensure_uploads_dir
from st_audiorec import st_audiorec
import asyncio
import sys
from dotenv import load_dotenv
from google.api_core import exceptions as google_exceptions
from groq import APIError

load_dotenv()
UPLOAD_DIR = ensure_uploads_dir("uploads")

CUSTOM_CSS = """
/* ---------- Global Styles & Variables ---------- */
:root {
    --radius: 12px;
    --shadow: 0px 1px 2px rgba(16, 24, 40, 0.05);
}

/* Streamlit Overrides */
body {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background-color: #F3F4F6; /* Soft Gray Background */
}

/* ---------- Header ---------- */
.app-header {
    text-align: center;
    margin-bottom: 2rem;
}
.app-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #111827; /* Heading Color */
    margin: 0;
    text-shadow: 2px 2px 5px red;
}
.app-header p {
    font-size: 1.1rem;
    color: #6B7280; /* Secondary Text Color */
    margin-top: 0.5rem;
}

/* ---------- Disclaimer ---------- */
.disclaimer-card {
    background-color: #FFF9E5;
    border: 1px solid #FFD66B;
    border-radius: var(--radius);
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
}
.disclaimer-card p {
    color: #7A2E0E;
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0;
}

/* ---------- Card Styles ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important; /* Clean White Card Background */
    border: 1px solid #E5E7EB !important; /* Light Border */
    border-radius: 12px;
    padding: 24px;
    box-shadow: var(--shadow);
}

/* Style the text inside the cards */
[data-testid="stVerticalBlockBorderWrapper"] h3 {
    color: #111827; /* Heading Color */
}

/* Blinking animation for the live recording indicator */
@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.5; }
    50% { transform: scale(1); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.5; }
}

/* ---------- RTL text for Urdu ---------- */
.rtl-text {
    direction: rtl;
    text-align: right;
}

[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p {
    color: #111827; /* Main text inside cards */
}
[data-testid="stVerticalBlockBorderWrapper"] p.secondary {
    color: #6B7280; /* Secondary Text Color */
}

/* ---------- Button Styles ---------- */
.stButton>button {
    background: #2563EB; /* Button Color */
    color: white !important;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    width: 100%;
    box-shadow: var(--shadow);
}
.stButton>button:hover {
    background: #1D4ED8; /* Darker Blue on hover */
}
[data-testid="stSidebar"] .stButton>button:hover {
    background: #DC2626 !important; /* Red on hover for sidebar buttons */
}

/* Override for Streamlit's info box to match card style */
.st-emotion-cache-1wmy9hl {
    background-color: #F9FAFB !important;
    color: #111827;
}

.st-emotion-cache-1wmy9hl .stMarkdown p {
    color: #111827 !important;
}

/* Sidebar Styles */
[data-testid="stSidebar"] {
    background-color: #F3F4F6 !important; /* Sky Blue */
}
"""

def format_analysis_html(response_text: str) -> str:
    escaped = response_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return escaped.replace("\n", "<br>")

# Set page config
st.set_page_config(
    page_title="AI Skin Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# Inject Custom CSS
st.markdown(f"""
<style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
{CUSTOM_CSS}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'transcript' not in st.session_state:
    st.session_state.transcript = "Your transcribed voice note will appear here."
if 'audio_response' not in st.session_state:
    st.session_state.audio_response = None
if 'keys_deleted' not in st.session_state:
    st.session_state.keys_deleted = False

# --- SIDEBAR ---
with st.sidebar:
    st.header("API Configuration")
    st.markdown("Enter your API keys here.")

    # Load keys from environment to pre-fill, but prioritize user input
    # If user clicked delete, keep the fields empty
    if st.session_state.keys_deleted:
        groq_api_key_env = ""
        gemini_api_key_env = ""
    else:
        groq_api_key_env = os.getenv("GROQ_API_KEY", "")
        gemini_api_key_env = os.getenv("GEMINI_API_KEY", "")

    groq_api_key = st.text_input("Groq API Key", type="password", value=groq_api_key_env, help="Aap apni key yahan se le sakte hain: https://console.groq.com/keys")
    gemini_api_key = st.text_input("Gemini API Key", type="password", value=gemini_api_key_env, help="Aap apni key yahan se le sakte hain: https://aistudio.google.com/app/apikey")

    # Set keys as environment variables for other modules to use
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
    if gemini_api_key:
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        st.session_state.keys_deleted = False # Reset if user enters a key

    if st.button("Delete API Keys", use_container_width=True):
        if "GROQ_API_KEY" in os.environ:
            del os.environ["GROQ_API_KEY"]
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        st.session_state.keys_deleted = True
        st.success("API keys have been cleared for this session.")
        st.rerun()

    st.markdown("---")
    st.subheader("Yeh App Kaise Kaam Karta Hai:")
    st.markdown("""
    1.  **Groq (Voice-to-Text)**: Your voice recording is converted into text using Groq's ultra-fast Whisper speech-to-text model.
    2.  **Gemini (Image Analysis)**: Your uploaded image and text description are analyzed using Google's Gemini AI model, which provides insights into the detected skin condition.

    3.  **gTTS (Text-to-Speech)**: The AI's response is converted into natural-sounding audio, allowing you to listen to the results.

    """)

# --- UI LAYOUT ---

# Header
st.markdown("""
<div class="app-header">
    <h1>🩺 AI Skin Health Assistant</h1>
    <p>Your personal AI-powered guide for preliminary skin health insights.</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-card">
    <p><strong>For Informational Purposes Only.</strong> This tool does not provide medical advice. Consult with a qualified healthcare professional for any health concerns.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    # --- CARD 1: VOICE RECORDING ---
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🎙️</span>
                <h3 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #111827;">Voice Recording</h3>
            </div>
            <span style="font-size: 0.9rem; color: #6B7280;">Record your symptoms</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="height: 10px; width: 10px; background-color: #3B82F6; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite;"></span>
                <span style="color: #2563EB; font-weight: 600; font-size: 0.95rem;">Ready to Record</span>
            </div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #111827; font-family: monospace;">00:00</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; padding: 20px 0; margin-bottom: 15px;">
            <svg width="140" height="80" viewBox="0 0 140 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="30" width="4" height="20" rx="2" fill="#1D4ED8">
                    <animate attributeName="height" values="20;50;20" dur="1.2s" repeatCount="indefinite" />
                    <animate attributeName="y" values="30;15;30" dur="1.2s" repeatCount="indefinite" />
                </rect>
                <rect x="24" y="20" width="4" height="40" rx="2" fill="#3B82F6">
                    <animate attributeName="height" values="40;70;40" dur="0.9s" repeatCount="indefinite" />
                    <animate attributeName="y" values="20;5;20" dur="0.9s" repeatCount="indefinite" />
                </rect>
                <rect x="38" y="35" width="4" height="10" rx="2" fill="#93C5FD">
                    <animate attributeName="height" values="10;30;10" dur="1.5s" repeatCount="indefinite" />
                    <animate attributeName="y" values="35;25;35" dur="1.5s" repeatCount="indefinite" />
                </rect>
                <rect x="52" y="15" width="4" height="50" rx="2" fill="#1E40AF">
                    <animate attributeName="height" values="50;75;50" dur="1.1s" repeatCount="indefinite" />
                    <animate attributeName="y" values="15;2.5;15" dur="1.1s" repeatCount="indefinite" />
                </rect>
                <rect x="66" y="25" width="4" height="30" rx="2" fill="#2563EB">
                    <animate attributeName="height" values="30;60;30" dur="0.8s" repeatCount="indefinite" />
                    <animate attributeName="y" values="25;10;25" dur="0.8s" repeatCount="indefinite" />
                </rect>
                <rect x="80" y="35" width="4" height="10" rx="2" fill="#93C5FD">
                    <animate attributeName="height" values="10;40;10" dur="1.4s" repeatCount="indefinite" />
                    <animate attributeName="y" values="35;20;35" dur="1.4s" repeatCount="indefinite" />
                </rect>
                <rect x="94" y="20" width="4" height="40" rx="2" fill="#3B82F6">
                    <animate attributeName="height" values="40;65;40" dur="1s" repeatCount="indefinite" />
                    <animate attributeName="y" values="20;7.5;20" dur="1s" repeatCount="indefinite" />
                </rect>
                <rect x="108" y="30" width="4" height="20" rx="2" fill="#1D4ED8">
                    <animate attributeName="height" values="20;45;20" dur="1.3s" repeatCount="indefinite" />
                    <animate attributeName="y" values="30;17.5;30" dur="1.3s" repeatCount="indefinite" />
                </rect>
            </svg>
        </div>
        """, unsafe_allow_html=True)

        audio_bytes = st_audiorec()

        st.markdown("<p class='secondary' style='margin-top: 20px;'>(Optional) Type additional details</p>", unsafe_allow_html=True)
        typed_text = st.text_area(
            "e.g., 'I have a red, itchy rash on my arm that appeared 3 days ago...'",
            label_visibility="collapsed"
        )

    # --- CARD 2: IMAGE UPLOAD ---
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 22px;">🖼️</span>
                <h3 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #111827;">Image Upload</h3>
            </div>
            <span style="font-size: 0.9rem; color: #6B7280;">Recommended: 3 angles</span>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_image = st.file_uploader(
            "Upload a clear, well-lit photo of the skin area.",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        if uploaded_image is not None:
            st.image(uploaded_image, use_container_width=True)

    analyze_button = st.button("Analyze Skin Condition", type="primary", use_container_width=True)

with col2:
    with st.container(border=True): 
        st.markdown("### Speech-to-Text")
        st.markdown(f"**[{datetime.now().strftime('%I:%M:%S %p')}]** {st.session_state.transcript}")

        st.divider()

        st.markdown("## AI Analysis")
        if st.session_state.analysis:
            st.markdown(st.session_state.analysis, unsafe_allow_html=True)
        else:
            st.info("The AI's analysis will be displayed here after you submit your details.")

        st.divider()

        st.markdown("### Audio Summary")
        if st.session_state.audio_response:
            st.audio(st.session_state.audio_response, autoplay=True)
        else:
            st.write("The audio summary will appear here.")


# --- BACKEND LOGIC ---
if analyze_button:
    # Check for API keys before proceeding
    if not os.getenv("GROQ_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        st.warning("Kripya sidebar mein Groq aur Gemini API keys enter karein.")
    elif uploaded_image is None:
        st.warning("Please upload a skin image first.")
    else:
        with st.spinner("Analyzing... This may take a moment."):
            image_path = os.path.join(UPLOAD_DIR, uploaded_image.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            patient_text = ""
            if audio_bytes:
                try:
                    audio_path = os.path.join(UPLOAD_DIR, "input_audio.wav")
                    with open(audio_path, "wb") as f:
                        f.write(audio_bytes)
                    patient_text = transcribe_audio(audio_path)
                    st.session_state.transcript = patient_text
                except APIError as e:
                    st.error(f"Groq (Voice-to-Text) API Error: {e.message}")
                    st.warning("Aapki voice transcribe nahi ho saki. Shayad API key galat hai ya uski limit khatam ho gayi hai. Kripya sidebar mein check karein.")
                    st.session_state.transcript = "Voice transcription failed due to API error."
                except Exception as e:
                    st.warning(f"Voice transcription fail ho gayi. Agar aapne text type kiya hai to use istemal kiya jayega. ({e})")
                    st.session_state.transcript = "Voice transcription failed."

            if not patient_text and typed_text:
                patient_text = typed_text
                st.session_state.transcript = patient_text

            if not patient_text:
                patient_text = "No description provided by the patient."
                st.session_state.transcript = patient_text

            try:
                ai_response = analyze_skin(image_path, patient_text)
                st.session_state.analysis = ai_response 

                audio_out_path = text_to_speech(ai_response, out_path=os.path.join(UPLOAD_DIR, "response.mp3"))
                st.session_state.audio_response = audio_out_path

            except google_exceptions.PermissionDenied as e:
                st.error("Gemini API Error: Invalid API Key (401 UNAUTHENTICATED).")
                st.warning("Aapki Gemini API key galat hai ya sahi se load nahi hui. Kripya sidebar mein sahi key enter karein.")
                st.session_state.analysis = "Error: Invalid Gemini API Key."
            except google_exceptions.ResourceExhausted as e:
                st.error("Gemini API Error: Quota Exceeded.")
                st.warning("Aapki Gemini API key ki free limit shayad khatam ho gayi hai. Kripya nayi key istemal karein.")
                st.session_state.analysis = "Error: Gemini API quota exceeded."
            except Exception as e:
                st.error(f"Analysis ke dauran ek error aayi: {e}")
                st.session_state.analysis = f"Error during analysis: {e}"

        st.rerun()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
