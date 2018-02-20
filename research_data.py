def valid_models():
    return ["WC", "IC"]


def small_graph_data():
    graph = {
        'A': {'B': 1, 'C': 1},
        'B': {'D': 0.2},
        'C': {'D': 0.2, 'E': 0.3},
        'D': {'E': 0.3, 'G': 0.3, 'I': 0.25},
        'E': {'F': 1, 'D': 0.2, 'H': 0.25},
        'F': {},
        'G': {'D': 0.2, 'H': 0.25, 'L': 0.25},
        'H': {'E': 0.3, 'G': 0.3, 'R': 0.5, 'O': 0.5},
        'I': {'K': 1, 'L': 0.25, 'D': 0.2},
        'J': {'I': 0.25},
        'K': {'I': 0.25},
        'L': {'I': 0.25, 'G': 0.3, 'M': 1, 'N': 1},
        'M': {'L': 0.25},
        'N': {'L': 0.25},
        'O': {'H': 0.25, 'P': 0.5},
        'P': {'T': 1, 'O': 0.5, 'Q': 1},
        'Q': {},
        'R': {'S': 1, 'P': 0.5, 'H': 0.25},
        'S': {'R': 0.5},
        'T': {}
    }

    return graph


def big_graph_data(model="WC"):
    graph, _ = import_hep_WC(model)
    return graph


def import_hep_WC(model="WC"):
    ''' Hep_WC contains:
        15,233 nodes
        62,796 edges
    '''
    print("Importing data from hep_WC.inf")
    file_name = 'data/hep_WC.inf'
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

            if model == "IC":
                inf_network[user1][user2] = 0.1
            elif model == "WC":
                inf_network[user1][user2] = inf_score
            else:
                raise Exception("Unknown model: {}".format(model))

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

    # print(num)
    return (inf_network, conditions)
