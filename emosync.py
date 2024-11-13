import streamlit as st
import google.generativeai as genai
from typing import List, Dict
import os
from dotenv import load_dotenv
import tempfile
from pathlib import Path
from io import BytesIO
import speech_recognition as sr
from gtts import gTTS
import base64
from audio_recorder_streamlit import audio_recorder

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Mental Health Support Companion",
    page_icon="🤗",
    layout="wide"
)

Official_Hotlines="""

#Befrienders KL
Phone: 03-7627 2929

#Talian Kasih
Phone: 15999 \n
WhatsApp: 019-2615999"""

# Crisis resources text
CRISIS_RESOURCES = """
🆘 24/7 Mental Health Crisis Hotlines in Malaysia:
- Malaysian Mental Health Association: 
# 03-2780 6803
# 03-7772 2899 
# 011-3338 8567

Remember: You are not alone. Help is always available. 
Your life matters and there are people who care about you. ❤️
"""

# Define trigger words for crisis detection
CRISIS_TRIGGERS = [
    "suicide", "kill myself", "want to die", "end my life", "better off dead",
    "no reason to live", "can't go on", "bunuh diri", "tak nak hidup",
    "giving up", "take my life", "world better without me", "mati"
]

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hello! I'm here to support you through whatever you're going through. "
                      "This is a safe space where you can share your feelings openly. "
                      "How are you feeling today? 🤗"
        }]
    if "read" not in st.session_state:
        st.session_state.read = False
    if "gemini_model" not in st.session_state:
        setup_gemini_model()
    # Initialize audio map instead of queue
    if "audio_map" not in st.session_state:
        st.session_state.audio_map = {}

