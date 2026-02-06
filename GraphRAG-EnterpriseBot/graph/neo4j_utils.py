from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "Abhishek@8998"


driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def fetch_graph_context():
    """Fetch sample graph info"""

    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n.name LIMIT 5")

        nodes = [record["n.name"] for record in result]

    return "Graph Nodes: " + ", ".join(nodes)
