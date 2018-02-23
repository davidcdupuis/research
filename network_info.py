'''
    Python script to find topological information of a network
    - average edge weight
    - # connected components
    - average number of node degrees
    - ...
'''

import research_data
import argparse


def avg_edge_weight(graph):
    ''' computes the avg edge weight of a graph '''
    avg = 0.0
    count = 0.0
    for key in graph.keys():
        for neighbor in graph[key].keys():
            count += 1.0
            avg = avg + (graph[key][neighbor] - avg)/count
    return avg


def conn_components(graph):
    ''' computes # connected components in graph '''
    pass


def avg_out_degrees(graph):
    ''' computes avg # of out degrees '''
    avg = 0
    count = 0
    for key in graph.keys():
        count += 1
        avg = avg + (len(graph[key].keys()) - avg)/count
    return avg


def not_reachable(graph):
    ''' Computes number of nodes not reachable by another node '''
    # initialize an array of all nodes
    non_reachable = set(graph.keys())
    for key in graph.keys():
        for neighbor in graph[key]:
            if neighbor in non_reachable:
                non_reachable.remove(neighbor)
    return len(non_reachable)


def num_nodes(graph):
    ''' Returns number of nodes in graph '''
    return len(graph.keys())

def num_edges(graph):
    ''' Returns number of edges in graph '''
    edges = 0
    for key in graph.keys():
        for neighbor in graph[key].keys():
            edges += 1
    return edges

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument('--small', default=False, action="store_true",
                        help="Whether to use the small graph or the big one.")
    parser.add_argument("--model", default="WC", help="Model to use")
    args = parser.parse_args()

    if args.model not in research_data.valid_models():
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))

    msg = "Use model: {}"
    print(msg.format(args.model))

    graph = {}
    if args.small:
        graph = research_data.small_graph_data(args.model)
    else:
        graph = research_data.big_graph_data(args.model)

    num_nodes = num_nodes(graph)
    print("Number of nodes in graph: {}".format(num_nodes))
    
    num_edges= num_edges(graph)
    print("Number of edges in graph: {}".format(num_edges))

    avg_edge = avg_edge_weight(graph)
    print("Average edge weight is {}".format(avg_edge))

    avg_out = avg_out_degrees(graph)
    print("Average out degree is {}".format(avg_out))

    non_reachability = not_reachable(graph)
    print("Number of non reachable nodes {}".format(non_reachability))
