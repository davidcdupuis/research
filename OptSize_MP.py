'''
'''

import time
import multiprocessing as mp
from OptSize import sim_spread, num_seed_sets

def find_opt_seed_size(graph, num_sim=100):
    '''
        Returns optimal seed size for graph
    '''
    t = time.time()
    seed_sizes = []
    opt_size = 0
    results = []
    with mp.Pool(mp.cpu_count()) as pool:
        # results = [pool.apply(sim_spread, args = (graph,)) for i in range(1, num_sim + 1)]
        # results = [sim_spread(graph) for i in range(1, num_sim + 1)]
        results = pool.map(sim_spread, [graph] * num_sim )
    print("It took {} seconds".format(time.time() - t))
    avg = sum(results)/len(results)
    return avg

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

    print("Searching for optimal seed set size of graph")
    opt_size = round(find_opt_seed_size(G, 10000))
    print("Optimal seed size is {}".format(opt_size))
    num_seed_sets(len(G.keys()), int(opt_size))
