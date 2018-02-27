#!/usr/bin/python3
'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''

import multiprocessing as mp
from monte_carlo import random_walk, monte_carlo_inf_score_est
import time
import argparse
import research_data
import csv
import random
from rtim_queue import manage_processes

THETA_AP = 0.8
NODES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O','P','Q', 'R', 'S', 'T']

def inf_scores_graph(graph, values, num_sim=10000):
    ''' Compute the influence score of all the nodes in the graph '''
    print("> Computing influence scores of all nodes")
    t = time.time()

    for node in graph.keys():
        with mp.Pool(mp.cpu_count()) as pool:
            inf_scores = pool.starmap(random_walk, [(graph, [node])] * num_sim)
        inf_score = sum(inf_scores) / float(len(inf_scores))
        values[node]['inf'] = inf_score

    msg = ": Done computing all influences scores in {} seconds"
    print(msg.format(time.time() - t))


def target(node, values, theta_inf):
    ''' Decide whether to target a node or not '''
    if values[node]['ap'] > THETA_AP or values[node]['inf'] < theta_inf:
        return False
    return True


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


def update_ap(node, new_path_weight, values):
    '''
        Update node's activation probability
    '''
    values[node]['ap'] = 1 - (1 - values[node]['ap']) * (1 - new_path_weight)
    # msg = ">> Updated activation probability of {}({}): {}"
    # print(msg.format(node, NODES[node-1], values[node]['ap']))


def update_neighbors_ap(graph, node, values, path_nodes=[], path_weight=1,
                        depth=3):
    '''
        Updates activation probability of neighbors when considering node
        as activated
        Recursive function
    '''
    # explore each neighbor
    path_nodes.append(node)
    # print("> At node {}, path_nodes {}".format(NODES[node-1], path_nodes))
    for neighbor in graph[node].keys():
        # check if the neighbor has not already been visited on this path
        # to avoid cycles
        if neighbor not in path_nodes:
            # update the ap of the neighbor with edge weight
            new_path_weight = path_weight * graph[node][neighbor]
            update_ap(neighbor, new_path_weight, values)
            # if depth is not maxed out keep exploring
            if depth > 1:
                update_neighbors_ap(graph, neighbor, values, path_nodes,
                                    new_path_weight, depth - 1)
    path_nodes.remove(node)


def save_inf_scores(graph_values, fname, model):
    print("> Saving influence scores to results.csv")
    file_name = "data/{0}/{0}_{1}_inf_scores.csv".format(fname, model.lower())
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        for key in graph_values.keys():
            line = [key, graph_values[key]['inf']]
            writer.writerow(line)
    print(": Successfully saved influence scores")

def save_seed(seeds, inf_spread, dataset, model, series='1'):
    '''
        Save seed set to csv file,
        Save influence spread as well
    '''
    file_name = "data/{0}/seeds/{0}_{1}_s{2}.csv"
    file_name = file_name.format(dataset, model.lower(), series)
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(["influence_spread:", inf_spread])
        for seed in seeds:
            writer.writerow([seed])
    print("> Seed set saved.")

def run_pre_processing(graph, graph_values, inf=True):
    '''
        Runs pre-processing part of RTIM
        returns graph_values with [inf, ap], as well as influence_threshold
        Compute and save influence scores if inf = True
    '''
    print("> RTIM is Pre-Processing!")
    if inf:
        inf_scores_graph(graph, graph_values)
        save_inf_scores(graph_values)

    research_data.import_inf_scores_csv('results.csv', graph_values)
    inf_scores = inf_score_array(graph_values)
    theta_inf_index = int(inf_threshold_index(inf_scores))
    theta_inf = inf_scores[theta_inf_index]
    print("> Influence threshold computed!")


def run_live(graph, graph_values, theta_inf, theta_inf_index, inf_scores,
            dataset):
    '''
        Runs live part of RTIM
    '''
    keys = graph.keys()
    seed = set()
    print("> RTIM is Live!")
    model = 'data/{0}/random_model/{0}_r0.csv'.format(dataset)
    with open(model, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            online_user = int(line[0])
            if target(online_user, graph_values, theta_inf):
                # add user to seed set
                seed.add(online_user)
                # update targeted user's ap as well as neighbor of max depth 3
                graph_values[online_user]['ap'] = 1.0
                update_neighbors_ap(graph, online_user, graph_values)
                # update influence threshold
                theta_inf_index -= 1
                theta_inf = inf_scores[theta_inf_index]
    print(": RTIM Live Over!")
    return seed


def run_full(graph, preProc=True, live=True, inf_thresh=0):
    '''
        Runs full RTIM experimentation
        Returns final targeted seed set
    '''
    print("---")
    graph_values = {}

    if inf_thresh != 0:
        theta_inf = inf_thresh
    elif preProc == False:
        print('''> Influence threshold must be specified if
                pre-processing is not run!''')

    # launch rtim pre-processing
    if preProc:
        run_pre_processing(graph, graph_values)

    # launch rtim live
    if live:
        return run_live(graph, graph_values, theta_inf)
    elif preProc:
        print("Pre-processing finished running without live process")


if __name__ == "__main__":
    '''
        pass argument to test RTIM with Python dic or Neo4J database
        second argument is file or database name to define data to use
    '''
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument('-f', '--file', default="hep",
                        help="File name to choose graph from")
    parser.add_argument("--model", default="WC", help="Model to use")
    parser.add_argument("--series", default="1",
                        help="What random series to use in live process")
    # parser.add_argument("--preProc", default=True, action="store_true",
    #                     help="Whether you want to RTIM pre-process")
    # parser.add_argument("--live", default=True,
    #                     help="Whether you want to run RTIM live")
    args = parser.parse_args()

    if args.model not in research_data.valid_models():
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))

    print("-------------------------------------------------------------------")
    print("Importing [{}]".format(args.file))
    print("Model [{}]".format(args.model))
    # print("RTIM Pre-Process [{}]".format(args.preProc))
    # print("RTIM Live [{}]".format(args.live))

    print("---")
    graph = {}
    graph, _ = research_data.import_graph_data(args.file, args.model)

    graph_values = {}
    for node in graph.keys():
        graph_values[node] = {'inf': 0, 'ap': 0}

    # inf_scores_graph(graph, graph_values)
    # save_inf_scores(graph_values, args.file, args.model)
    # manage_processes(graph)

    fname = 'data/{0}/{0}_{1}_inf_scores.csv'
    fname = fname.format(args.file, args.model.lower())
    research_data.import_inf_scores_csv(fname, graph_values)
    # print(graph_values)
    inf_scores = inf_score_array(graph_values)

    theta_inf_index = int(inf_threshold_index(inf_scores))
    theta_inf = inf_scores[theta_inf_index]
    # msg = "Influence threshold index {}, value {}"
    # print(msg.format(theta_inf_index, theta_inf))

    seed = set()
    seed = run_live(graph, graph_values, theta_inf, theta_inf_index, inf_scores,
                    args.file)
    print("---")

    inf_spread = monte_carlo_inf_score_est(graph, seed)
    print("Influence spread of seed set is {}".format(inf_spread))
    save_seed(seed, inf_spread, args.file, args.model, args.series)
