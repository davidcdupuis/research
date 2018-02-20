''' Live Real-Time Bidding Influnce Maximization
'''

import random
from heapq import *
from math import log
import time
import matplotlib.pyplot as plt

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

def influenced(prob):
    return random.random() < prob

class RTBIM:
    def __init__(self, graph):
        self.graph = graph
        self.keys = self.graph.keys()
        self.values = {}
        for key in self.graph:
            self.values[key] = {'inf':0, 'ap':0}

    # --------Monte Carlo -------
    def monte_carlo_seed_score(self, seed):
        ''' Computes Monte Carlo influence score of a seed set
            Does not test already activated nodes
        '''
        pass

    def monte_carlo_influence(self, nodes, num_sim = 10000, timed = False, print_logs = False):
        ''' for each node in nodes, perform num_sim simulations to
            compute influence score assigned to self.values
        '''
        t0 = time.time()
        count = 0
        for node in nodes:
            score = 0.0
            for i in range(1, num_sim + 1):
                result = self.monte_carlo_simulation(node)
                score = score + (result - score)/float(i)# compute dynamic avg
            self.values[node]['inf'] = round(score, 3)
            count += 1
            if print_logs and count % 100 == 0:
                print("> {} node influence score computed".format(count))
        t1 = time.time()
        if timed:
            print("> Monte Carlo method finished computing in {} seconds".format(round(t1 - t0, 2)))

    def monte_carlo_simulation(self, node):
        ''' Perform breadth first random walk from node
            and computes score
        '''
        activated = 0
        activated_nodes = set()
        q = [node]
        while q:
            curr = q.pop(0)
            for neighbor in self.graph[curr]:
                if neighbor not in activated_nodes and influenced(self.graph[curr][neighbor]):
                    activated += 1
                    activated_nodes.add(neighbor)
                    q.append(neighbor)
        return activated

    # --------Monte Carlo -------

    def propagate(self, node, non_activated_nodes):
        q = []
        depth = 0
        q.append((node, depth))
        while q:
            curr = q.pop(0)[0]
            # print("> {}".format(curr))
            # curr = curr[0]
            non_activated_nodes.remove(curr)
            depth += 1
            for neighbor in self.graph[curr]:
                if depth <= 3 and neighbor in non_activated_nodes: # check that neighbor can be activated
                    if influenced(self.graph[curr][neighbor]): # try and influence neighbor with edge probability
                        if True not in [neighbor == i[0] for i in q]:
                            q.append((neighbor, depth))
        return 1

    def compute_inf(self, num_sims = 10000):
        # compute the influence score of each node in graph
        # we do so here by doing 10,000 MC simulations on each node
        for key in self.keys:
            nodes_activated_list = []
            for i in range(num_sims):
                non_activated_nodes = set(self.keys)
                self.propagate(key, non_activated_nodes)
                nodes_activated_list.append(len(self.keys) - len(non_activated_nodes))
            key_inf_score = sum(nodes_activated_list) / float(len(nodes_activated_list))
            # print(key, nodes_activated_list[0:10],key_inf_score)
            self.values[key]['inf'] = round(key_inf_score, 3)
        print("Done computing influence score of keys")

    def update_ap(self, node):
        # update activation probability of all "neighbors" of targeted node
        dist = self.shortest_bfs(node, 3)
        for key in dist:
            if dist[key] != -1:
                # print(key, dist[key])
                old_ap = self.values[key]['ap']
                if dist[key] == float('Inf'):
                    distance = 0
                else:
                    distance = dist[key]
                new_ap = 1 - (1 - old_ap)*(1 - distance)
                self.values[key]['ap'] = round(new_ap, 3)

    def shortest_bfs(self, node, max_depth = 3):
        # find shortest path to all neighbors of depth less than depth
        # stop at depth or when path weight is below min_path
        if not node:
            return
        dist = dict.fromkeys(self.keys, -1)#float('Inf'))
        dist[node] = 0
        depth = 0
        heap = []
        heappush(heap, (dist[node], node, depth))
        while heap:
            curr = heappop(heap)[1]
            depth += 1
            for neighbor in self.graph[curr]:
                if depth <= max_depth:
                    if dist[curr] != -1 and dist[curr] != 0:
                        next_dist = dist[curr] * self.graph[curr][neighbor]
                    else:
                        next_dist = self.graph[curr][neighbor]
                    if dist[neighbor] < next_dist:
                        dist[neighbor] = next_dist
                        heappush(heap, (dist[neighbor], neighbor, depth))
        # print(dist)
        for neighbor in dist:
            if dist[neighbor] == -1:
                dist[neighbor] = 0
        return dist

    def target(self, node):
        ''' Using influence score and activation probability of node decide
            to target (True) or not (False)
        '''
        if self.values[node]['ap'] >= 0.8:
            return False
        return True

    def random_select(self):
        return random.sample(self.graph.keys(), 1)[0]

    def inf_score_distribution(self):
        ''' display the distribution of influence score
            round the scores down to the nearest int
        '''
        values = []
        for key in self.keys:
            values.append(int(self.values[key]['inf']))
        plt.hist(values)
        plt.title("Influence score distribution")
        plt.xlabel("Influence score")
        plt.ylabel("Number of Users")
        plt.show()

    def easyim(self):
        t0 = time.time()
        # implementation of the EaSyIm algorithm to compute influence score of each node
        prev_local_inf = dict.fromkeys(self.keys, 0)

        for i in range(3):
            for node in self.keys:
                curr_local_inf = 0
                for neighbor in self.graph[node]:
                    curr_local_inf += self.graph[node][neighbor]*(1 + prev_local_inf[neighbor])
                prev_local_inf[node] = curr_local_inf

        for node in self.keys:
            self.values[node]['inf'] = prev_local_inf[node]
        t1 = time.time()
        print("EaSyIM finished computing in {} seconds".format(round(t1 - t0, 2)))

    def inf_meth1(self, max_depth):
        ''' Simple method of computing influence score of nodes:
            We take the shortest path between u and any neighbor of max_depth
            and sum it to get the influence score
        '''
        t0 = time.time()
        for node in self.graph.keys():
            distances = self.shortest_bfs(node, max_depth)
            for neighbor in distances:
                self.values[node]['inf'] += distances[neighbor]
        t1 = time.time()
        print("Shortest BFS finished computing in {} seconds".format(round(t1 - t0, 2)))

    def inf_meth2(self, max_depth):
        ''' Simple method of computing influence score of nodes:
            Compute activation probability of any node at most max_depth by
            applying: 1 - (1 - w1)(1 - w2) ... with the weight of each path of
            length at most max_depth.
            Sum the activation probabilities to get the influence score of u.
        '''
        t0 = time.time()
        for node in self.graph.keys():
            inf_score = 0
            neighbors = self.bfs(node, max_depth)
            # compute all paths from u to neighbor
            for neighbor in neighbors:
                ap = 0
                paths = self.find_all_paths_uv_depth(node, neighbor, max_depth)
                print(paths)
                for path in paths:
                    ap = 1 - (1 - ap)*(1 - self.edges_weight(path))
                inf_score += ap
            self.values[node]['inf'] = inf_score

        t1 = time.time()
        print("All paths BFS finished computing in {} seconds".format(round(t1 - t0, 2)))

    def bfs(self, node, max_depth):
        visited = set()
        q = []
        depth = 0
        q.append((node, depth))
        visited.add(node)
        neighbors = set()
        while q:
            top = q.pop(0)
            node = top[0]
            depth = top[1]
            for neighbor in self.graph[node]:
                if depth < max_depth and neighbor not in visited:
                    q.append((neighbor, depth + 1))
                    visited.add(neighbor)
                    neighbors.add(neighbor)
        return neighbors

    def find_all_paths_uv_depth(self, start, end, max_depth, path=[]):
        ''' Function to find all paths between two nodes
        '''
        path = path + [start]
        if start == end:
            return [path]
        if not self.graph.has_key(start):
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path and max_depth >= 0:
                newpaths = self.find_all_paths_uv_depth(node, end, max_depth - 1, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def edges_weight(self, edges):
        ''' Take a list representing a path and compute weight
        '''
        product = 1
        for edge in edges:
            product *= self.graph[edge[0]][edge[1]]
        return product

    def run(self, seed_size, bud = float('Inf'), save = "False"):
        ''' Run targeting test on graph
            k    : number of nodes we want to target before we stop
            save : if "True" saves necessary files to folder
        '''
        # print("")
        # print("Computing influence score of all nodes")
        self.compute_inf()
        # print("Done computing influence score of all nodes")
        # print("-----------------------------------------")
        # print(self.values)
        # print("-----------------------------------------")
        i = 1
        targeted = []
        while i < seed_size:
            node = self.random_select()
            if self.target(node):
                i += 1
                targeted.append(node)
                self.values[node]['ap'] = 1
                self.update_ap(node)

        print("Finished targeting {0} users".format(seed_size))
        print("Users targeted: {0}".format(targeted))
        print("-----------------------------------------")
        print(self.values)
        print("-----------------------------------------")

test_graph = {'A':{'B':2, 'C':2}, 'B':{'D':2}, 'C':{'D':3}, 'D':{}}
test_graph_probs = {'A':{'B':0.2, 'C':0.5}, 'B':{'D':0.5}, 'C':{'D':0.3}, 'D':{}}

if __name__ == "__main__":

    graph = import_hep_WC()[0]

    rtbim = RTBIM(graph)
    # rtbim.run(11)
    # rtbim.compute_inf(10000)
    # rtbim.easyim()
    # rtbim.inf_meth2(3)
    rtbim.monte_carlo_influence(rtbim.graph.keys(), timed = True, print_logs = True)
    # print(rtbim.values)
    rtbim.inf_score_distribution()
    # print(rtbim.find_all_paths_uv_depth('A','E', 3))
    # print(rtbim.all_paths_dls('A', 3))
