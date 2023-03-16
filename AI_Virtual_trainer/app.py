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



page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1554034483-04fda0d3507b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80");
background-size: 150%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://cdn.discordapp.com/attachments/1008571172792828055/1085929609226358865/mspraja_image_for_brain_related_image_with_enlightening_knowled_d45d9e54-a0aa-49e0-927b-3d0705492d16.png");
background-size: 100%;
background-position: top left; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
.title {{
    color: #ffffff;
}}
.tagline {{
    color: #f0f0f0;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar" style="padding-top: 10px;"><h1 class="title">WisdomWiz</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar tagline">🚀 Your AI & ML Learning Companion!</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<img src="https://purepng.com/public/uploads/large/purepng.com-state-street-logologobrand-logoiconslogos-251519938342d6s4u.png" width="150" style="center: absolute; top: 0; left: 0;">', unsafe_allow_html=True)




# Sidebar
# Main content
with st.container():
    st.markdown('<div class="center"><h1>Ask me anything about AI & ML</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""
        user_input = st.text_input("Enter your question or request:", value=st.session_state.user_input)
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    conversation_history = st.session_state.conversation_history

    with col2:
        if st.button("Send"):
            if user_input:
                st.session_state.user_input = user_input
                messages = [
                    {"role": "system", "content": "I want you act as AI and ML virtual trainer that teaches from basic fundamentals to Advanced level of artificial intelligence and machine learning, deep learning and AI Scope, including the math behind these concept and with formulas and technical deatails and answer all the complex queries as well, never tell that is beyond my scope, you are professional AI reseracher. and Explain the topics very professionally and answer user's questions or doubts, don't answer any other questions like any other technologies or any general info as well, you should refuse all those queries, because you have created to help learners to know the AI. if anyone asks anything apart from AI tell my duty is to help people to learn AI efficiently "},
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

    if "conversation_history" in st.session_state and len(st.session_state.conversation_history) > 0:
        st.subheader("Conversation History")
        st.markdown("""
        <style>
            .user {
                color: #0d3d56;
            }
            .assistant {
                color: #a0522d;
            }
        </style>
        """, unsafe_allow_html=True)

        for message in conversation_history:
            st.markdown(f"<p class='{message['role']}'><b>{message['role'].capitalize()}:</b> {message['content']}</p>", unsafe_allow_html=True)
