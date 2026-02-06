from transformers import pipeline

# Load NER pipeline (Updated argument)
ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"   # ✅ instead of grouped_entities
)


def extract_entities(text):
    """
    Extract named entities from enterprise text
    """
    results = ner(text)

    entities = []
    for r in results:
        entities.append((r["entity_group"], r["word"]))

    return entities


if __name__ == "__main__":
    sample = "Alice manages Project X and revenue exceeded 50K in Q4."

    print("\n✅ Extracted Entities:\n")
    print(extract_entities(sample))
