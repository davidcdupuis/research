''' Python algorithm to find the size of a seed necessary to maximize coverage
    in a social network graph through user influence.
'''

import random
from operator import itemgetter
import numpy as np
import operator
from decimal import Decimal

reverse_graph = {'A':{},
        'B':{'A':1},
        'C':{'A':1},
        'D':{'B':0.2, 'C':0.2, 'E':0.2, 'I':0.2, 'G':0.2},
        'E':{'C':0.3, 'D':0.3, 'H':0.3},
        'F':{'E':1},
        'G':{'D':0.3, 'H':0.3, 'L':0.3},
        'H':{'G':0.25, 'E':0.25, 'R':0.25, 'O':0.25},
        'I':{'J':0.25, 'K':0.25, 'D':0.25, 'L':0.25},
        'J':{},
        'K':{'I':1},
        'L':{'I':0.25, 'G':0.25, 'M':0.25, 'N':0.25},
        'M':{'L':1},
        'N':{'L':1},
        'O':{'N':0.3, 'H':0.3, 'P':0.3},
        'P':{'O':0.5, 'R':0.5},
        'Q':{'P':1},
        'R':{'H':0.5, 'S':0.5},
        'S':{'R':1},
        'T':{'R':0.5, 'P':0.5},
        }

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

def import_hep_WC():
    ''' Hep_WC contains:
        15,233 nodes
        62,796 edges
    '''
    print("Importing data from hep_WC.inf")
    file_name = 'hep_WC.inf'
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
            inf_network[user1][user2] = inf_score
            if inf_score == 1.0:
                if user1 not in condict:
                    condict[user1] = 0
                condict[user1] += 1
                conditions.append((user1, user2))

    print("Done importing hep_WC.inf")
    num = {}
    for key in condict:
        if condict[key] not in num:
            num[condict[key]] = 0
        num[condict[key]] += 1

    print(num)
    return inf_network, conditions

def test(graph):
    non_activated_nodes = set(graph.keys())
    #print("non active> {0}".format(non_activated_nodes))
    seed_size = 0
    while non_activated_nodes:
        curr = random.sample(non_activated_nodes, 1)[0]
        choices[curr] += 1
        propagate(curr, curr, non_activated_nodes)
        seed_size += 1
    return seed_size

def propagate(origin, node, non_activated_nodes):
    #print("> propagate")
    q = []
    q.append(node)
    while q:
        #print("Queue: {0}".format(q))
        curr = q.pop(0)
        # print("non_activated_nodes: {0}".format(non_activated_nodes))
        #print("curr: {0}".format(curr))
        non_activated_nodes.remove(curr)
        if origin not in nodes[curr]:
            nodes[curr][origin] = 1
        else:
            nodes[curr][origin] += 1
        for neighbor in graph[curr]:
            if neighbor in non_activated_nodes: # check that neighbor can be activated
                if influenced(graph[curr][neighbor]): # try and influence neighbor with edge probability
                    #print("add to queue: {0}".format(neighbor))
                    if neighbor not in q:
                        q.append(neighbor)
    return 1

def influenced(prob):
    return random.random() < prob

def display_stats(lst):
    ''' Display list stats
    '''
    _min = np.amin(lst)
    _max = np.amax(lst)
    avg = np.mean(lst)
    var = np.var(lst)
    median = np.median(lst)
    std = np.std(lst)

    print("")
    print("----------------------------------")
    print("Statistics:")
    print("Mean {0}".format(avg))
    print("Variance {0}".format(var))
    print("Median {0}".format(median))
    print("Standard deviation {0}".format(std))
    print("Min value {0}".format(_min))
    print("Max value {0}".format(_max))
    print("----------------------------------")

    return avg

