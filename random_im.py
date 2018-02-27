'''
    Random IM algorithm
'''

import csv
import random
from monte_carlo import monte_carlo_inf_score_est
import research_data

def target():
    return random.random() > 0.5


def run_all():
    '''
        Runs random on all models
    '''
    pass


def run_live():
    '''
    '''
    seed = set()
    # read from random_models
    model = 'data/small_graph/random_model/small_graph_r0.csv'
    with open(model, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            user = int(line[0])
            if target():
                print("Targeting {}".format(user))
                seed.add(user)
    return seed

if __name__ == "__main__":

    graph = {}
    graph, _ = research_data.import_graph_data('small_graph', 'WC')

    # for every random_model
    #   get seed set for random_model
    #   compute influence spread
    #   save seed set
    seed = run_live()
    inf_spread = monte_carlo_inf_score_est(graph, seed)
    print("Seed: {}".format(seed))
    print("Influence spread is {}".format(inf_spread))
