#!/usr/bin/python3
'''
    Function to initialize graphs
    - Convert graph from undirected to directed
    - Compute weighted cascade edge weights of graph and save
'''

import argparse
import csv

datasets = ['small_graph', 'hep', 'hept', 'phy', 'dblp', 'youtube', 'orkut',
            'friendster', 'livejournal', 'twitter']
algorithms = ['undirToDir', 'computeWC', 'processTwitterDataset']


def undirToDir(dataset, import_file):
    '''
        Converts an undirected graph to a directed graph
        For each line in file, reverse edges:
        start - end:
            * start -> end
            * end -> start
    '''
    import_dir =  "data/{}/{}".format(dataset, import_file)
    export_dir = "data/{0}/{0}.inf".format(dataset)
    count = 0
    with open(import_dir, 'r') as read_file:
        with open(export_dir, 'w', newline='') as write_file:
            reader = csv.reader(read_file, delimiter='\t')
            writer = csv.writer(write_file, delimiter=' ')
            for line in reader:
                count += 1
                start = line[0]
                end = line[1]
                writer.writerow([start, end])
                writer.writerow([end, start])
                if ((count < 1000000 and count % 100000 == 0)
                    or (count < 10000000 and count % 2000000 == 0)
                    or (count < 100000000 and count % 20000000 == 0)
                    or (count >= 100000000 and count % 100000000 == 0)):
                    print("Processed {} edges!".format(count))
    msg = "Directed graph: {} file saved with {} edges!"
    print(msg.format(export_dir, count))


def computeWC(dataset):
    '''
        Computes edge weights for weighted cascade
        - Import graph without weights
        - Compute weights for all edges
        - Save graph under dataset_wc.inf
    '''
    # Build inverse influence graph
    inv_graph = {}
    import_dir = "data/{0}/{0}.inf".format(dataset)
    print("Importing {}".format(import_dir))
    with open(import_dir, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        for line in reader:
            user1 = int(line[0])
            user2 = int(line[1])
            if user1 not in inv_graph:
                inv_graph[user1] = {}
            if user2 not in inv_graph:
                inv_graph[user2] = {}
            inv_graph[user2][user1] = 0
    print("Graph {} imported correctly".format(dataset))

    print("Computing and saving edge weights")
    export_dir = "data/{0}/{0}_wc.inf".format(dataset)
    count = 0
    with open(export_dir, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        for user in inv_graph.keys():
            num = len(inv_graph[user].keys())
            for influencer in inv_graph[user].keys():
                count += 1
                inv_graph[user][influencer] = 1.0/num
                writer.writerow([influencer, user, inv_graph[user][influencer]])
                if ((count < 1000000 and count % 100000 == 0)
                    or (count < 10000000 and count % 2000000 == 0)
                    or (count < 100000000 and count % 20000000 == 0)
                    or (count >= 100000000 and count % 100000000 == 0)):
                    print("Processed {} edges!".format(count))
    print("Weights computed successfully and saved to {}".format(export_dir))


def processTwitterDataset(dataset, import_file):
    '''
        Function to process directed twitter file with tab separator
    '''
    # Build inverse influence graph
    inv_graph = {}
    import_dir = "data/{}/{}".format(dataset, import_file)
    print("Importing {}".format(import_dir))
    with open(import_dir, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for line in reader:
            user1 = int(line[0])
            user2 = int(line[1])
            if user1 not in inv_graph:
                inv_graph[user1] = {}
            if user2 not in inv_graph:
                inv_graph[user2] = {}
            inv_graph[user2][user1] = 0
    print("Graph {} imported correctly".format(dataset))

    print("Computing and saving edge weights")
    export_dir = "data/{0}/{0}_wc.inf".format(dataset)
    count = 0
    with open(export_dir, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        for user in inv_graph.keys():
            num = len(inv_graph[user].keys())
            for influencer in inv_graph[user].keys():
                count += 1
                inv_graph[user][influencer] = 1.0/num
                writer.writerow([influencer, user, inv_graph[user][influencer]])
                if ((count < 1000000 and count % 100000 == 0)
                    or (count < 10000000 and count % 2000000 == 0)
                    or (count < 100000000 and count % 20000000 == 0)
                    or (count >= 100000000 and count % 100000000 == 0)):
                    print("Processed {} edges!".format(count))
    print("Weights computed successfully and saved to {}".format(export_dir))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graph Initialization")
    parser.add_argument('-a','--algorithm', help='{}'.format(algorithms))
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help='{}'.format(datasets))
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    if args.dataset not in datasets:
        raise Exception("Dataset does not exist!")
    if args.algorithm not in algorithms:
        raise Exception("Algorithm does not exist!")

    if args.algorithm == 'undirToDir' and args.file == None:
        raise Exception("File name not specified!")

    if args.algorithm == 'processTwitterDataset' and args.file == None:
        raise Exception("File name not specified!")

    if args.algorithm == 'undirToDir':
        undirToDir(args.dataset, args.file)

    if args.algorithm == 'computeWC':
        computeWC(args.dataset)

    if args.algorithm == 'processTwitterDataset' and args.file != None:
        processTwitterDataset(args.dataset, args.file)
