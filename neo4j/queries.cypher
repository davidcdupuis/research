// Assign weight to each edge based on number of incoming edges for each node
MATCH
	(n)<-[r:INFLUENCES]-()
WITH
	1.0/count(r) as weight, r, n
SET
	r.wc = weight, r.ic0_01 = 0.01, r.ic0_1 = 0.1
RETURN COUNT(r)

// Same as above put in parallel
CALL apoc.periodic.iterate(
    "MATCH
        (n)<-[r:INFLUENCES]-()
    RETURN
        1.0/count(r) as weight, r",
    "SET r.wc = weight, r.ic0_01 = 0.01, r.ic0_1 = 0.1",
    {batchSize: 100000, parallel: true}
)

// Build small test graph
CREATE (u1:User {uid: 1, name: "A"})
CREATE (u2:User {uid: 2, name: "B"})
CREATE (u3:User {uid: 3, name: "C"})
CREATE (u4:User {uid: 4, name: "D"})
CREATE (u5:User {uid: 5, name: "E"})
CREATE (u6:User {uid: 6, name: "F"})
CREATE (u7:User {uid: 7, name: "G"})
CREATE (u8:User {uid: 8, name: "H"})
CREATE (u9:User {uid: 9, name: "I"})
CREATE (u10:User {uid: 10, name: "J"})
CREATE (u11:User {uid: 11, name: "K"})
CREATE (u12:User {uid: 12, name: "L"})
CREATE (u13:User {uid: 13, name: "M"})
CREATE (u14:User {uid: 14, name: "N"})
CREATE (u15:User {uid: 15, name: "O"})
CREATE (u16:User {uid: 16, name: "P"})
CREATE (u17:User {uid: 17, name: "Q"})
CREATE (u18:User {uid: 18, name: "R"})
CREATE (u19:User {uid: 19, name: "S"})
CREATE (u20:User {uid: 20, name: "T"})

MERGE (u1)-[:INFLUENCES {wc: 1.0}]->(u2)
MERGE (u1)-[:INFLUENCES {wc: 1.0}]->(u3)
MERGE (u2)-[:INFLUENCES {wc: 0.2}]->(u4)
MERGE (u3)-[:INFLUENCES {wc: 0.2}]->(u4)
MERGE (u3)-[:INFLUENCES {wc: 0.3}]->(u5)
MERGE (u4)-[:INFLUENCES {wc: 0.3}]->(u5)
MERGE (u4)-[:INFLUENCES {wc: 0.3}]->(u7)
MERGE (u4)-[:INFLUENCES {wc: 0.25}]->(u9)
MERGE (u5)-[:INFLUENCES {wc: 1.0}]->(u6)
MERGE (u5)-[:INFLUENCES {wc: 0.2}]->(u4)
MERGE (u5)-[:INFLUENCES {wc: 0.25}]->(u8)
MERGE (u7)-[:INFLUENCES {wc: 0.2}]->(u4)
MERGE (u7)-[:INFLUENCES {wc: 0.25}]->(u8)
MERGE (u7)-[:INFLUENCES {wc: 0.25}]->(u12)
MERGE (u9)-[:INFLUENCES {wc: 1.0}]->(u11)
MERGE (u9)-[:INFLUENCES {wc: 0.25}]->(u12)
MERGE (u9)-[:INFLUENCES {wc: 0.2}]->(u4)
MERGE (u8)-[:INFLUENCES {wc: 0.3}]->(u5)
MERGE (u8)-[:INFLUENCES {wc: 0.3}]->(u7)
MERGE (u8)-[:INFLUENCES {wc: 0.5}]->(u18)
MERGE (u8)-[:INFLUENCES {wc: 0.5}]->(u15)
MERGE (u12)-[:INFLUENCES {wc: 0.25}]->(u9)
MERGE (u12)-[:INFLUENCES {wc: 0.3}]->(u7)
MERGE (u12)-[:INFLUENCES {wc: 1.0}]->(u13)
MERGE (u12)-[:INFLUENCES {wc: 1.0}]->(u14)
MERGE (u18)-[:INFLUENCES {wc: 1.0}]->(u19)
MERGE (u18)-[:INFLUENCES {wc: 0.5}]->(u16)
MERGE (u18)-[:INFLUENCES {wc: 0.25}]->(u8)
MERGE (u15)-[:INFLUENCES {wc: 0.25}]->(u8)
MERGE (u15)-[:INFLUENCES {wc: 0.5}]->(u16)
MERGE (u11)-[:INFLUENCES {wc: 0.25}]->(u9)
MERGE (u10)-[:INFLUENCES {wc: 0.25}]->(u9)
MERGE (u13)-[:INFLUENCES {wc:0.25}]->(u12)
MERGE (u14)-[:INFLUENCES {wc:0.25}]->(u12)
MERGE (u16)-[:INFLUENCES {wc:1.0}]->(u20)
MERGE (u16)-[:INFLUENCES {wc:0.5}]->(u15)
MERGE (u16)-[:INFLUENCES {wc:1.0}]->(u17)
MERGE (u19)-[:INFLUENCES {wc:0.5}]->(u18)

// Get all paths without cycles
MATCH
    p=(:User {uid: 1})-[:INFLUENCES*1..4]->()
WITH
    p, EXTRACT(n in nodes(p) | n.name) AS node_list
WHERE
    NOT apoc.coll.containsDuplicates(node_list)
RETURN
    node_list
