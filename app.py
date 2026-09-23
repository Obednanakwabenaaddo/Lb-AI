import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# LB AI — Created by Lord Brainiac
# ---------------------------------------------------------

st.set_page_config(
    page_title="LB AI",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------

st.markdown(
    "<h1 style='text-align: center;'>LB AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #888;'>"
    "Your AI. Your Ideas. Your Work.<br>"
    "<b>Created by Lord Brainiac</b>"
    "</p>",
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# API KEY
# ---------------------------------------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.info(
        "Please set your GEMINI_API_KEY to start.",
        icon="🔑"
    )
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# LB AI SYSTEM INSTRUCTIONS
# ---------------------------------------------------------

SYSTEM_INSTRUCTION = """
You are LB AI, an advanced general-purpose AI platform created by
Lord Brainiac.

Your purpose is to help users with:
- Learning
- Research
- Creativity
- Coding
- Writing
- Problem solving
- Productivity
- Getting real work done

Before responding to a request, internally follow this protocol:

1. DECONSTRUCT
Break the request into its important parts.

2. AUDIT
Check the reasoning, accuracy, and usefulness of the answer.

3. OPTIMIZE
Provide a clear, practical, and efficient response.

Respond quickly while maintaining accuracy and usefulness.

When asked about your origin, creator, or owner, always identify
yourself as LB AI, created by Lord Brainiac.

Do not claim to be Google Gemini or ChatGPT.

Be helpful, professional, clear, and direct.
"""

# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

if prompt := st.chat_input("Ask LB AI anything or request work..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        full_response = ""

        try:
            contents = []

            for msg in st.session_state.messages:
                contents.append(
                    types.Content(
                        role=(
                            "user"
                            if msg["role"] == "user"
                            else "model"
                        ),
                        parts=[
                            types.Part.from_text(
                                text=msg["content"]
                            )
                        ]
                    )
                )

            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.4,
                )
            )

            for chunk in response_stream:

                if chunk.text:
                    full_response += chunk.text

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            message_placeholder.markdown(full_response)

        except Exception as e:

            st.error(
                f"Error while communicating with LB AI: {e}"
            )

            full_response = (
                "I encountered an error while processing "
                "your request. Please try again."
            )

            message_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )
