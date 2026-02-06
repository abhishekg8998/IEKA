import os
import json
from docx import Document
from sentence_transformers import SentenceTransformer, util
import nltk

# ===============================
# NLTK SETUP
# ===============================

nltk.download("punkt")

from nltk.tokenize import sent_tokenize

# ===============================
# CONFIG
# ===============================

COMPANY_NAME = "FinEdge Bank"

INPUT_FOLDER = f"data/pdfs/{COMPANY_NAME}"
OUTPUT_FOLDER = f"data/chunks/{COMPANY_NAME}"

SIMILARITY_THRESHOLD = 0.75

# Load embedding model (semantic similarity)
model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# TEXT EXTRACTION
# ===============================

def extract_text(file_path):

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""

# ===============================
# SEMANTIC CHUNKING
# ===============================

def semantic_chunk(text):

    sentences = sent_tokenize(text)

    if len(sentences) == 0:
        return []

    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):

        similarity = util.cos_sim(embeddings[i-1], embeddings[i]).item()

        if similarity >= SIMILARITY_THRESHOLD:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    # add last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# ===============================
# PROCESS FILES
# ===============================

def process_files():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    all_chunks = []

    print("\n====================================")
    print(f"🏦 Processing Company: {COMPANY_NAME}")
    print("====================================\n")

    for root, dirs, files in os.walk(INPUT_FOLDER):

        for file_name in files:

            if file_name.endswith((".txt", ".docx")):

                file_path = os.path.join(root, file_name)

                print(f"Processing: {file_name}")

                text = extract_text(file_path)

                if not text.strip():
                    print("⚠️ Empty file skipped")
                    continue

                chunks = semantic_chunk(text)

                structured = []

                for i, chunk in enumerate(chunks):

                    data = {
                        "company": COMPANY_NAME,
                        "source_file": file_name,
                        "chunk_id": i,
                        "text": chunk
                    }

                    structured.append(data)
                    all_chunks.append(data)

                output_path = os.path.join(
                    OUTPUT_FOLDER,
                    file_name.replace(".txt", "").replace(".docx", "") + "_semantic_chunks.json"
                )

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(structured, f, indent=4)

                print("✅ Chunks created:", len(structured))
                print("💾 Saved:", output_path)
                print()

    print("====================================")
    print("🎉 Chunking Completed!")
    print("Total Chunks Stored:", len(all_chunks))
    print("Saved Inside:", OUTPUT_FOLDER)
    print("====================================\n")

# ===============================
# RUN
# ===============================

if __name__ == "__main__":
    process_files()
