#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Python script to compute optimal influence maximization result using brut force

    1. We find all subsets of the graph.
    2. We compute the influence spread of each seed seed_set
        2.1. For each node not in the seed set we compute it's activation probability
             based on all seed nodes by finding all the paths between these nodes.
        2.2. Using all these paths we compute iep for each node not in the seed set.
'''
from itertools import combinations
from itertools import tee
from operator import mul
import random
import time

graph = {'A':{'B':1,'C':1},
        'B':{'D':0.2},
        'C':{'D':0.2, 'E':0.3},
        'D':{'E':0.3,'G':0.3,'I':0.25},
        'E':{'F':1,'D':0.2,'H':0.25},
        'F':{},
        'G':{'D':0.2,'H':0.25,'L':0.25},
        'H':{'E':0.3,'G':0.3,'R':0.5,'O':0.5},
        'I':{'K':1,'L':0.25,'D':0.2},
        'J':{'I':0.25},
        'K':{'I':0.25},
        'L':{'I':0.25,'G':0.3,'M':1,'N':1},
        'M':{'L':0.25},
        'N':{'L':0.25},
        'O':{'H':0.25,'P':0.5},
        'P':{'T':1,'O':0.5,'Q':1},
        'Q':{},
        'R':{'S':1,'P':0.5,'H':0.25},
        'S':{'R':0.5},
        'T':{},
        }

influence_graph = dict.fromkeys(graph.keys(), 0)

''' Function to compute the exact influence score of a node independently.
'''
def influence_score(node):
    # sum the activation probability of every neighbor to compute score
    score = 0
    for key in graph.keys():
        if key != node:
            #print("Searching for all paths between {0} and {1}".format(node, key))
            paths = find_all_paths(graph, node, key)
            #print("{0} paths found between {1} and {2}".format(len(paths), node, key))
            #print("Computing activation probability of {0}".format(key))
            ap = iep(paths)
            #print("Activation probability of {0} from {1} is {2}".format(key, node, ap))
            score += ap
            #print("-------------------------------------------------------------------")
    return score

''' Function to find all paths between two nodes
'''
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

''' Finds all paths between two nodes where only the start node can be activated
'''
def find_all_paths_non_activated(graph, activated, curr, end, path=[]):
    path = path + [curr]
    if curr == end:
        return [path]
    if not graph.has_key(curr):
        return []
    paths = []
    for neighbor in graph[curr]:
        if neighbor not in path  and neighbor not in activated:
            newpaths = find_all_paths_non_activated(graph, activated, neighbor, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def create_seeds(graph, size = 0):
    l = len(graph.keys())
    seed_sets = []
    if size == 0:
        min_lim, max_lim = 0, l
    else:
        min_lim, max_lim = size, size + 1
    for i in range(min_lim, max_lim):
        combos = combinations(graph.keys(), i)
        for combo in combos:
            if ((not(('A' in combo and 'B' in combo) or
                   ('A' in combo and 'C' in combo) or
                   ('K' in combo and 'I' in combo) or
                   ('M' in combo and 'L' in combo) or
                   ('P' in combo and 'Q' in combo) or
                   ('P' in combo and 'T' in combo) or
                   ('R' in combo and 'S' in combo) or
                   ('L' in combo and 'N' in combo) or
                   ('E' in combo and 'F' in combo))) and
                   ('A' in combo and 'J' in combo)):
                   yield combo

def old_seed_influence_spread(seed):
    # for every node in seed compute it's influence score
    # sum the activation score
    total = 0
    for node in seed:
        score = 0
        for key in graph.keys():
            if key != node:
                paths = find_all_paths_non_activated(graph, seed, node, key)
                score += iep(paths) # the influence score of a node is the sum of activation probabilities of his non activated neighbors
        #print('Influence score of {0} is {1}'.format(node, score))
        total += score
    total += len(seed)
    return total

''' Function to compute the influence spread of a particular seed set S
    This is done by computing a^S(x_i) where x_i is any node not in S.
    We find all paths between every node in S which do not contain more than 1 node in S
    and apply the IEP on these paths
