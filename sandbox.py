#!/usr/bin/env python

letters = "0123456789abcdef"

# s = ""
# for c in letters:
#     s += "\"{}\",".format(c)
# letters = s.strip(',')

for l in letters:
    # statement = """WITH [{}] AS letters
    #     UNWIND letters as l
    #         MATCH (o:Organisation)
    #         WHERE o.uuid STARTS WITH l
    #         MERGE (indent:Identifier:UPPIdentifier{{value:o.uuid}})-[:IDENTIFIES]->(o)
    #         RETURN count(indent)
    # """.format(l)
    statement = """MATCH (o:Organisation)
    WHERE o.uuid STARTS WITH "{}"
    MERGE (indent:Identifier:UPPIdentifier{{value:o.uuid}})-[:IDENTIFIES]->(o)
    RETURN count(indent)
    """.format(l)
    print statement
