#!/usr/bin/python3
'''
'''

import time
import multiprocessing as mp
import argparse
from optimal_size import sim_spread, num_seed_sets
import research_data


def find_opt_seed_size(graph, num_sim):
    '''
        Returns optimal seed size for graph
    '''
    print("> Searchinf for optimal seed set size")
    t = time.time()
    results = []
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(sim_spread, [graph] * num_sim)

    print(": Optimal seed set size found in {} seconds".format(time.time() - t))
    avg = sum(results) / len(results)
    return avg


if __name__ == "__main__":
    # Manage command-line arguments
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument("-n", "--number", type=int, default=100,
                        help="Number of simulation.")
    parser.add_argument('-m', '--model', default="WC", help="Model to use")
    parser.add_argument('-f', '--file', default="hep_wc",
                        help="File name to choose graph from")
    args = parser.parse_args()

    if args.model not in research_data.valid_models():
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))

    # Here are available:
    #  - args.number: (int) The  number of simulation
    #  - args.model: (string) The model to use

    print("-------------------------------------------------------------------")
    msg = "Searching for optimal seed set size of graph [{} simulations] \n"
    msg += "Use model: {}"
    print(msg.format(args.number, args.model))
    print("---")

    graph = {}
    graph, _ = research_data.import_graph_data(args.file, args.model)

    opt_size = round(find_opt_seed_size(graph,
                                        args.number))
    print("---")
    print("Optimal seed size is {}".format(opt_size))
    num_seed_sets(len(graph.keys()), int(opt_size))
