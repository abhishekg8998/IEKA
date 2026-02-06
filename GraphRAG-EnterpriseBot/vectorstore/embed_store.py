import os
import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

# =====================================
# CONFIG
# =====================================

COMPANY_NAME = "FinEdge Bank"

CHUNK_FOLDER = f"data/chunks/{COMPANY_NAME}"
INDEX_FOLDER = f"data/vector_index/{COMPANY_NAME}"

os.makedirs(INDEX_FOLDER, exist_ok=True)

INDEX_PATH = os.path.join(INDEX_FOLDER, "faiss.index")
META_PATH = os.path.join(INDEX_FOLDER, "metadata.json")

# =====================================
# LOAD EMBEDDING MODEL
# =====================================

print("Loading MPNet embedding model...")

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

print("Model loaded successfully ✅")

# =====================================
# LOAD CHUNKS
# =====================================

def load_chunks():

    all_chunks = []

    for file in os.listdir(CHUNK_FOLDER):

        if file.endswith(".json"):

            file_path = os.path.join(CHUNK_FOLDER, file)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                for item in data:
                    all_chunks.append(item)

    print("Total chunks loaded:", len(all_chunks))

    return all_chunks


# =====================================
# CREATE FAISS INDEX
# =====================================

def build_index():

    chunks = load_chunks()

    texts = [c["text"] for c in chunks]

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    dimension = embeddings.shape[1]

    # cosine similarity via inner product
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, INDEX_PATH)

    # Save metadata
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)

    print("\n✅ FAISS index created successfully!")
    print("Stored vectors:", index.ntotal)


# =====================================
# SEARCH FUNCTION
# =====================================

def search(query, top_k=5):

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for i in indices[0]:
        results.append(metadata[i])

    return results


# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    build_index()

    print("\nTest Search:")
    results = search("risk management issues")

    for r in results:
        print("-", r["text"][:100])
