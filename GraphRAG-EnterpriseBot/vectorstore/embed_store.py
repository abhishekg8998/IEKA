from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks_db = []
embeddings_db = []


def ingest_pdf_chunks(chunks):
    global chunks_db, embeddings_db

    chunks_db.clear()
    embeddings_db.clear()

    for chunk in chunks:
        emb = model.encode(chunk).tolist()
        chunks_db.append(chunk)
        embeddings_db.append(emb)

    return True


def search(query, top_k=3):
    if len(chunks_db) == 0:
        return ["⚠️ No chunks stored yet. Upload a PDF first."]

    query_emb = model.encode(query).tolist()

    sims = cosine_similarity([query_emb], embeddings_db)[0]
    top_indices = sims.argsort()[-top_k:][::-1]

    return [chunks_db[i] for i in top_indices]
