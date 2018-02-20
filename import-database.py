# create Neo4J database from Twitter follower files
#from neo4j.v1 import GraphDatabase
import sys
import os

def importFolder(path):
    pass

def importFile(path):
    users_graph = {}
    with open(path) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    for line in lines:
        users = line.split(" ")
        users_graph[users[0]] = users[1::]
    print(users_graph)


if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        importFolder(sys.argv[1])
    elif os.path.isfile(sys.argv[1]):
        importFile(sys.argv[1])
    else:
        print("Wrong file or folder name")
