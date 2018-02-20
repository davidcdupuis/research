'''
  Monte Carlo Simulation

  Simulate influence spread through random walks
'''

import random
import time


def influenced(prob):
    return random.random() < prob


def monte_carlo_inf_score_est(graph, seed, num_sim=10000, timed=False):
    '''
        Performs num_sim influence simulations from seed on graph
        Returns Monte Carlo influence score of seed in graph
    '''
    t0 = time.time()
    inf_score = 0
    for i in range(1,  num_sim + 1):
        activated = random_walk(graph,  seed)
        # update inf_score as streaming average during simulation
        inf_score = inf_score + (activated - inf_score)/float(i)
    if timed:
        print("> Monte Carlo method finished computing in {} seconds".format(
                                                round(time.time() - t0,  2)))
    return inf_score


def random_walk(graph,  seed):
    '''
        Performs a random walk from seed nodes on graph
        Returns number of activated nodes + size of seed set.
    '''
    # in random walk we don't attempt activating twice an activated node
    activated = 0
    activated_nodes = set()
    [activated_nodes.add(e) for e in seed]
    for node in seed:
        q = [node]
        while q:
            curr = q.pop(0)
            activated += 1
            for neighbor in graph[curr]:
                if (neighbor not in activated_nodes and
                        influenced(graph[curr][neighbor])):
                    activated_nodes.add(neighbor)
                    q.append(neighbor)
    return activated


if __name__ == "__main__":
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

    S = ['A', 'E', 'D', 'G', 'I', 'H', 'J', 'L', 'O', 'P', 'R']
    print("\nTesting Monte Carlo on seed set {}".format(S))
    S_score = monte_carlo_inf_score_est(G,  S,  timed=True)
    print("Influence score of seed set is {}".format(S_score))
