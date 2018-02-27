#!/usr/bin/python3
'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''

import multiprocessing as mp
from monte_carlo import random_walk
import time
import argparse
import research_data
import csv
import random

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


def save_inf_scores(graph_values, file_name="results.csv"):
    print("> Saving influence scores to results.csv")
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        for key in graph_values.keys():
            line = [key, graph_values[key]['inf']]
            writer.writerow(line)
    print(": Successfully saved influence scores")

def run_pre_processing(graph):
    '''
        Runs pre-processing part of RTIM
        returns graph_values with [inf, ap], as well as influence_threshold
    '''
    pass

def run_live(graph):
    '''
        Runs live part of RTIM
    '''
    pass

def run_full(graph, preProc=True, live=True, inf_thresh=0):
    '''
        Runs full RTIM experimentation
        Returns final targeted seed set
    '''
    print("---")
    keys = graph.keys()
    graph_values = {}
    seed = set()
    if inf_thresh != 0:
        theta_inf = inf_thresh
    elif preProc == False:
        print('''> Influence threshold must be specified if
                pre-processing is not run!''')

    # launch rtim pre-processing
    if preProc:
        print("> RTIM is Pre-Processing!")
        # compute influence scores
        for node in graph.keys():
            graph_values[node] = {'inf': 0, 'ap': 0}
    else:
        # import influence scores from csv file
        research_data.import_inf_scores_csv('results.csv', graph_values)

    # launch rtim live
    if live:
        print("> RTIM is Live!")
        lim = len(keys) # select as many users as there are in graph
        for i in range(lim):
            online_user = random.sample(keys, 1)[0]
            if target(online_user, graph_values, theta_inf):
                seed.append(online_user)
                graph_values[online_user]['ap'] = 1.0
                update_ap(graph, online_user, graph_values)

    return seed


if __name__ == "__main__":
    '''
        pass argument to test RTIM with Python dic or Neo4J database
        second argument is file or database name to define data to use
    '''
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument('-f', '--file', default="hep_wc",
                        help="File name to choose graph from", required=True)
    parser.add_argument("--model", default="WC", help="Model to use")
    args = parser.parse_args()

    if args.model not in research_data.valid_models():
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))

    print("-------------------------------------------------------------------")
    print("Importing [{}]".format(args.file))
    print("Model [{}]".format(args.model))

    print("---")
    graph = {}
    graph, _ = research_data.import_graph_data(args.file, args.model)

    graph_values = {}
    for node in graph.keys():
        graph_values[node] = {'inf': 0, 'ap': 0}

    # inf_scores_graph(graph, graph_values)
    # save_inf_scores(graph_values)

    research_data.import_inf_scores_csv('results.csv', graph_values)
    # print(graph_values)
    inf_scores = inf_score_array(graph_values)

    # if len(graph.keys()) < 30:
    #     print(graph_values)
    #     print("")
    #     print(inf_scores)

    # theta_inf_index = int(inf_threshold_index(inf_scores))
    # theta_inf = inf_scores[theta_inf_index]
    # msg = "Influence threshold index {}, value {}"
    # print(msg.format(theta_inf_index, theta_inf))

    print("-")
    graph_values[1]['ap'] = 1.0
    update_neighbors_ap(graph, 1, graph_values)
    print("Finished updating activation probabilities")
    print("-")
    print(graph_values)

    print("---")
