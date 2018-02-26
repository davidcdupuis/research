#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' File to convert .edges files into one big json format graph
'''

import os
import pprint
import json

def fetch_files(directory):
    ''' Get all .edges files from directory
    '''
    files = []
    return files

def read_file(file, ego):
    ''' Read a file line by line
        the 'ego' follows every node in the file
        1 2 = 2 influences 1
        Add '2' to a dictionary as key if necessary and/or add '1' as tuple
        value with edge weight of 1
        network = {2:{1:0}}
        save network in a json file
    '''
    inf_network = {}
    inf_network[ego] = {}
    pp = pprint.PrettyPrinter(indent=4)
    with open(file, 'r') as f:
        for line in f:
            user = line.strip("\n").split(" ") # user[0] follows user[1], user[1] influences user[0]
            if user[1] not in inf_network:
                inf_network[user[1]] = {}
            if user[0] not in inf_network:
                inf_network[user[0]] = {}
            inf_network[user[1]][user[0]] = 1 # user[1] influences user[0]
            inf_network[user[1]][ego]     = 1 # user[1] influences ego
            inf_network[user[0]][ego]     = 1 # user[0] influences ego

    with open('inf_network.json', 'w') as outfile:
        json.dump(inf_network, outfile, sort_keys = True, indent = 4, ensure_ascii = False)


if __name__ == "__main__":
    '''
        Create a base dictionary (json)
        For every .edges file:
        > read each line and create new node if necessary
        > append to this node his follower with an initial edge weight of 1

        For every node in the graph:
        > Count the number of in-neighbors and update incoming edge weights
    '''
    read_file('12831.edges','12831')
