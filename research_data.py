def valid_models():
    return ["WC", "0.1","0.01","0.5","0.9"]


def import_graph_data(fname, model="WC"):
    ''' Hep_WC contains:
        15,233 nodes
        62,796 edges
    '''
    print("> Importing data from {}".format(fname))
    file_name = 'data/' + fname
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

            if model == "0.1":
                inf_network[user1][user2] = 0.1
            elif model == "0.01":
                inf_network[user1][user2] = 0.01
            elif model == "WC":
                inf_network[user1][user2] = inf_score
            else:
                raise Exception("Unknown model: {}".format(model))

            if inf_score == 1.0:
                if user1 not in condict:
                    condict[user1] = 0
                condict[user1] += 1
                conditions.append((user1, user2))

    print(": Done importing {}".format(fname))
    num = {}
    for key in condict:
        if condict[key] not in num:
            num[condict[key]] = 0
        num[condict[key]] += 1

    # print(num)
    return (inf_network, conditions)


def import_inf_scores_csv(file_name):
    '''
    '''
    inf_scores = {}
    with open(file_name, "r") as f:
        for line in f:
            vals = line.strip("\n").split(",")
            inf_scores[vals[0]] = float(vals[1])
    return inf_scores

if __name__ == "__main__":
    import_inf_scores_csv('results.csv')
