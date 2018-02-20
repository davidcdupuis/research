''' IM Simulator

    Runs both the RTB and IM server to evaluate IM model
'''

import thread
from threading import Thread
#from neo4j.v1 import GraphDatabase
import random
import time

def influence(probability):
    return random.random() < probability

class RTBServer(Thread):
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

class IMServer(Thread):
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

    def run(self):
        # runs model on graph while communicating with RTBServer
        pass

    def pre_process(self):
        pass

    def live_process(self):
        pass

class MyThread(Thread):
    def __init__(self, val):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val = val

    def run(self):
        for i in range(1, self.val):
            print('Value %d in thread %s' % (i, self.getName()))

            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = random.randint(1, 5)
            print('%s sleeping fo %d seconds...' % (self.getName(), secondsToSleep))
            time.sleep(secondsToSleep)

preProcessing = True

def run():
    pass

''' IM Server
    Server to decide which users to target either in pre-processing or live or both.
'''
def im_server(model):
    import model

''' RTB Server

'''
def rtb_server(db = "default", selection = "random", propagation="WC"):
    if selection == "random":
        pass
    if propagation == "WC":
        pass

if __name__=='__main__':
    '''
    rtbserver = RTBServer()
    rtbserver.setName('RTB server')

    imserver = IMServer()
    imserver.setName('IM server')

    rtbserver.start()
    imserver.start()

    rtbserver.join()
    imserver.join()
    '''
    myThreadOb1 = MyThread(4)
    myThreadOb1.setName('Thread 1')

    myThreadOb2 = MyThread(4)
    myThreadOb2.setName('Thread 2')

    # Start running the threads!
    myThreadOb1.start()
    myThreadOb2.start()

    # Wait for the threads to finish...
    myThreadOb1.join()
    myThreadOb2.join()
    print('Main terminating')
