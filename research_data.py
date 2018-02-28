#!/usr/bin/python3

import argparse

datasets = ['small_graph', 'hep', 'hept', 'phy']
models = ['wc', '0.1', '0.01', '0.3', '0.5', '0.8', '0.9']

def valid_models():
    return ["wc", "0.1","0.01","0.5","0.9"]


def import_graph_data(dataset, model="wc"):
    ''' Hep_WC contains:
        15,233 nodes
        62,796 edges
    '''
    print("> Importing data from {}".format(dataset))
    file_name = 'data/{0}/{0}_wc.inf'.format(dataset)
    inf_network = {}
    conditions = []
    condict = {}
    with open(file_name, 'r') as f:
        next(f)
        for line in f:
            # user1 user2 influence => (user1 -- influence --> user2)
            data = line.strip("\n").split(" ")
            user1 = int(data[0])
            user2 = int(data[1])
            inf_score = float(data[2])
            if user1 not in inf_network:
                inf_network[user1] = {}
            if user2 not in inf_network:
                inf_network[user2] = {}

            if type(model) == float:
                inf_network[user1][user2] = model
            elif model == "wc":
                inf_network[user1][user2] = inf_score
            else:
                raise Exception("Unknown model: {}".format(model))

            if inf_score == 1.0:
                if user1 not in condict:
                    condict[user1] = 0
                condict[user1] += 1
                conditions.append((user1, user2))

    print(": Done importing {}".format(file_name))
    num = {}
    for key in condict:
        if condict[key] not in num:
            num[condict[key]] = 0
        num[condict[key]] += 1

    # print(num)
    return (inf_network, conditions)


def import_inf_scores_csv(file_name, values):
    '''
    '''
    with open(file_name, "r") as f:
        for line in f:
            vals = line.strip("\n").split(",")
            user = int(vals[0])
            inf_score = float(vals[1])
            values[user]['inf'] = inf_score
    return values


if __name__ == "__main__":
    parser = parser = argparse.ArgumentParser(description="Main")
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help='{}'.format(datasets))
    parser.add_argument('-m', '--model', default='wc',
                        help='{}'.format(models))
    args = parser.parse_args()

    if args.dataset not in datasets:
        msg = "Invalid arguments [dataset] -> Received: {}"
        raise Exception(msg.format(args.dataset))
    if args.model not in models:
        msg = "Invalid arguments [model] -> Received: {}"
    else:
        if args.model != 'wc':
            args.model = float(args.model)

    print("-------- Parameters --------")
    print("Dataset \t [{}]".format(args.dataset))
    print("Model \t\t [{}], type [{}]".format(args.model, type(args.model)))
    print("----------------------------")

    graph, _ = import_graph_data(args.dataset, args.model)
    if args.dataset == 'small_graph':
        print(graph)
    # import_inf_scores_csv('results.csv')
