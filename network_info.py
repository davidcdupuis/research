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

def avg_degrees(graph):
    ''' computes avg # of degrees '''
    pass

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

    avg = avg_edge_weight(graph)
    print("Average edge weight is {}".format(avg))
