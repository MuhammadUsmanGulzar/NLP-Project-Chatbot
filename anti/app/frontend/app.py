import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Local RAG Chatbot", page_icon="🤖")

st.title("🤖 Local RAG Chatbot (CCP)")

# Sidebar for Ingestion
with st.sidebar:
    st.header("📄 Document Ingestion")
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        if st.button("Ingest Document"):
            with st.spinner("Ingesting and Indexing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    if response.status_code == 200:
                        st.success(f"Success: {response.json().get('message')}")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/chat", json={"query": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "No response received.")
                    context = data.get("context", [])
                    
                    st.markdown(answer)
                    
                    with st.expander("View Retrieved Context"):
                        for i, chunk in enumerate(context):
                            st.write(f"**Chunk {i+1}:**")
                            st.info(chunk)
                            
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error from API: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
