'''
    Convert graph.inf file by replacing
    node ids by appropriate index value in array
'''

import args
from research_data import import_graph_data

def run(dataset):
    # step 1 load graph
    graph = import_graph_data(dataset)[0]

    # step 2 get keys and order them
    sorted_keys = sorted(graph.keys())

    # step 3 in new equivalency dict, assign index value to keys
    equivalency = {}
    for i in range(len(sorted_keys)):
        equivalency[sorted_keys[i]] = i

    # step 4 save graph back to file
    file_name = "data/{}/indexed_{}_wc.inf".format(dataset)
    with open(file_name, 'w') as f:
        for key in graph.keys():
            for neighbor in graph[key].keys():
                line = str(equivalency[key]) + ' '
                line += str(equivalency[neighbor]) + ' '
                line += str(graph[key][neighbor]) + "\n"
                f.write(line)

if __name__ == "__main__":
    args = args.getArguments("idToIndex")
    run(args.dataset)
