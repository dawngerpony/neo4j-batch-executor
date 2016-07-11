from py2neo import Graph, Path
import time
import argparse

letters = "0123456789abcdef"

def connect():
    return Graph("http://localhost:7474/db/data/")

def get_statements_count():
    """ Generate the Cypher statements required to count the number of nodes
        batches by the first two characters of the UUID.
    """
    statements = []
    for first in letters:
        for second in letters:
            s = """MATCH (o:Organisation)
    WHERE o.uuid STARTS WITH "{}{}"
    RETURN count(o)
""".format(first, second)
            statements.append(s)
    return statements


def get_statements_add_identifier_node_statements():
    """ Generate the Cypher statements required to add UPPIdentifier nodes to organisations
        in batches without crashing Neo4j.
    """
    statements = []
    for first in letters:
        for second in letters:
            s = """MATCH (o:Organisation)
    WHERE o.uuid STARTS WITH "{}{}"
    MERGE (indent:Identifier:UPPIdentifier{{value:o.uuid}})-[:IDENTIFIES]->(o)
    RETURN count(indent)
""".format(first, second)
            statements.append(s)
    return statements


def execute_statements(graph, statements=[]):
    """ Execute a set of Cypher statements.
    """
    for s in statements:
        print s
        start = time.time()
        print graph.data(s)
        end = time.time()
        print "Query took {} seconds".format(end - start)

def parse_args():
    parser = argparse.ArgumentParser(description='Split expensive neo4j statements into batches.')
    parser.add_argument('op', choices=['count','upp'], help='the operation to execute')


def run(args):
    graph = connect()
    if args.op == "count":
        statements = get_statements_count()
    elif args.op == "upp":
        statements = get_statements_add_identifier_node_statements()
    start = time.time()
    execute_statements(graph, statements)
    end = time.time()
    print "Execution took {} seconds".format(end - start)


if __name__ == "__main__":
    run()