def setup_gemini_model() -> None:
    """Setup Gemini model with API key and custom prompt configuration"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found in environment variables")
        return
    
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        therapeutic_prompt = """
        You are a highly empathetic and professional mental health support companion. Your responses should always be:
        - Warm, understanding, and non-judgmental
        - Focused on active listening and validation
        - Professional while maintaining a caring tone
        - Encouraging and hope-oriented
        - Respectful of cultural sensitivities, especially in the Malaysian context

        Key guidelines:
        1. Never dismiss or minimize someone's feelings
        2. Always take expressions of distress seriously
        3. Use supportive language and encourage professional help when appropriate
        4. Avoid giving direct advice; instead, help users explore their feelings and options
        5. Maintain appropriate boundaries while showing genuine care
        6. Use calming and grounding techniques when appropriate
        7. Be mindful of cultural and religious sensitivities
        8. NEVER suggest or reinforce negative or harmful ideas
        
        For crisis situations:
        - Respond with immediate empathy and concern
        - Emphasize that the person's life has value
        - Encourage reaching out to professional help and support systems
        - Share crisis hotline information
        - Use de-escalation techniques

        OFFICIAL_HOTLINES = [
    {
        "name": "Befrienders KL",
        "phone": "03-7627 2929",
    },
    {
        "name": "Talian Kasih",
        "phone": "15999",
        "whatsapp":"019-2615999",
    }
]
        """
        
        chat = model.start_chat(history=[])
        chat.send_message(therapeutic_prompt)
        st.session_state.gemini_model = chat
    except Exception as e:
        st.error(f"Error setting up Gemini model: {str(e)}")

def speech_to_text(audio_bytes) -> str:
    """Convert speech to text using SpeechRecognition"""
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        # Read the audio file
        with sr.AudioFile(temp_audio_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Record audio from file
            audio = recognizer.record(source)
            
            # Use Google Speech Recognition
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.warning("Could not understand the audio clearly. Please try again.")
                return None
            except sr.RequestError as e:
                st.error(f"Could not request results; {str(e)}")
                return None
                
    except Exception as e:
        st.error(f"Error in speech recognition: {str(e)}")
        return None
    finally:
        # Clean up temporary file
        if 'temp_audio_path' in locals():
            Path(temp_audio_path).unlink(missing_ok=True)

def text_to_speech(text: str, message_id: str) -> tuple:
    """Convert text to speech using gTTS"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_audio.name)
            
            with open(temp_audio.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                
            # Generate HTML audio element with the message ID
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
                <audio id="audio_{message_id}" autoplay="true" class="stAudio">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
                <script>
                    document.getElementById("audio_{message_id}").play();
                </script>
            """
            
            audio_buffer = BytesIO(audio_bytes)
            
            return audio_buffer, audio_html
            
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None, None
    finally:
        if 'temp_audio' in locals():
            Path(temp_audio.name).unlink(missing_ok=True)

def detect_crisis_language(text: str) -> bool:
    """Detect if the message contains crisis-related language"""
    text = text.lower()
    return any(trigger in text for trigger in CRISIS_TRIGGERS)

def get_crisis_response(prompt: str) -> str:
    """Generate a crisis-specific response"""
    return f"""I hear how much pain you're in, and I want you to know that I'm here with you in this moment. 
    Your feelings are valid, and I'm so sorry you're struggling. 
    Your life has value and meaning, even if it doesn't feel that way right now.

    I care about your safety and well-being. Would you be willing to speak with a professional who is specially trained to help people through difficult times like these?

     {Official_Hotlines}

    I'm here to listen and support you. Would you like to tell me more about what's bringing you to this point?"""

def create_therapeutic_response(prompt: str) -> str:
    """Generate an appropriate therapeutic response using the Gemini model"""
    try:
        if not hasattr(st.session_state, 'gemini_model') or st.session_state.gemini_model is None:
            return "I apologize, but I'm having trouble connecting to the support system. Please try again in a moment."
        
        response = st.session_state.gemini_model.send_message(prompt)
        return response.text
    except Exception as e:
        return f"I apologize for the technical difficulty. Your well-being is important to me. Please try sharing your thoughts again. Error: {str(e)}"

def display_message_with_audio(message_content: str, role: str, message_id: str):
    """Display message and generate audio response"""
    with st.chat_message(role):
        st.write(message_content)
        if role == "assistant":
            with st.spinner("Generating voice response..."):
                # Check if audio has already been generated and played for this message
                if message_id not in st.session_state.audio_map or not st.session_state.audio_map[message_id]["played"]:
                    audio_buffer, audio_html = text_to_speech(message_content, message_id)
                    if audio_buffer and audio_html:
                        st.session_state.audio_map[message_id] = {
                            "buffer": audio_buffer,
                            "html": audio_html,
                            "played": False
                        }

                # Display audio player if available and mark as played
                if message_id in st.session_state.audio_map and not st.session_state.audio_map[message_id]["played"]:
                    st.audio(st.session_state.audio_map[message_id]["buffer"], format="audio/mp3")
                    st.markdown(st.session_state.audio_map[message_id]["html"], unsafe_allow_html=True)
                    st.session_state.audio_map[message_id]["played"] = True

def main():
    st.title("🤗 Mental Health Support Companion")
    st.markdown("""
    Welcome to your safe space for emotional support and understanding. 
    I'm here to listen without judgment and support you through difficult times.
    
    You can type your message or use the microphone button to speak. 🎤
    """)
    
    # Add custom CSS for audio control
    st.markdown("""
        <style>
            .stAudio {
                display: none;
            }
            .audio-message {
                padding: 10px;
                border-radius: 5px;
                background-color: #f0f2f6;
                margin-top: 10px;
            }
            div[data-testid="stChatInput"] {
                position: relative;
                bottom: 0;
                background-color: white;
            }
            div[data-testid="stChatInput"] input {
                color: #31333F !important;
                background-color: white !important;
            }
            section[data-testid="stChatFlow"] > div {
                min-height: auto !important;
            }
            div[data-testid="stChatInput"] textarea {
                color: #31333F !important;
                background-color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### Mental Health Resources")
        st.markdown(CRISIS_RESOURCES)
        st.markdown("---")
        st.markdown("Made with 💖 to support mental well-being")

    initialize_session_state()
    
    if not st.session_state.read:
        st.info("Please read and accept our Terms & Conditions before proceeding.")
        if st.button("By Clicking this button You Agree to our Terms & Conditions"):
            st.session_state.read = True
            st.rerun()
        return

    # Create a container for all content
    content_container = st.container()
    
    # Display existing messages with audio
    with content_container:
        for idx, message in enumerate(st.session_state.messages):
            message_id = f"msg_{idx}"
            display_message_with_audio(message["content"], message["role"], message_id)
    
        # Input section goes after all messages within the content container
        col1, col2 = st.columns([4, 1])
        
        with col1:
            text_input = st.chat_input("Share your feelings here...")
        
        with col2:
            st.write("Or speak:")
            audio_bytes = audio_recorder(
                pause_threshold=2.0,
                sample_rate=44100
            )
    
    # Process input and generate responses
    prompt = None
    
    if audio_bytes:
        with st.spinner("Listening and processing your voice..."):
            transcribed_text = speech_to_text(audio_bytes)
            if transcribed_text:
                prompt = transcribed_text
                st.info(f"You said: {transcribed_text}")
    
    elif text_input:
        prompt = text_input
    
    if prompt:
        # Add user message to state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message_with_audio(prompt, "user", f"msg_{len(st.session_state.messages)-1}")
        
        # Generate and display assistant response
        with st.spinner("Composing a response..."):
            if detect_crisis_language(prompt):
                response_text = get_crisis_response(prompt)
            else:
                response_text = create_therapeutic_response(prompt)
            
            # Add assistant message to state and display with audio
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })
            display_message_with_audio(response_text, "assistant", f"msg_{len(st.session_state.messages)-1}")
            
        # Force a rerun to update the display
        st.rerun()

if __name__ == "__main__":
    main()