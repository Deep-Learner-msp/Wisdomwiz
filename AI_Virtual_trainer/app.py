import streamlit as st
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def generate_answer(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 2048,
        "temperature": 0.5,
        "n": 1,
        "messages": messages
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

st.title("WisdomWiz: AI & ML Unraveled")

st.write("🚀 Welcome to WisdomWiz: Your AI & ML Learning Companion! 🤖 I'm your friendly virtual mentor, here to guide you through the fascinating world of AI and ML. Together, we'll explore the essentials and unravel the math that powers these cutting-edge technologies. Feel free to dive into any topic, ask questions, or seek clarification. Let's embark on this enlightening journey together! 💡")

conversation_history = st.session_state.get("conversation_history", [])

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Enter your question or request:", value=st.session_state.user_input)

with col2:
    if st.button("Send"):
        if user_input:
            st.session_state.user_input = user_input
            messages = [
                {"role": "system", "content": "You are an AI and ML virtual trainer that teaches the basics and fundamentals of artificial intelligence and machine learning, including the math behind these concepts. Explain the topics in simple terms and answer user's questions or doubts., refuse to answer all the question except AI and ML, DL space, don't ever answer anything, just tell I'm here to teach you the AI"},
            ]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_input})

            answer = generate_answer(messages)
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": answer['choices'][0]['message']['content']})
            st.session_state.conversation_history = conversation_history

            st.session_state.user_input = ""

if st.button("Download Notes"):
    if conversation_history:
        with open("notes.txt", "w") as notes_file:
            for message in conversation_history:
                notes_file.write(f"{message['role'].capitalize()}: {message['content']}\n")

        st.download_button(
            label="Download Conversation as Notes",
            data=open("notes.txt", "rb").read(),
            file_name="notes.txt",
            mime="text/plain"
        )
    else:
        st.write("There is no conversation history to download.")

if "conversation_history" in st.session_state and st.session_state.conversation_history:
    st.subheader("Conversation History")

    st.markdown("""
    <style>
        .user {
            color: #1f77b4;
        }
        .assistant {
            color: #ff7f0e;
        }
    </style>
    """, unsafe_allow_html=True)

    for message in st.session_state.conversation_history:
        st.markdown(f"<p class='{message['role']}'><b>{message['role'].capitalize()}:</b> {message['content']}</p>", unsafe_allow_html=True)
