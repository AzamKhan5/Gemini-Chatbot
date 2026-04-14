import streamlit as st
import google.generativeai as genai

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# App UI
st.title("💬 Gemini AI Chatbot")

# Input box
user_input = st.text_input("You:", key="input")
submit = st.button("Send")

# When user sends message
if submit and user_input:
    # Save user message
    st.session_state.messages.append(("You", user_input))

    # Display user message
    st.write(f"**You:** {user_input}")

    # Send message with streaming
    response = st.session_state.chat.send_message(user_input, stream=True)

    st.write("**Gemini:**")
    response_placeholder = st.empty()

    full_response = ""

    # Stream response (live typing effect)
    for chunk in response:
        if chunk.text:
            full_response += chunk.text
            response_placeholder.markdown(full_response)

    # Save Gemini response
    st.session_state.messages.append(("Gemini", full_response))

# Chat history
st.subheader("📜 Chat History")

for sender, message in st.session_state.messages:
    st.write(f"**{sender}:** {message}")
