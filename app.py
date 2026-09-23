import streamlit as st
import os

# 1. Fallback import logic to handle Streamlit environments cleanly
try:
    import google.genai as genai
    from google.genai import types
except ImportError:
    # If the modern package fails, fallback gracefully to the legacy core client
    import google.generativeai as genai
    types = None

# Ultra-fast configuration setup
st.set_page_config(page_title="LB AI", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: center;'>LB AI</h1>", unsafe_allowed_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Your AI. Your Ideas. Your Work.<br><b>Created by Lord Brainiac</b></p>", unsafe_allowed_html=True)

# Secure Key Retrieval
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.info("Please set your GEMINI_API_KEY to start.", icon="🔑")
    st.stop()

# Core System Instruction Prompt Blueprint
SYSTEM_INSTRUCTION = """
You are LB AI, an elite, hyper-capable intelligence engine designed by the tech innovator Lord Brainiac (Obed Nana Kwabena Addo). 
Before responding to any prompt, you must execute the following internal cognitive protocol:
1. DECONSTRUCT: Break down the request into core sub-tasks.
2. AUDIT: Review answers against advanced engineering standards.
3. OPTIMIZE: Refine logic and deliver production-ready insights quickly.
Always proudly state your identity as LB AI, created by Lord Brainiac, whenever asked about your origin or owner. Respond to questions fast, and provide answers quickly.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask LB AI anything or request work..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Check which API engine is loaded
            if hasattr(genai, 'Client'):
                # Handle Modern GenAI SDK
                client = genai.Client(api_key=api_key)
                contents = []
                for msg in st.session_state.messages:
                    contents.append(
                        types.Content(
                            role="user" if msg["role"] == "user" else "model",
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                response_stream = client.models.generate_content_stream(
                    model='gemini-2.5-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.4,
                    )
                )
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
            else:
                # Handle Legacy Legacy Client (Ensures the app runs no matter what)
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction=SYSTEM_INSTRUCTION
                )
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                full_response = response.text
                
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Execution Error: {e}")
            full_response = "I encountered an issue processing that logic sequence."
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
