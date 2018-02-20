'''
  OptSize: Finds optimal size of seed set using Monte Carlo simulations

  Can compute number of seed combinations based on size of optimal set
  and nodes not in the optimal seed set
'''

import random
import time
import operator
from decimal import Decimal
import multiprocessing as mp
from scipy.special import comb


def influenced(prob):
    return random.random() < prob


def node_spread_sim(graph, node, non_activated_nodes):
    '''
        Simulates influence spread from a node, removing newly activated nodes
        from non_activated_nodes
    '''
    q = []
    q.append(node)
    while q:
        curr = q.pop(0)
        non_activated_nodes.remove(curr)
        for neighbor in graph[curr]:
            if (neighbor in non_activated_nodes and
                    influenced(graph[curr][neighbor]) and
                    neighbor not in q):
                q.append(neighbor)


def sim_spread(graph):
    '''
    '''
    non_activated_nodes = set(graph.keys())
    seed_size = 0
    while non_activated_nodes:
        curr = random.sample(non_activated_nodes, 1)[0]
        node_spread_sim(graph, curr, non_activated_nodes)
        seed_size += 1
    return seed_size


def num_seed_sets(n, k=0, g=0):
    '''
        Prints number of possible seed sets based on number of nodes and size
        of optimal seed set S*
        n: |V|
        k: |S*|
        g: number of nodes that cannot be in S*, influence by a node with
        probability of 1
    '''
    if k <= 0:
        print("There are 2^{} number of possible seed sets.".format(n))
    else:
        if g <= 0:
            print("There are {:.2E} number of possible seed sets.".format(
                                            Decimal(comb(n, k, exact = True))))
        else:
            print("There are {:.2E} number of possible seed sets.".format(
                                    Decimal(comb(n, k, exact = True) -
                                    comb(n - g, k - g, exact = True))))

if __name__ == "__main__":
    pass
