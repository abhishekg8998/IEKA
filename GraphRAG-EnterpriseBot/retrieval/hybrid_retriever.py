from neo4j import GraphDatabase
from vectorstore.embed_store import search

# Neo4j connection
NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Abhishek@8998"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def graph_retrieve(entity_name):
    """
    Retrieve relationships from Neo4j graph
    """
    query = """
    MATCH (e:Entity {name:$name})
    OPTIONAL MATCH (e)-[r]->(n)
    RETURN e.name AS entity, type(r) AS relation, n.name AS connected
    """

    with driver.session() as session:
        results = session.run(query, name=entity_name)

        output = []
        for record in results:
            output.append(
                f"{record['entity']} -[{record['relation']}]-> {record['connected']}"
            )

    return output


def hybrid_retrieve(query):
    """
    Combine Graph Retrieval + Vector Search
    """
    print("\n🔍 Hybrid Retrieval Running...\n")

    # Vector search
    vector_results = search(query)

    # Graph search (simple: use query itself as entity)
    graph_results = graph_retrieve("Alice")

    return {
        "vector_results": vector_results,
        "graph_results": graph_results
    }


if __name__ == "__main__":
    q = "Who manages Project X?"

    results = hybrid_retrieve(q)

    print("\n✅ VECTOR RESULTS:\n", results["vector_results"])
    print("\n✅ GRAPH RESULTS:\n", results["graph_results"])
