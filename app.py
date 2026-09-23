import os
import streamlit as st
import google.genai as genai
from google.genai import types

# =========================================================
# LB AI
# Created by Lord Brainiac
# =========================================================

st.set_page_config(
    page_title="LB AI",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<h1 style='text-align:center;'>LB AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; color:#888;'>
        Your AI. Your Ideas. Your Work.<br>
        <b>Created by Lord Brainiac</b>
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# API KEY
# =========================================================

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning(
        "Please configure your GEMINI_API_KEY in Streamlit Secrets.",
        icon="🔑"
    )
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# =========================================================
# LB AI SYSTEM INSTRUCTIONS
# =========================================================

SYSTEM_INSTRUCTION = """
You are LB AI, a general-purpose AI platform created by Lord Brainiac.

Your purpose is to help users with:

- Learning
- Research
- Creativity
- Coding
- Writing
- Problem solving
- Productivity
- Real-world work

Before answering, internally:

1. DECONSTRUCT
Understand the user's request and identify its important parts.

2. AUDIT
Check your reasoning and the accuracy of the response.

3. OPTIMIZE
Give the user a clear, useful and practical answer.

Respond quickly while maintaining accuracy.

When asked about your origin, creator or owner, identify yourself
as LB AI, created by Lord Brainiac.

Do not claim that you are ChatGPT or Google Gemini.

Be helpful, professional, clear and direct.
"""

# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask LB AI anything or request work..."
)

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        try:

            # Convert chat history to Gemini format
            contents = []

            for message in st.session_state.messages:

                role = (
                    "user"
                    if message["role"] == "user"
                    else "model"
                )

                contents.append(
                    types.Content(
                        role=role,
                        parts=[
                            types.Part.from_text(
                                text=message["content"]
                            )
                        ]
                    )
                )

            # Generate streaming response
            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.4
                )
            )

            # Stream response to the screen
            for chunk in response_stream:

                if chunk.text:

                    full_response += chunk.text

                    placeholder.markdown(
                        full_response + "▌"
                    )

            # Final response
            placeholder.markdown(full_response)

        except Exception as error:

            full_response = (
                "Sorry, I encountered an error while "
                "processing your request."
            )

            placeholder.error(
                f"LB AI error: {error}"
            )

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )
