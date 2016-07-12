#!/usr/bin/env python

from py2neo import Graph, Path
import time
import argparse

letters = "0123456789abcdef"

def connect(url):
    print "URL: {}".format(url)
    return Graph(url)

def get_statements_count(node_type="Organisation"):
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


def get_statements_add_uppidentifier_node_statements(node_type="Organisation"):
    """ Generate the Cypher statements required to add UPPIdentifier nodes to organisations
        in batches without crashing Neo4j.
    """
    statements = []
    for first in letters:
        for second in letters:
            s = """MATCH (n:{})
    WHERE n.uuid STARTS WITH "{}{}"
    MERGE (indent:Identifier:UPPIdentifier{{value:n.uuid}})-[:IDENTIFIES]->(n)
    RETURN count(indent)
""".format(node_type, first, second)
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
    parser.add_argument('op', choices=['count_nodes','add_upp_identifiers'], help='the operation to execute')
    parser.add_argument('--node-type', default='Organisation', choices=['Organisation'], help='the node type')
    parser.add_argument('--neo-url', default='http://localhost:7474/db/data/', help='the Neo4j URL')
    return parser.parse_args()

def run(args):
    graph = connect(args.neo_url)
    statements = []
    if args.op == 'count_nodes':
        statements = get_statements_count()
    elif args.op == 'add_upp_identifiers':
        statements = get_statements_add_identifier_node_statements()
    else:
        print "Unknown operation '{}'".format(args.op)
    start = time.time()
    execute_statements(graph, statements)
    end = time.time()
    print "Execution took {} seconds".format(end - start)


if __name__ == '__main__':
    run(parse_args())
