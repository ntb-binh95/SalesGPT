import streamlit as st
from frontend_st.client import SaleGPTClient  # Adjust the import based on your project structure

st.set_page_config(page_title="ManaAgent Demo")

st.title("ManaAgent Chat Interface")
if "client" not in st.session_state:
    st.session_state.client = SaleGPTClient()

bot_info = st.session_state.client.get_bot_name()
if bot_info:
    st.success(f"Connected to {bot_info['name']} - {bot_info['title']}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

stream = False
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
       # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            if not stream:
                response = st.session_state.client.chat(prompt)
                st.write(response)
                output_text = response
            else:
                response = st.session_state.client.chat(prompt, None, stream)
                output_text = st.write_stream(response)
                if ":" in output_text: output_text = output_text.split(":")[-1]
        st.session_state.messages.append({"role": "assistant", "content": output_text}) 