'''
def seed_influence_spread(seed):
    total = 0
    to_visit = [x for x in graph.keys() if x not in seed]
    for key in to_visit:
        paths = []
        for node in seed:
            paths += find_all_paths_non_activated(graph, seed, node, key)
        if len(paths) >= 15:
            print("> Computing IEP on 2^{0}".format(len(paths)))
        key_score = iep(paths)
        total += key_score
    total += len(seed)
    return total

def optimal_seed_influence_spread(seed):
    total = 0
    to_visit = [x for x in graph.keys() if x not in seed]
    for key in to_visit:
        paths = []
        for node in seed:
            paths += find_all_paths_non_activated(graph, seed, node, key)
        all_path_groups = find_dependency_groups(paths)
        score = 1
        for group in all_path_groups:
            if len(group) > 1:
                # print("Group length: {0}".format(len(group)))
                if len(group) >= 16:
                    print("> Computing IEP on 2^{0}".format(len(group)))
                    avg = 0
                    for path in group:
                        avg += len(path)
                    avg = float(avg) / len(group)
                    print("> Avg path lengths are: {0}".format(avg))
                group_score = iep(group)
            else:
                # print("Group length 1: {0}".format(group))
                group_score = edges_weight(group)
            score *= (1 - group_score)
        key_score = 1 - score
        total += key_score
    total += len(seed)
    return total

def hybrid_seed_influence_spread(seed):
    '''
        Influence spread function using exact method if number of paths <= 18
        else it uses Monte Carlo simulation
    '''
    total = 0
    to_visit = [x for x in graph.keys() if x not in seed]
    try_MC = False
    for key in to_visit:
        paths = []
        for node in seed:
            paths += find_all_paths_non_activated(graph, seed, node, key)
        if len(paths) >= 18:
            print("> 2^{0} combos, stopping, attempting seed_MC".format(len(paths)))
            try_MC = True
            break
        key_score = iep(paths)
        total += key_score
    if try_MC:
        total = seed_MC(seed)
    else:
        total += len(seed)
    return total

def find_best_seed_set(seeds, opt = "exact"):
    ''' Brut force function to find optimal seed set
    '''
    best_score = 0
    count = 0
    for seed in seeds:
        if opt == "exact":
            seed_score = seed_influence_spread(seed)
        elif opt == "opt":
            seed_score = optimal_seed_influence_spread(seed)
        elif opt == "mc":
            seed_score = seed_MC(seed)
        elif opt == "hybrid":
            seed_score = hybrid_seed_influence_spread(seed)
        count += 1
        if best_score < seed_score:
            best_score = seed_score
            best_seed = seed
            print("> Current best seed set: ({0}, {1})".format(best_seed, best_score))
            print("> Tested seeds: {0} ".format(count))
        if count % 1000 == 0:
            print("> Tested seeds: {0} ".format(count))
        if best_score >= 20.0:
            return (best_seed, best_score)
    return (best_seed, best_score)

''' Function to find the edges that make up the intersection of different paths
'''
def path_intersect(paths):
    # for each path extract edges
    intersect = set()
    for path in paths:
        edges = path_edges(path)
        for edge in edges:
            intersect.add(edge)
    return intersect

''' Function to find all the edges in a path
'''
def path_edges(path):
    path_edges = []
    for i in range(0,len(path)-1):
        path_edges.append((path[i], path[i+1]))
    return path_edges

''' Function that computes the product of the edges in a list
'''
def edges_weight(edges):
    product = 1
    for edge in edges:
        product *= graph[edge[0]][edge[1]]
    return product

''' Computes:
    sum_intersect([p1, p2, p3], 2) = (p1 ∩ p2) + (p1 ∩ p3) + (p2 ∩ p3)
