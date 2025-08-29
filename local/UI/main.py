import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="RAG Chatbot Demo", layout="centered")

# Title
st.title("💬 Hỗ trợ vay vốn trong ngân hàng")
st.caption("Hãy đặt câu hỏi. Chatbot sẽ tìm kiếm ngữ cảnh liên quan và tạo ra phản hồi.")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask me anything..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from RAG
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            api_url = "http://localhost:8000/retrieve"  # Change to your actual API endpoint from API Gateway
            response = requests.post(api_url, json={"query": user_input})
            if response.status_code == 200:
                rag_response = response.json().get("response", "")
            else:
                rag_response = "Sorry, I couldn't retrieve a response from the API."
            st.markdown(rag_response)

    # Append assistant message
    st.session_state.messages.append({"role": "assistant", "content": rag_response})
