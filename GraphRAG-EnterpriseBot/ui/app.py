import streamlit as st
import os
import sys

# ✅ Fix Import Path (VERY IMPORTANT)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion.extract_text import extract_text_from_pdf
from ingestion.chunk_docs import chunk_text
from vectorstore.embed_store import ingest_pdf_chunks, search
from graph.neo4j_utils import fetch_graph_context
from llm.graph_rag_chain import generate_answer

# ---------------------------------------------------
# Streamlit Config
# ---------------------------------------------------

st.set_page_config(page_title="Enterprise GraphRAG Bot", layout="wide")

st.title("📄 Enterprise GraphRAG PDF Assistant")
st.write("Upload any PDF and chat with it using Neo4j + Vector Search + Gemini.")

# ---------------------------------------------------
# Session Chat History
# ---------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------
# PDF Upload Section
# ---------------------------------------------------

st.header("📌 Upload a PDF")

uploaded_file = st.file_uploader("Upload your enterprise PDF", type=["pdf"])

if uploaded_file:

    # Save uploaded file
    pdf_path = os.path.join("data/pdfs", uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ PDF Uploaded Successfully!")

    # ---------------------------------------------------
    # Extract Text from PDF
    # ---------------------------------------------------

    raw_text = extract_text_from_pdf(pdf_path)

    st.write("📌 Extracted Text Length:", len(raw_text))

    if len(raw_text.strip()) < 50:
        st.error("❌ No readable text found in PDF. It may be scanned.")
        st.stop()

    # ---------------------------------------------------
    # Chunk the Text
    # ---------------------------------------------------

    chunks = chunk_text(raw_text)

    st.info(f"📌 Extracted {len(chunks)} chunks from PDF")

    # Preview First Chunk
    st.subheader("📍 Preview of First Chunk")
    st.write(chunks[0][:800])

    # ---------------------------------------------------
    # Store Chunks into Vector DB
    # ---------------------------------------------------

    ingest_pdf_chunks(chunks)

    st.success("✅ PDF Indexed Successfully! Now ask questions below.")

# ---------------------------------------------------
# Question Answer Section
# ---------------------------------------------------

st.header("💬 Ask a question from the uploaded PDF")

query = st.text_input("Type your question here:")

if st.button("Ask"):

    if not query.strip():
        st.warning("⚠️ Please type a valid question.")
        st.stop()

    # ---------------------------------------------------
    # Vector Retrieval
    # ---------------------------------------------------

    retrieved_chunks = search(query)

    doc_context = "\n\n".join(retrieved_chunks)

    # ---------------------------------------------------
    # Graph Retrieval (Neo4j Context)
    # ---------------------------------------------------

    graph_context = fetch_graph_context()

    # ---------------------------------------------------
    # Combine Full Context
    # ---------------------------------------------------

    full_context = f"""
DOCUMENT CONTEXT:
{doc_context}

GRAPH CONTEXT:
{graph_context}
"""

    # ---------------------------------------------------
    # Generate Answer using Gemini
    # ---------------------------------------------------

    answer = generate_answer(full_context, query)

    # Save to Chat History
    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("Bot", answer))

# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------

st.subheader("🗨 Chat History")

for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Bot:** {msg}")
