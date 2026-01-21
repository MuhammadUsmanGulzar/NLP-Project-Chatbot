# Local RAG Chatbot (CCP Project)

A fully deployed **Retrieval-Augmented Generation (RAG)** chatbot using **Local LLaMA**, **FAISS**, and **FastAPI**.
Designed to meet university Complex Computing Problem (CCP) requirements.

## 📌 Project Overview
- **Model**: LLaMA (via Ollama) - completely offline.
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence-Transformers).
- **Vector DB**: FAISS (Facebook AI Similarity Search).
- **Backend**: FastAPI.
- **Frontend**: Streamlit.

## 🚀 Setup Instructions

### 1. Prerequisites
- **Python 3.9+** installed.
- **Ollama** installed and running.
  - Download from: [ollama.com](https://ollama.com)
  - Pull the model (run in terminal):
    ```bash
    ollama pull llama3
    ```
    *(Note: You can use `mistral` or others, just update `app/backend/main.py`)*

### 2. Installation
Clone the project and install dependencies:

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ How to Run

### Step 1: Start the Backend (API)
Open a terminal in the project root (`i:/NLP CCP/anti`) and run:

```bash
uvicorn app.backend.main:app --reload --port 8000
```
*You will see "Application startup complete".*

### Step 2: Start the Frontend (UI)
Open a **new** terminal in the project root and run:

```bash
streamlit run app/frontend/app.py
```
*The browser should open automatically at `http://localhost:8501`.*

## 💡 Usage Guide
1.  **Ingest Documents**:
    - Go to the sidebar in the Streamlit app.
    - Upload a PDF or TXT file.
    - Click **"Ingest Document"**.
    - Watch for the success message.
2.  **Chat**:
    - Type your question in the main chat box.
    - The bot will retrieve relevant chunks from your document and answer using LLaMA.
    - Expand "View Retrieved Context" to see what the bot read.

## 🏗️ Architecture (For Viva)

1.  **Ingestion Layer**:
    - **Component**: `app/backend/core/ingestion.py`
    - **Function**: Loads PDF/TXT, cleans text, and splits it into manageable chunks (sliding window).
2.  **Retrieval Layer**:
    - **Component**: `app/backend/core/retrieval.py`
    - **Embeddings**: Converts text chunks into vector embeddings using `SentenceTransformer`.
    - **Vector Store**: Stores vectors in a FAISS index for fast similarity search (`L2` distance).
3.  **Generation Layer**:
    - **Component**: `app/backend/core/generation.py`
    - **LLM**: Connects to the local Ollama instance (`/api/generate`).
    - **Prompting**: Injects retrieved context + user query into a structured prompt.
4.  **API Layer**:
    - **Component**: `app/backend/main.py` (FastAPI).
    - Exposes REST endpoints for the frontend to communicate with the logic layers.
5.  **Application Layer**:
    - **Component**: `app/frontend/app.py` (Streamlit).
    - Provides a user-friendly chat interface.

## 📂 Project Structure
```text
app/
├── backend/
│   ├── core/         # Core logic (RAG pipeline)
│   ├── main.py       # API Server
├── frontend/
│   ├── app.py        # UI
requirements.txt      # Dependencies
README.md             # Documentation
```
