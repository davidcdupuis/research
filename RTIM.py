'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''

import multiprocessing as mp
from MonteCarlo import random_walk
import time

THETA_AP = 0.8

def inf_scores_graph(graph, values, num_sim=10000):
    ''' Compute the influence score of all the nodes in the graph '''
    for node in graph.keys():
        with mp.Pool(mp.cpu_count()) as pool:
            inf_scores = pool.starmap(random_walk, [(graph, node)] * num_sim)
        inf_score = sum(inf_scores) / float(len(inf_scores))
        values[node]['inf'] = inf_score


def target(node):
    ''' Decide whether to target a node or not '''
    if graph[node]['ap'] > THETA_AP or graph[node]['inf'] < theta_inf:
        return False
    return True


def update_ap(graph, node):
    '''
        Updates the activation probability of neighboring nodes
    '''
    pass


def inf_score_array(values):
    '''
    '''
    # extract from values influence score array
    arr = []
    for node in values.keys():
        arr.append(values[node]['inf'])
    arr = sorted(arr)
    return arr

def inf_threshold_index(inf_score_array, top=20):
    '''
        Finds the index of the influence threshold
        values: dict containing all scores
        top: top percentage desired
    '''
    index = len(inf_score_array) - len(inf_score_array) * top / 100
    return index


if __name__ == "__main__":
    '''
        pass argument to test RTIM with Python dic or Neo4J database
        second argument is file or database name to define data to use
    '''
    G = {
            'A': {'B': 1, 'C': 1},
            'B': {'D': 0.2},
            'C': {'D': 0.2,  'E': 0.3},
            'D': {'E': 0.3, 'G': 0.3, 'I': 0.25},
            'E': {'F': 1, 'D': 0.2, 'H': 0.25},
            'F': {},
            'G': {'D': 0.2, 'H': 0.25, 'L': 0.25},
            'H': {'E': 0.3, 'G': 0.3, 'R': 0.5, 'O': 0.5},
            'I': {'K': 1, 'L': 0.25, 'D': 0.2},
            'J': {'I': 0.25},
            'K': {'I': 0.25},
            'L': {'I': 0.25, 'G': 0.3, 'M': 1, 'N': 1},
            'M': {'L': 0.25},
            'N': {'L': 0.25},
            'O': {'H': 0.25, 'P': 0.5},
            'P': {'T': 1, 'O': 0.5, 'Q': 1},
            'Q': {},
            'R': {'S': 1, 'P': 0.5, 'H': 0.25},
            'S': {'R': 0.5},
            'T': {}
        }

    print("\nPre-Processing")

    graph_values = {}
    for node in G.keys():
        graph_values[node] = {'inf': 0, 'ap': 0}

    print("Computing influence scores of all nodes")
    t = time.time()
    inf_scores_graph(G, graph_values)
    print("Done computing all influences scores in {} seconds".format(time.time() - t))

    inf_scores = inf_score_array(graph_values)
    theta_inf_index = int(inf_threshold_index(inf_scores))
    print("\nInfluence threshold index {}".format(theta_inf_index))
    theta_inf = inf_scores[theta_inf_index]
    print("\nInfluence threshold: {}".format(theta_inf))
