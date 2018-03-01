#!/usr/bin/python3
'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''

import multiprocessing as mp
from monte_carlo import random_walk, inf_score_est_mp
import time
import argparse
import research_data
import csv
import random
from rtim_queue import rtim_inf_scores

theta_ap = 0.8
preProc_time = -1
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


def target(node, values, theta_ap, theta_inf):
    ''' Decide whether to target a node or not '''
    if values[node]['ap'] > theta_ap or values[node]['inf'] < theta_inf:
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
    file_name = "data/rtim/results/{0}_{1}_inf_scores.csv"
    file_name = file_name.format(fname, model.lower())
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        for key in graph_values.keys():
            line = [key, graph_values[key]['inf']]
            writer.writerow(line)
    print(": Successfully saved influence scores")


def import_inf_scores(dataset, model, values):
    '''
    '''
    file_name = 'data/rtim/results/{0}_{1}_inf_scores.csv'
    file_name = file_name.format(dataset, model)
    with open(file_name, "r") as f:
        for line in f:
            vals = line.strip("\n").split(",")
            user = int(vals[0])
            inf_score = float(vals[1])
            values[user]['inf'] = inf_score
    return values


def save_seed(seeds, inf_spread, dataset, model, series='0'):
    '''
        Save seed set to csv file,
        Save influence spread as well
    '''
    file_name = "data/{0}/rtim/seeds/{0}_{1}_s{2}.csv"
    file_name = file_name.format(dataset, model.lower(), series)
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(["influence_spread:", inf_spread])
        for seed in seeds:
            writer.writerow([seed])
    print("> Seed set saved.")


def run_pre_processing(graph, dataset, model, graph_values, inf=True):
    '''
        Runs pre-processing part of RTIM
        returns graph_values with [inf, ap], as well as influence_threshold
        Compute and save influence scores if inf = True
    '''
    print("> RTIM is Pre-Processing!")
    t0 = time.time()
    rtim_inf_scores(graph, dataset, model)
    t1 = time.time()
    t = t1 - t0
    print(": Pre-Processing is over in {} seconds".format(t))
    save_pre(dataset, model, t)


def run_live(graph, dataset, model, serie, theta_ap=0.8, top=20,
             max_size=float(inf)):
    '''
        Runs live part of RTIM
    '''
    keys = graph.keys()

    graph_values = {}
    for node in keys:
        graph_values[node] = {'inf': 0, 'ap': 0}

    # computing influence threshold
    import_inf_scores(dataset, model, graph_values)
    inf_scores = inf_score_array(graph_values)
    theta_inf_index = int(inf_threshold_index(inf_scores, top))
    theta_inf = inf_scores[theta_inf_index]

    print("> RTIM is Live!")
    seed = set()
    t0 = time.time()

    file_name = 'data/{0}/random_model/{0}_s{1}.csv'.
    file_name = file_name.format(dataset, serie)
    with open(model, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            online_user = int(line[0])
            if (target(online_user, graph_values, theta_ap, theta_inf)
                and len(seed) <= max_size):
                seed.add(online_user) # add user to seed set
                # update targeted user's activation probability
                graph_values[online_user]['ap'] = 1.0
                # update act. prob. of neighbors of to depth 3
                update_neighbors_ap(graph, online_user, graph_values)
                # update influence threshold
                theta_inf_index -= 1
                theta_inf = inf_scores[theta_inf_index]

    t1 = time.time()
    t = t1 - t0
    print(": RTIM Live over. in {} seconds".format(t))

    # compute influence spread of seed set
    inf_spread = inf_score_est_mp(graph, seed)
    print("Influence spread of seed set is {}".format(inf_spread))

    save_live(dataset, model, serie, t, len(seed), inf_spread, theta_ap, top)
    return seed


def save_pre(dataset, model, run_time):
    '''
        Save pre-processing data in results
    '''
    file_name = 'data/{0}/rtim/results/{0}_{1}_pre.txt'
    file_name = file_name.format(dataset, model)
    with open(file_name, 'w') as f:
        f.write('RTIM pre-processing data\n')
        f.write('Dataset: {}\n'.format(dataset))
        f.write('Dataset model: {}\n'.format(model))
        f.write('Computation time: {} seconds\n'.format(run_time))
    print('> Saved RTIM pre-processing data!')


def save_live(dataset, model, serie, run_time, seed_size, spread, theta_ap,
              top):
    '''
        Save live data in results
    '''
    file_name = 'data/{0}/rtim/results/{0}_{1}_s{2}_live.txt'
    file_name = file_name.format(dataset, model, serie)
    with open(file_name, 'w') as f:
        f.write('RTIM live data\n')
        f.write('Dataset: {}\n'.format(dataset))
        f.write('Dataset model: {}\n'.format(model))
        temp = 'User availability dataset: {0}_s{1}.csv\n'
        f.write(temp.format(dataset, serie))
        # f.write('User availability model: {}\n'.format(av_model))
        f.write('Computation time: {} seconds\n'.format(run_time))
        f.write('Influence Threshold top tier: {}%\n'.format(top))
        f.write('Activation probability threshold: {}\n'.format(theta_ap))
        f.write('Seed size: {}\n'.format(seed_size))
        f.write('Seed spread: {}\n'.format(spread))
    print('> Saved RTIM live data!')


if __name__ == "__main__":
    '''
        pass argument to test RTIM with Python dic or Neo4J database
        second argument is file or database name to define data to use
    '''
    parser = argparse.ArgumentParser(description="RTIM")
    parser.add_argument('-f', '--file', default="hep",
                        help="File name to choose graph from")
    parser.add_argument("--model", default="WC", help="Model to use")
    parser.add_argument("--series", default="1",
                        help="What random series to use in live process")
    parser.add_argument('--ap', default=0.8, type=float,
                        help='Define theta_ap: activation prob threshold')
    parser.add_argument('--inf', default=20, type=int,
                        help='Define theta_inf: inf score top tier threshold')
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
    print("Theta_ap [{}]".format(args.ap))
    print("Theta_inf [{}]".format(args.inf))

    theta_ap = args.ap
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

    theta_inf_index = int(inf_threshold_index(inf_scores, args.inf))
    theta_inf = inf_scores[theta_inf_index]
    # msg = "Influence threshold index {}, value {}"
    # print(msg.format(theta_inf_index, theta_inf))

    seed = set()
    seed = run_live(graph, graph_values, theta_inf, theta_inf_index, inf_scores,
                    args.file)
    print("---")

    inf_spread = inf_score_est_mp(graph, seed)
    print("Influence spread of seed set is {}".format(inf_spread))
    save_seed(seed, inf_spread, args.file, args.model, args.series)

    save_data(args.file, args.model, len(seed), inf_spread, theta_ap, args.inf,
              'random_basic', 0, preProc_time)
