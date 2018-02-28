#!/usr/bin/python3
'''
    Based on model and dataset generate file(s) to use as online users for live
    process
'''

import argparse
import random
import research_data
import csv

models = ['random_basic', 'random_decay', 'random_long']

def basic_generator(dataset, nodes, num=1):
    '''
        - As many choices as there are users
        - Repetition is possible
    '''
    for i in range(num):
        file_name = 'data/{0}/random_model/{0}_s{1}.csv'.format(dataset, i)
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            for _ in range(len(nodes)):
                user = random.sample(nodes, 1)[0]
                writer.writerow([user])
        print("> Saved random_basic data to {}".format(file_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Models generator")
    parser.add_argument('-m', '--model', default="random_basic",
                        help='What model to use')
    parser.add_argument('-d', '--dataset', required=True,
                        help='What data to generate model for.')
    parser.add_argument('-n', '--number', type=int,
                        help='How many random datasets you want')
    args = parser.parse_args()

    print("Model [{}]".format(args.model))
    print("Dataset [{}]".format(args.dataset))

    graph, _ = research_data.import_graph_data(args.dataset)
    keys = graph.keys()

    if args.model == "random_basic":
        basic_generator(args.dataset, keys, args.number)
