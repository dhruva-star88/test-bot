import os
import streamlit as st
from langchain.llms import HuggingFaceHub

# Initialize Hugging Face API
API_KEY = os.getenv("Chat-bot")
llm = HuggingFaceHub(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    huggingfacehub_api_token=API_KEY
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("Chatbot with Hugging Face Model")
st.sidebar.title("Instructions")
st.sidebar.info(
    """
     This is a simple chatbot interface created with Streamlit.
    Type your message in the input box and press Enter to chat.
    """
)
def clean_response(user_input, response):
    """
    Remove the user's input from the bot's response if it's repeated.
    """
    if response.lower().startswith(user_input.lower()):
        return response[len(user_input):].strip()
    return response.strip()

# Input form for user
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")

# If user sends a message
if submitted and user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response
    with st.spinner("Thinking..."):
        raw_response = llm(user_input)
        bot_response = clean_response(user_input, raw_response)

    # Append bot response to chat history
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")
