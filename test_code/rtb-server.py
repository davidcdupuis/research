''' RTB Simulator

    * Connects to a Neo4J database
    * When launched:
        - Follows one of two models (random or ordered) to select a user from the database
        - Send a "bid request" to the IM server and awaits a response.
        - If no response is made within a parametized time limit the server selects a new user,
        otherwise if the server receives a "bid response" it activates that user and simulates
        information propagation in the database. Selection is not influenced by this simulation.
        - The server keeps track of how many users have been activated and record the associated time.
        - Based on a parameter the simulator stops either when the rtb server simulated that all the users
        have been influenced or when the IM server makes that decision.
'''

import random

def influence(probability):
    return random.random() < probability

class RTBServer():
    def __init__(self):
        self.activated = set()
        self.graph = {'A':{},
                'B':{'A':1},
                'C':{'A':1},
                'D':{'B':0.2, 'C':0.2, 'E':0.2, 'I':0.2, 'G':0.2},
                'E':{'C':0.3, 'D':0.3, 'H':0.3},
                'F':{'E':1},
                'G':{'D':0.3, 'H':0.3, 'L':0.3},
                'H':{'G':0.25, 'E':0.25, 'R':0.25, 'O':0.25},
                'I':{'J':0.25, 'K':0.25, 'D':0.25, 'L':0.25},
                'J':{},
                'K':{'I':1},
                'L':{'I':0.25, 'G':0.25, 'M':0.25, 'N':0.25},
                'M':{'L':1},
                'N':{'L':1},
                'O':{'N':0.3, 'H':0.3, 'P':0.3},
                'P':{'O':0.5, 'R':0.5},
                'Q':{'P':1},
                'R':{'H':0.5, 'S':0.5},
                'S':{'R':1},
                'T':{'R':0.5, 'P':0.5},
                }
        self.number_nodes = len(self.graph.keys())

    def run(self):
        while len(self.activated) < self.number_nodes:
            choice = self.randomChoiceRepetition()
            print('Chose {0}'.format(choice))
            if influence(0.5):
                self.target(choice)
                print(self.activated)

    def randomChoiceRepetition(self):
        return random.choice(self.graph.keys())

    ''' For any activated node, activate neighbor node with influence probability
        Repeat recursively until no nodes have been activated
    '''
    def target(self, node):
        # for every neighbor of node not already activated try and activate
        if node not in self.activated:
            self.activated.add(node)
            for neighbor in self.graph[node]:
                #print(neighbor, graph[node][neighbor])
                if neighbor not in self.activated:
                    if influence(self.graph[node][neighbor]):
                        self.activated.add(neighbor)
                        self.target(neighbor)

if __name__ == '__main__':
    rtbserver = RTBServer()
    rtbserver.run()
