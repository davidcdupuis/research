#!/usr/bin/python3
'''
    Computes weighted cascade edges of file
    Saves changes to new file
'''

import research_data
import argparse
import csv

def save_file(graph, file_name):
    '''
        Saves graph to file_name.inf
    '''
    print("> Saving graph to {}".format(file_name))
    num_edges = 0
    for key in graph.keys():
        for n in graph[key].keys():
            num_edges += 1

    with open('data/' + file_name, "w") as f:
        f.write(str(len(graph.keys())) + ' ' + str(num_edges) + '\n')
        for key in graph.keys():
            for neighbor in graph[key].keys():
                line = str(key) + ' '
                line += str(neighbor) + ' '
                line += str(graph[key][neighbor])
                f.write(line)
                f.write('\n')

    print(": File {} successfully saved to data/".format(file_name))


def compute_wc(graph):
    '''
        Computes weighted cascade edges of graph
    '''
    print("> Computing weighted cascade edges")
    occurences = dict.fromkeys(graph.keys(), 0)
    for key in graph.keys():
        for neighbor in graph[key].keys():
            occurences[neighbor] += 1

    for key in graph.keys():
        for neighbor in graph[key].keys():
            graph[key][neighbor] = 1 / float(occurences[neighbor])

    print(": Successfully computed weighted cascade edges of graph")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weighted cascade computer")
    parser.add_argument('-f', '--file', help='File name to compute WC on',
                        required=True)
    parser.add_argument('-s','--save', help='file name to save changes to')
    args = parser.parse_args()

    # check if file is in data else print error
    graph = {}
    graph, _ = research_data.import_graph_data(args.file)
    compute_wc(graph)

    if args.save:
        save_file(graph, args.save)
