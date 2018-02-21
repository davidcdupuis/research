'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''

import multiprocessing as mp
from MonteCarlo import random_walk
import time
import argparse
import research_data

THETA_AP = 0.8

def inf_scores_graph(graph, values, num_sim=10000):
    ''' Compute the influence score of all the nodes in the graph '''
    for node in graph.keys():
        with mp.Pool(mp.cpu_count()) as pool:
            inf_scores = pool.starmap(random_walk, [(graph, [node])] * num_sim)
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
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument('--small', default=False, action="store_true",
                        help="Whether to use the small graph or the big one.")
    parser.add_argument("--model", default="WC", help="Model to use")
    args = parser.parse_args()

    if args.model not in research_data.valid_models():
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))

    graph_size = ""
    if args.small:
        graph_size = "small"
    else:
        graph_size = "large"

    msg = "Pre-processing {} graph using RTIM\n"
    msg += "Use model: {}"
    print(msg.format(graph_size, args.model))

    graph = {}
    if args.small:
        graph = research_data.small_graph_data()
    else:
        graph = research_data.big_graph_data(args.model)

    print("Pre-Processing")

    graph_values = {}
    for node in graph.keys():
        graph_values[node] = {'inf': 0, 'ap': 0}

    print("Computing influence scores of all nodes")
    t = time.time()
    inf_scores_graph(graph, graph_values)
    msg = "Done computing all influences scores in {} seconds"
    print(msg.format(time.time() - t))

    inf_scores = inf_score_array(graph_values)

    if len(graph.keys()) < 30:
        print(graph_values)
        print("")
        print(inf_scores)

    theta_inf_index = int(inf_threshold_index(inf_scores))
    theta_inf = inf_scores[theta_inf_index]

    msg = "\nInfluence threshold index {}, value {}"
    print(msg.format(theta_inf_index, theta_inf))
