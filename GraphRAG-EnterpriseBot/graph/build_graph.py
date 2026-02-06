from neo4j import GraphDatabase
from entity_extraction.ner_entities import extract_entities

# Neo4j Connection
NEO4J_URI = "bolt://127.0.0.1:7687"

NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Abhishek@8998"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def insert_entities_to_graph(text):
    """
    Extract entities from text and insert them into Neo4j
    """

    entities = extract_entities(text)

    with driver.session() as session:
        for label, name in entities:
            session.run(
                """
                MERGE (e:Entity {name:$name})
                SET e.type = $label
                """,
                name=name,
                label=label
            )

    print("✅ Entities inserted into Neo4j successfully!")


if __name__ == "__main__":
    sample_text = "Alice manages Project X and revenue exceeded 50K in Q4."

    insert_entities_to_graph(sample_text)

    driver.close()
