'''
    Random IM algorithm
'''

import csv
import random
from monte_carlo import inf_score_est_mp
import research_data


def target():
    return random.random() > 0.5


def save_data(algorithm, dataset, model, serie, seed_size, seed_spread):
    '''
    '''
    file_name = 'data/{0}/{1}/results/{1}_{0}_{2}_s{3}_results.txt'
    file_name = file_name.format(dataset, algorithm, model, serie)
    with open(file_name, 'w') as f:
        f.write('Random IM processing data\n')
        tmp = 'User availability model: {0}_s{1}.csv\n'
        f.write(tmp.format(dataset, serie))
        f.write('Seed size: {}\n'.format(seed_size))
        f.write('Seed spread: {}\n'.format(seed_spread))

    print('> Saved Random IM data to results')


def save_seed(algorithm, seeds, inf_spread, dataset, model, serie='0'):
    '''
        Save seed set to csv file,
        Save influence spread as well
    '''
    file_name = "data/{0}/{1}/seeds/{1}_{0}_{2}_s{3}_seeds.csv"
    file_name = file_name.format(dataset, algorithm, model, serie)
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(["influence_spread:", inf_spread])
        for seed in seeds:
            writer.writerow([seed])
    print("> Seed set saved.")


def run_repeat(graph, dataset, model, serie, max_size=float('inf')):
    '''
        Runs Random IM on random_model
        Save results
        max_size = IM budget/numbers of users that can be targeted
    '''
    print("> Running Random IM on {}/{}/s{}".format(dataset, model, serie))
    seed = set()
    # read from random_models
    file_name = 'data/{0}/random_model/{0}_s{1}.csv'.format(dataset, serie)
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            user = int(line[0])
            if target() and len(seed) <= max_size:
                seed.add(user)

    print(": Finished targeting!")
    inf_spread = inf_score_est_mp(graph, seed)
    print("Influence spread is {}".format(inf_spread))
    save_seed('rand_repeat', seed, inf_spread, dataset, model, serie)
    save_data('rand_repeat', dataset, model, serie, len(seed), inf_spread)
    print(": Finished running Random IM.")

def run_no_repeat(graph, dataset, model, serie, max_size=float('inf')):
    '''
        Runs Random IM with non repeat property: it doesn't retarget a user
        that has already been targeted
        max_size = number of users that can be targeted
    '''
    print("> Running Random IM on {}/{}/s{}".format(dataset, model, serie))
    seed = set()
    # read from random_models
    file_name = 'data/{0}/random_model/{0}_s{1}.csv'.format(dataset, serie)
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            user = int(line[0])
            if target() and user not in seed and len(seed) <= max_size:
                seed.add(user)

    print(": Finished targeting!")
    inf_spread = inf_score_est_mp(graph, seed)
    print("Influence spread is {}".format(inf_spread))
    save_seed('rand_no_repeat', seed, inf_spread, dataset, model, serie)
    save_data('rand_no_repeat', dataset, model, serie, len(seed), inf_spread)
    print(": Finished running Random IM.")

if __name__ == "__main__":
    graph = {}
    graph, _ = research_data.import_graph_data('small_graph')

    run(graph, 'small_graph', 'wc' ,0)
