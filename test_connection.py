#!/usr/bin/env python

# https://neo4j.com/developer/python/
def neo4j():
    from neo4j.v1 import GraphDatabase, basic_auth

    driver = GraphDatabase.driver("bolt://localhost:7474", auth=basic_auth("neo4j", "neo4j"))
    session = driver.session()

    session.run("CREATE (a:Person {name:'Arthur', title:'King'})")

    result = session.run("MATCH (a:Person) WHERE a.name = 'Arthur' RETURN a.name AS name, a.title AS title")
    for record in result:
      print("%s %s" % (record["title"], record["name"]))

    session.close()

# http://py2neo.org/v3/database.html
def py2neo():
    from py2neo import Graph, Path
    # graph = Graph()
    graph = Graph("http://localhost:7474/db/data/")
    print graph.data("MATCH (o:Organisation) RETURN o LIMIT 4")

if __name__ == "__main__":
    py2neo()
