📄 Enterprise GraphRAG PDF Assistant

A chatbot that can:

✅ Upload any PDF
✅ Extract text
✅ Break into chunks
✅ Store chunks in Vector DB
✅ Extract entities into Neo4j Graph
✅ Retrieve both Graph + Vector context
✅ Answer using Gemini LLM
✅ Show UI in Streamlit

🏗️ Complete Architecture
PDF Upload
   ↓
Text Extraction
   ↓
Chunking
   ↓
Vector Embeddings (Semantic Search)
   ↓
Entity Extraction (NER)
   ↓
Neo4j Graph Storage (Relations)
   ↓
Hybrid Retrieval (Vector + Graph)
   ↓
LLM Answer Generation (Gemini)
   ↓
Streamlit Chat UI

✅ Folder Structure We Created
GraphRAG-EnterpriseBot/
│ README.md
│ requirements.txt
│
├── data/
│   ├── pdfs/
│   └── chats/
│
├── ingestion/
│   extract_text.py
│   chunk_docs.py
│
├── vectorstore/
│   embed_store.py
│
├── entity_extraction/
│   ner_entities.py
│
├── graph/
│   neo4j_utils.py
│   build_graph.py
│
├── retrieval/
│   hybrid_retriever.py
│
├── llm/
│   graph_rag_chain.py
│
└── ui/
    app.py