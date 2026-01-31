import streamlit as st
import httpx
import os
import asyncio

st.set_page_config(page_title="Gemini Chat App", page_icon="🤖")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.title("🤖 Gemini AI Chat")
st.write("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

# ---------- Gemini API Call ----------
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
        result = response.json()   # ✅ Proper indentation

    return result.get("text", "No response from Gemini")

# ---------- Chat Handling ----------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = asyncio.run(call_gemini(user_input))
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
