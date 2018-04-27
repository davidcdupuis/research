#!/usr/bin/python3
'''
    Function to initialize graphs
    - Convert graph from undirected to directed
    - Compute weighted cascade edge weights of graph and save
'''

import argparse
import csv

datasets = ['small_graph', 'hep', 'hept', 'phy', 'dblp', 'youtube']
algorithms = ['undirToDir', 'computeWC']

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
    graph = {}
    import_dir = "data/{0}/{0}".format(dataset)
    with open(import_dir, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        for line in reader:
            user1 = int(line[0])
            user2 = int(line[1])
            if user1 not in graph:
                graph[user1] = {}
            if user2 not in graph:
                graph[user2] = {}
            graph[user1][user2] = {}
            graph[user2][user1] = {}
            #import correctly

    export_dir = "data/{0}/{0}_wc.inf".format(dataset)
    with open(export_dir, 'w') as file:
        writer = csv.writer(file, delimiter=' ')
        # write every edge of graph to  file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graph Initlization")
    parser.add_argument('-a','--algorithm', help=algorithms)
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help=datasets)
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    if args.dataset not in datasets:
        raise Exception("Dataset does not exist!")
    if args.algorithm not in algorithms:
        raise Exception("Algorithm does not exist!")

    if args.algorithm == 'undirToDir' and args.file == None:
        raise Exception("File name not specified!")

    if args.algorithm == 'undirToDir':
        undirToDir(args.dataset, args.file)

    if args.algorithm == 'computeWC':
        computeWC(args.dataset)