def nCk(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(operator.mul, xrange(n, n-r, -1))
    denom = reduce(operator.mul, xrange(1, r+1))
    return numer//denom

def save_array(sims, mx, ids, file_name):
    with open(file_name, 'w') as f:
        f.write('# Number of ids: {0}\n'.format(len(ids)))
        f.write('# Number of simulations: {0}\n'.format(sims))
        f.write('# Max occurences count: {0}\n'.format(mx))
        f.write('# id id_occurences\n')
        for _id in arr:
            f.write('{0} {1}\n'.format(_id[0], _id[1]))
    print("Number of id occurrences saved to {0}".format(file_name))

def save_stats(file_name):
    with open(file_name, 'w') as f:
        f.write('')
    print("Stats saved to {0}".format(file_name))

def save_seed_set(seed_set, file_name):
    with open(file_name, 'w') as f:
        f.write('# size {0}'.format(len(seed_set)))
        for seed in seed_set:
            f.write('{0}\n'.format(seed))

def special_combinations(iterable, r, nodes_in_condition, pair_conditions):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    ls = []
    for i in indices:
        ls.append(pool[i])

    if all(cond in ls for cond in nodes_in_condition) and all(not(cond[0] in ls and cond[1] in ls) for cond in pair_conditions):
        yield tuple(ls)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        ls = []
        for i in indices:
            ls.append(pool[i])
        if all(cond in ls for cond in nodes_in_condition) and all(not(cond[0] in ls and cond[1] in ls) for cond in conditions):
            yield tuple(ls)

if __name__ == "__main__":
    print("run test")

    #graph, conditions = import_hep_WC()
    # print(len(conditions))
    # conditions = sorted(conditions, key=itemgetter(0))
    # with open('conditions.txt', 'w') as f:
    #     for condition in conditions:
    #         f.write(str(condition) + "\n")
    # print("Conditions file saved to conditions.txt")
    keys = graph.keys()
    print("Number of nodes in graph {0}".format(len(keys)))
    choices = dict.fromkeys(keys, 0)
    nodes = {}
    for key in keys:
        nodes[key] = {}

    # Test for optimal seed size
    num_sim = 100
    print("\nSearching for optimal seed size")
    seed_sizes = []
    cnt = 0
    for i in range(num_sim):
        seed_sizes.append(test(graph))
        cnt += 1
        if cnt % num_sim / 10 == 0:
            print("> " + str(cnt))

    #
    # keyslist = []
    # for key, value in choices.iteritems():
    #     keyslist.append([key, value])
    # keyslist = sorted(keyslist, key=itemgetter(1), reverse=True)
    # for key in keyslist:
    #     print("> {0}".format(key))

    opt_k = round(display_stats(seed_sizes))
    # print("Optimal seed set sizes is {0}".format(seed_sizes[0:11]))
    print("\nOptimal seed set size is {0}".format(opt_k)) # sum(seed_sizes) / float(len(seed_sizes))
    print("")

    '''Compute number of combinations necessary'''
    # nodes_in_best_seed = []
    # for choice in choices:
    #     if choices[choice] == num_sim:
    #         nodes_in_best_seed.append(choice)
    # print(len(nodes_in_best_seed))
    # result = sum(1 for i in special_combinations(keys, int(opt_k), nodes_in_best_seed, conditions))
    # result_text = "{:.2E}".format(Decimal(result))
    # print("Number of combinations to check is {0}".format(result_text))

    '''Display count of number of occurrences'''
    l = int(num_sim - (num_sim * 5.0/100.0))
    cnt = {}
    arr = []
    i = 0
    for choice in choices:
        arr.append((choice, choices[choice]))
        if choices[choice] >= l:
            val = int(choices[choice])
            if val not in cnt:
                cnt[val] = 0
            cnt[val] += 1
        i += 1
    print(cnt)

    '''Save number of occurences for each id'''
    arr = sorted(arr, key=itemgetter(1), reverse=True)
    save_array(num_sim, cnt[num_sim], arr, 'id_occurrences.txt' )

    # opt_seed_set = ['A','G','F','K','J','M','N','Q','S','T']
    '''Compute influence spread of optimal seed set'''
    # opt_seed_set = []
    # for i in range(int(opt_k)):
    #     opt_seed_set.append(arr[i][0])
    #
    # save_seed_set(opt_seed_set, 'seed_set.txt')
    # print(len(opt_seed_set))
    #
    # nodes_activated_list = []
    # for i in range(100):
    #     non_activated_nodes = set(graph.keys())
    #     for node in opt_seed_set:
    #         if node in non_activated_nodes:
    #             propagate(node, node, non_activated_nodes)
    #     nodes_activated_list.append(len(graph.keys()) - len(non_activated_nodes))
    # print("MC spread of the opt_seed_set is {0}".format(sum(nodes_activated_list) / float(len(nodes_activated_list))))
