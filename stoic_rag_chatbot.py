from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from fastembed import TextEmbedding
from openai import OpenAI
import streamlit as st

# --- Configuration ---
collection_name = "stoic_wisdom"  # Defined globally to fix NameError
PDF_PATH = "C:/Users/balak/Downloads/The Daily Stoic.pdf"
OPENROUTER_KEY = "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"

# --- Resource Caching ---
@st.cache_resource
def get_qdrant_client():
    return QdrantClient(path="./qdrant_db")

@st.cache_resource
def get_embedder():
    # Cache the model so it doesn't reload every time
    return TextEmbedding(cache_dir="./models_cache")

client = get_qdrant_client()
embedder = get_embedder()

# --- Step 1 & 2: Database Initialization ---
if not client.collection_exists(collection_name):
    print("Database not found. Creating and uploading for the first time...")
    
    # 1. Load and Chunk
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 2. Create Collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
    # 3. Generate Embeddings and Store
    print("Generating embeddings... this might take a minute.")
    vectors = [list(embedder.embed(chunk.page_content))[0] for chunk in chunks]

    client.upload_collection(
        collection_name=collection_name,
        vectors=vectors,
        payload=[{"text": chunk.page_content} for chunk in chunks],
        ids=list(range(len(chunks)))
    )
    print("Upload complete!")
else:
    print("Database found! Skipping PDF processing and starting chat...")

# --- Step 3: Define Hybrid Search ---
def hybrid_search(query, top_k=5):
    query_vector = list(embedder.embed(query))[0]
    
    # query_points is the standard for 2026 local mode
    search_results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k
    ).points
    
    context = "\n\n".join([r.payload["text"] for r in search_results])
    return context

# --- Step 4: Chat with OpenRouter ---
openai_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

def ask_stoic_bot(query):
    context = hybrid_search(query)
    response = openai_client.chat.completions.create(
        model="openrouter/hunter-alpha",
        messages=[
            {"role": "system", "content": "You are a Stoic philosophy assistant. Answer with wisdom from Stoicism and refer to the context provided."},
            {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"}
        ]
    )
    if response and response.choices:
        return response.choices[0].message.content
    else:
        return "The Stoic masters are silent right now. Try asking again in 10 seconds."

# --- Example Run (Terminal Testing) ---
if __name__ == "__main__":
    print("\n--- Stoic Wisdom AI is Online ---")
    while True:
        user_question = input("You: ")
        if user_question.lower() in ['exit', 'quit']:
            break
        print("\nSearching the texts...")
        answer = ask_stoic_bot(user_question)
        print(f"\nStoic Bot: {answer}\n")
        print("-" * 30)