'''
def sum_intersect(paths, s):
    # for every combination of paths we compute their path_intersect
    combos = combinations(paths, s)
    total = 0
    for combo in combos:
        intersect = path_intersect(combo)
        total += edges_weight(intersect) # we convert that path intersect to a probability and sum them all
    return total

''' Function to compute IEP on a list of probabilities
'''
def iep(paths):
    result = 0
    for k in range(1,len(paths)+1):
        result = result + (-1)**(k+1)*sum_intersect(paths, k)
    return result

def filter_seeds(seeds):
    filtered_seeds = list(seeds)
    #print(filtered_seeds)
    #print(seeds)
    for seed in seeds:
        #print("> Checking {0}".format(seed))
        # 'B' and 'C' in seed != 'B' in seed and 'C' in seed
        if ('A' in seed and 'B' in seed) or ('A' in seed and 'C' in seed) or ('K' in seed and 'I' in seed) or ('M' in seed and 'L' in seed) or ('P' in seed and 'Q' in seed) or ('P' in seed and 'T' in seed) or ('R' in seed and 'S' in seed) or ('L' in seed and 'N' in seed) or ('E' in seed and 'F' in seed):
            #print(">> Removing: {0}".format(seed))
            filtered_seeds.remove(seed)
    return filtered_seeds

def propagate(node, non_activated_nodes):
    #print("> propagate")
    q = []
    q.append(node)
    while q:
        #print("Queue: {0}".format(q))
        curr = q.pop(0)
        # print("non_activated_nodes: {0}".format(non_activated_nodes))
        #print("curr: {0}".format(curr))
        non_activated_nodes.remove(curr)
        for neighbor in graph[curr]:
            if neighbor in non_activated_nodes: # check that neighbor can be activated
                if influenced(graph[curr][neighbor]): # try and influence neighbor with edge probability
                    #print("add to queue: {0}".format(neighbor))
                    if neighbor not in q:
                        q.append(neighbor)
    return 1

def influenced(prob):
    return random.random() < prob

def find_dependency_groups(paths):
    # instead of storing unshable type list we will store a path_id
    path_ids = {}
    i = 0
    for path in paths:
        path_ids[i] = path
        i += 1
    #print(path_ids)

    paths_lst = path_ids.keys()
    groups = {}
    for key in path_ids:
        groups[key] = []
    # print(groups)
    for i in range(0, len(paths_lst)):
        for j in range(i + 1, len(paths_lst)):
            # print("> Comparing paths {0} and {1}".format(paths_lst[i], paths_lst[j]))
            dependency = dependent(path_ids[paths_lst[i]], path_ids[paths_lst[j]])
            # print("> Paths {0} and {1} are {2} independent".format(path_ids[paths_lst[i]], path_ids[paths_lst[j]], ('','not')[dependency]))
            if dependency:
                #print("> " + str(paths_lst[i]) + ":"+ str(groups[paths_lst[i]]))
                if not groups[paths_lst[i]]:
                    groups[paths_lst[i]] = [paths_lst[j]]
                else:
                    groups[paths_lst[i]].append(paths_lst[j])

    all_path_groups =  []
    visited = set()
    for path in paths_lst:
        if path not in visited:
            group = group_rec_util(groups, path)
            lst = []
            for _id in group:
                lst.append(path_ids[_id])
            all_path_groups.append(lst)
            visited = visited.union(group)

    return all_path_groups

def group_rec_util(groups, curr):
    if not groups[curr]:
        return set([curr])
    paths = set([curr])
    for path in groups[curr]:
        paths = paths.union(group_rec_util(groups, path))
    return list(paths)

def dependent(path1, path2):
    ''' Determines if two paths are dependent: if they share a common edge
        i.e. if they have two common consecutive nodes
    '''
    # we go through an array comparing each value with values in the other
    # array, if we find a similar we check if both next ones are the same
    # if they are not we skip
    # print("> Searching dependency")
    i = 0
    while i < len(path1) - 1:
        # search for path1[i] in path2
        for j in range(0, len(path2)):
            # if node is found compare next, if same return True
            # print(">> Comparing nodes {0} and {1}".format(path1[i], path2[j]))
            if path1[i] == path2[j]:
                # if j + 1 < len(path2):
                #     print(">>> Comparing segments [{0},{1}] and [{2},{3}]".format(path1[i], path1[i + 1], path2[j], path2[j + 1]))
                if j + 1 < len(path2) and path1[i + 1] == path2[j + 1]:
                    #print(">>> Similar segments are [{0},{1}] and [{2},{3}]".format(path1[i], path1[i + 1], path2[j], path2[j + 1]))
                    return True
                else:
                    break
        i += 1
    return False

def seed_MC(seed):
    ''' Perform Monte Carlo simulation on seed to evaluate score
    '''
    nodes_activated_list = []
    for i in range(10000):
        non_activated_nodes = set(graph.keys())
        for node in seed:
            if node in non_activated_nodes:
                propagate(node, non_activated_nodes)
        nodes_activated_list.append(len(graph.keys()) - len(non_activated_nodes))
    return sum(nodes_activated_list) / float(len(nodes_activated_list))

if __name__ == "__main__":
    print("")

    # Create seeds of a specific size
    # size = 11
    # combos = combinations(graph.keys(), size)
    # seeds = []
    # for combo in combos:
    #     # we filter combinations that contain relationships that are useless because nodes are guaranteed to be activated together.
    #     if not(('A' in combo and 'B' in combo) or ('A' in combo and 'C' in combo) or ('K' in combo and 'I' in combo) or ('M' in combo and 'L' in combo) or ('P' in combo and 'Q' in combo) or ('P' in combo and 'T' in combo) or ('R' in combo and 'S' in combo) or ('L' in combo and 'N' in combo) or ('E' in combo and 'F' in combo)):
    #         seeds.append(combo)
    # seed = ['A','E','G','I','H','J','L','O','P','R']
    # print("Seed MC: {0}".format(seed_MC(seed)))
    # print("Exact seed influence score: {0}".format(seed_influence_spread(seed)))
    # print("Optimal seed inf. score: {0}".format(optimal_seed_influence_spread(seed)))
    # print("Found {0} relevant number of seeds of size {1}".format(len(seeds), size))

    # Create all possible seed sets
    size = 10
    seeds = create_seeds(graph, size)
    seeds = tee(seeds, 2)
    seeds_size = sum(1 for _ in seeds[0])
    if size != 0:
        print("Found {0} relevant number of seeds of size {1}".format(seeds_size, size))
    else:
        print("Found {0} relevant number of seeds of all possible size".format(seeds_size))


    # Find best seed set among seeds
    print("\nSearching for best seed set.")
    t0 = time.time()
    opt_seed_set = find_best_seed_set(seeds[1], "hybrid")
    t1 = time.time()
    print("Optimal seed set found in {0} seconds.\n".format(round(t1 - t0, 2)))
    print("Best seed set is: {0}".format(opt_seed_set))

    # opt_seed_set = ['A','E','D','G','I','H','J','L','O','P','R']
    # print("Testing Monte Carlo simulation of optimal seed set.")
    # nodes_activated_list = []
    # for i in range(10000):
    #     non_activated_nodes = set(graph.keys())
    #     for node in opt_seed_set:
    #         if node in non_activated_nodes:
    #             propagate(node, non_activated_nodes)
    #     nodes_activated_list.append(len(graph.keys()) - len(non_activated_nodes))
    # print("MC spread of {0} is {1}".format(opt_seed_set, sum(nodes_activated_list) / float(len(nodes_activated_list))))

    # Testing dependent paths
    test_path1 = ['A','C','E','H','R','P','T']
    test_path2 = ['A','C','E','H','R','T']
    test_path3 = ['B','C','H','A','R','T','X','O']
    test_path4 = ['E','H','C','T']
    # print("")
    # print("Dependency of paths: ({0}, {1}) is {2}\n".format(test_path1, test_path2, dependent(test_path1, test_path2)))
    # print("Dependency of paths: ({0}, {1}) is {2}\n".format(test_path1, test_path3, dependent(test_path1, test_path3)))
    # print("Dependency of paths: ({0}, {1}) is {2}\n".format(test_path2, test_path3, dependent(test_path2, test_path3)))
    # paths = [test_path1, test_path2, test_path3, test_path4]
    # print(find_dependency_groups(paths))
