# A LOCAL RETRIEVAL-AUGMENTED GENERATION (RAG) CHATBOT FOR SECURE DOCUMENT ANALYSIS

**Submitted by:** [Your Name]  
**University/College:** [Your University Name]  
**Course:** Complex Computing Problem (CCP)  
**Date:** [Current Date]

---

## 1. ABSTRACT
In the era of Large Language Models (LLMs), data privacy remains a critical concern. Cloud-based solutions like OpenAI and Gemini require sending sensitive data to external servers, which violates strict privacy policies for many organizations. This project implements a fully offline, privacy-preserving Chatbot using Retrieval-Augmented Generation (RAG). By leveraging local execution of LLaMA (via Ollama), FAISS for vector storage, and FastAPI for backend orchestration, the system allows users to query internal documents (PDFs/TXTs) without any data leaving the local network.

## 2. INTRODUCTION
### 2.1 Problem Statement
Generative AI allows for powerful conversational interfaces, but standard models hallucinate when asked about specific, non-public data. Fine-tuning models is computationally expensive. Furthermore, reliance on cloud APIs poses data security risks and recurring costs.
### 2.2 Objectives
*   To build a RAG pipeline that runs 100% locally.
*   To implement an efficient document ingestion system for PDFs and text files.
*   To utilize vector embeddings for semantic search (Retrieval) rather than keyword matching.
*   To provide a user-friendly chat interface for interacting with documents.
### 2.3 Scope
The project is limited to text-based documents and text-based answers. It uses open-source models (Llama 3, Gemma) optimized for consumer hardware.

## 3. LITERATURE REVIEW
### 3.1 Retrieval-Augmented Generation (RAG)
RAG combines the generative capabilities of LLMs with the accuracy of information retrieval. Lewis et al. (2020) demonstrated that RAG models outperform standard seq2seq models on knowledge-intensive tasks.
### 3.2 Vector Embeddings & FAISS
Dense vector indexes allow for semantic similarity search. FAISS (Facebook AI Similarity Search) is the industry standard for efficient similarity search and clustering of dense vectors.

## 4. SYSTEM ARCHITECTURE
### 4.1 Technology Stack
*   **LLM Engine**: Ollama (Llama 3 / Gemma 2B)
*   **Vector Database**: FAISS (Local CPU Index)
*   **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
*   **Backend Framework**: FastAPI (Python)
*   **Frontend Interface**: Streamlit

### 4.2 Data Flow
1.  **Ingestion**: User uploads a file. The system parses text and splits it into chunks (size=500 tokens).
2.  **Embedding**: Each chunk is converted to a vector and stored in FAISS.
3.  **Retrieval**: When a user asks a question, the query is vectorized, and the top-3 most similar chunks are retrieved.
4.  **Generation**: The retrieved chunks are appended to the system prompt. The LLM generates an answer based *only* on this context.

## 5. IMPLEMENTATION DETAILS
### 5.1 Ingestion Module (`ingestion.py`)
Handles parsing of `.pdf` files using `pypdf`. Implements sliding window chunking to maintain context overlap.
### 5.2 Retrieval Service (`retrieval.py`)
Uses `sentence-transformers` to encode text. FAISS `IndexFlatL2` is used for Euclidean distance calculation.
### 5.3 Generation Service (`generation.py`)
Connects to the local Ollama API (`localhost:11434`). A robust system prompt ensures the model does not hallucinate information outside the provided context.

## 6. TESTING AND RESULTS
### 6.1 Performance Testing
*   **Latency**: Average response time on `gemma:2b` is <5 seconds on CPU.
*   **Accuracy**: The system correctly answers questions contained within the uploaded policy documents.
### 6.2 Limitations
*   Initial model loading time can be slow on older hardware.
*   Context window size limits the number of documents that can be processed at once.

## 7. CONCLUSION
This project successfully demonstrates a functional, local RAG chatbot. It meets the requirement for a Complex Computing Problem by integrating multiple advanced components (Vector Search, LLM Inference, API Design) into a cohesive solution. Future work could include adding support for image parsing and citation highlighting.

## 8. REFERENCES
1.  Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*.
2.  Facebook Research. *FAISS: A library for efficient similarity search*.
3.  FastAPI Documentation. https://fastapi.tiangolo.com/
