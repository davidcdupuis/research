#!/usr/bin/python3
'''
'''

import time
import multiprocessing as mp
import argparse
from optimal_size import sim_spread, num_seed_sets
import research_data
from math import ceil
import matplotlib.pyplot as plt
import pandas as pd


def find_opt_seed_size(graph, num_sim, reach):
    '''
        Returns optimal seed size for graph
    '''
    print("> Searching for optimal seed set size")

    results = []
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.starmap(sim_spread, [(graph, reach)]* num_sim)

    #best = min(results)
    #avg = sum(results) / len(results)
    #print("Optimal seed size found is: {}".format(round(avg)))
    return results #avg, best


def save_data(dataset, model, reach, opt_res, opt_size, num_sim, run_time, best):
    '''
        Saves data to appropriate text file
    '''
    file_name = 'data/{0}/opt_size/opt_size_{0}_{1}.txt'
    file_name = file_name.format(dataset, model)
    with open(file_name, 'a') as f: # w for write and a for append
        f.write('Dataset: {}\n'.format(dataset))
        f.write('Model: {}\n'.format(model))
        f.write('Reach: {}\n'.format(reach))
        f.write('Simulations: {}\n'.format(num_sim))
        f.write('Runtime: {} seconds\n'.format(run_time))
        f.write('Best size: {}\n'.format(best))
        f.write('Optimal size found: {}\n'.format(opt_res))
        f.write('Optimal seed set size: {}\n'.format(opt_size))
        f.write('-----------------------------------------------------------\n')

    print("> Data saved to {}".format(file_name))


def run(graph, dataset, model, reach, num_sim=1000):
    '''
        Run optimal_size_mp to find optimal seed size
        Save results to file in folder
    '''
    t0 = time.time()
    results = find_opt_seed_size(graph, num_sim, reach)
    avg = sum(results) / len(results)
    opt_size = ceil(avg)
    t1 = time.time()
    run_time = t1 - t0

    best = min(results)
    print("Optimal seed set size found in {} seconds".format(run_time))
    print("Optimal seed size is {}".format(opt_size))

    # plot simulation convergence of results
    df = pd.DataFrame([{'simulations':i+1,'size':sum(results[:i+1])/len(results[:i+1])} for i in range(len(results))])

    plt.plot(df['simulations'],df['size'],color='blue',label='opt_size')
    plt.xlabel('simulations')
    plt.ylabel('size')
    plt.legend()
    plt.title('Evolution of opt_size vs simulations for {}'.format(dataset))
    file_name = 'data/{0}/opt_size/opt_size_{0}_{1}_{2}.png'
    file_name = file_name.format(dataset, model, reach)
    plt.savefig(file_name)
    plt.close()
    print("Saved figure to png")
    save_data(dataset, model, reach, avg, opt_size, num_sim, run_time, best)


def plotResults(results):
    '''
        Plot results to view convergence
    '''


if __name__ == "__main__":
    # Manage command-line arguments
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument("-n", "--number", type=int, default=100,
                        help="Number of simulations.")
    parser.add_argument('-m', '--model', default="WC", help="Model to use")
    parser.add_argument('-d', '--dataset', default="hep",
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
    graph, _ = research_data.import_graph_data(args.dataset, args.model)

    # opt_size = round(find_opt_seed_size(graph, args.number))
    # print("---")
    # print("Optimal seed size is {}".format(opt_size))
    # num_seed_sets(len(graph.keys()), int(opt_size))
    run(graph, args.dataset, args.model, args.number)
