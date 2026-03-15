import streamlit as st
from stoic_rag_chatbot import ask_stoic_bot

# --- Page Config ---
st.set_page_config(page_title="Stoic Wisdom", page_icon="🏛️")

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Minimalist CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { border-radius: 10px; width: 100%; height: 3em; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏛️ Stoic Access")
    
    email = st.text_input("Gmail", value="user@gmail.com")
    password = st.text_input("Password", type="password")
    
    if st.button("Grant Chat Access"):
        if email == "user@gmail.com" and password == "user":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials.")

# --- CHAT INTERFACE ---
else:
    st.title("🌿 Stoic Guide")
    st.caption("Seek peace in the present moment.")

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Logic
    if prompt := st.chat_input("What is on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = ask_stoic_bot(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})