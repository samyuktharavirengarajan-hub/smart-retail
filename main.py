import streamlit as st
import httpx
import os

# ========== CONFIG ==========
st.set_page_config(page_title="Gemini Chat App", page_icon="🤖")

# Use environment variable for safety
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ========== UI ==========
st.title("🤖 Gemini AI Chat")
st.write("Ask me anything!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

# ========== GEMINI CALL FUNCTION ==========
async def call_gemini(prompt):
    url = "https://api.gemini.com/v1/generate"  # Replace with real endpoint

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "max_tokens": 100
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        data = response.json()

    return data.get("text", "No response from Gemini")

# ========== HANDLE CHAT ==========
if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = st.run(call_gemini(user_input))
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

        result = response.json()

    # Return Gemini reply
    return JSONResponse(content={"reply": result.get("text", "No response")})
