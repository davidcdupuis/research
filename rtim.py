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

THETA_AP = 0.8

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


def update_ap(graph, node):
    '''
        Updates activation probability of neighbors when considering node
        as activated
    '''
    pass


def save_inf_scores(graph_values, file_name="results.csv"):
    print("> Saving influence scores to results.csv")
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        for key in graph_values.keys():
            line = [key, graph_values[key]['inf']]
            writer.writerow(line)
    print(": Successfully saved influence scores")


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

    msg = "Pre-processing graph using RTIM\n"
    msg += "Use model: {}".format(args.model)
    print(msg)

    print("---")
    graph = {}
    graph, _ = research_data.import_graph_data(args.file, args.model)

    graph_values = {}
    for node in graph.keys():
        graph_values[node] = {'inf': 0, 'ap': 0}

    # inf_scores_graph(graph, graph_values)
    # save_inf_scores(graph_values)

    research_data.import_inf_scores_csv('results.csv', graph_values)
    print(graph_values)
    inf_scores = inf_score_array(graph_values)

    # if len(graph.keys()) < 30:
    #     print(graph_values)
    #     print("")
    #     print(inf_scores)

    theta_inf_index = int(inf_threshold_index(inf_scores))
    theta_inf = inf_scores[theta_inf_index]

    print("---")
    msg = "Influence threshold index {}, value {}"
    print(msg.format(theta_inf_index, theta_inf))
