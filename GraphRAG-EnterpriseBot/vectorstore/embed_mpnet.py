from sentence_transformers import SentenceTransformer
import numpy as np

# ==========================
# LOAD EMBEDDING MODEL
# ==========================

print("Loading MPNet embedding model...")

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

print("Model loaded successfully ✅")


# ==========================
# GENERATE EMBEDDINGS
# ==========================

def generate_embedding(text):

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


# ==========================
# TEST
# ==========================

if __name__ == "__main__":

    sample = "Zenith Risk project faced regulatory challenges."

    emb = generate_embedding(sample)

    print("Embedding size:", len(emb))
