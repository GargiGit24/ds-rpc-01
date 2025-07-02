import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# FastAPI URL (adjust if needed)
API_URL = "http://127.0.0.1:8000/chat"

# Session State for storing user info
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.role = ""
    st.session_state.chat_history = []

# Sidebar login form
st.sidebar.title("🔐 Login")

if not st.session_state.authenticated:
    st.session_state.username = st.sidebar.text_input("Username")
    st.session_state.password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/login",
                auth=HTTPBasicAuth(st.session_state.username, st.session_state.password)
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.role = data["role"]
                st.session_state.authenticated = True
                st.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
            else:
                st.error("Invalid credentials.")
        except Exception as e:
            st.error(f"Login failed: {e}")

# Chat UI
if st.session_state.authenticated:
    st.title("💬 Role-Based Assistant")
    st.write(f"Welcome, **{st.session_state.username}**! (Role: `{st.session_state.role}`)")
        # Logout Button
    if st.sidebar.button("Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun() 


    user_input = st.text_input("Ask a question", key="chat_input")

    if st.button("Send") and user_input:
        try:
            response = requests.post(
                API_URL,
                auth=HTTPBasicAuth(st.session_state.username, st.session_state.password),
                json={"message": user_input}
            )

            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]

                # Show conversation
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Assistant", answer))

                for speaker, message in st.session_state.chat_history:
                    st.markdown(f"**{speaker}:** {message}")

                if sources:
                    st.markdown("**Sources:**")
                    for src in sources:
                        st.markdown(f"- `{src}`")
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Request failed: {e}")
