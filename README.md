# 🏛️ Stoic-Chatbot: AI Wisdom Assistant

A Retrieval-Augmented Generation (RAG) chatbot designed to provide philosophical advice from ancient texts. This project uses vector embeddings to retrieve relevant insights from Stoic literature and serves them through a modern Streamlit interface.

## 🚀 Features
- **RAG Architecture**: Uses semantic search to find the most relevant Stoic teachings.
- **Vector Database**: Powered by **Qdrant** for high-performance similarity search.
- **AI-Powered**: Integrates with **OpenRouter** to access state-of-the-art LLMs.
- **Clean UI**: A minimalist Streamlit interface with a secure login flow.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Vector DB**: Qdrant
- **Embeddings**: FastEmbed (BGE-Small)
- **Orchestration**: LangChain
- **LLM**: OpenRouter (e.g., Mistral/Llama)

## 📖 How it Works
1. **Ingestion**: The system reads philosophical PDFs (like *The Daily Stoic*).
2. **Chunking & Embedding**: Text is split into meaningful chunks and converted into vectors.
3. **Retrieval**: When a user asks a question, Qdrant finds the most mathematically similar text chunks.
4. **Generation**: The LLM uses the retrieved context to formulate a personalized, Stoic response.



## 🏗️ Installation & Setup

1. **Clone the repo**:
   ```bash
   git clone [https://github.com/Jxyanth/Stoic-Chatbot.git](https://github.com/Jxyanth/Stoic-Chatbot.git)
   cd Stoic-Chatbot
