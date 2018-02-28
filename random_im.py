'''
    Random IM algorithm
'''

import csv
import random
from monte_carlo import monte_carlo_inf_score_est
import research_data


def target():
    return random.random() > 0.5


def save_data(dataset, model, serie, seed_size, seed_spread):
    '''
    '''
    file_name = 'data/{0}/random_im/results/random_im_{0}_{1}_s{2}_results.txt'
    file_name = file_name.format(dataset, model, serie)
    with open(file_name, 'w') as f:
        f.write('Random IM processing data\n')
        tmp = 'User availability model: {0}_s{1}.csv\n'
        f.write(tmp.format(dataset, serie))
        f.write('Seed size: {}\n'.format(seed_size))
        f.write('Seed spread: {}\n'.format(seed_spread))

    print('> Saved Random IM data to results')


def save_seed(seeds, inf_spread, dataset, model, serie='0'):
    '''
        Save seed set to csv file,
        Save influence spread as well
    '''
    file_name = "data/{0}/random_im/seeds/{0}_{1}_s{2}_seeds.csv"
    file_name = file_name.format(dataset, model, serie)
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(["influence_spread:", inf_spread])
        for seed in seeds:
            writer.writerow([seed])
    print("> Seed set saved.")


def run(graph, dataset, model, serie):
    '''
        Runs Random IM on random_model
        Save results
    '''
    seed = set()
    # read from random_models
    file_name = 'data/{0}/random_model/{0}_s{1}.csv'.format(dataset, serie)
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            user = int(line[0])
            if target():
                seed.add(user)

    inf_spread = monte_carlo_inf_score_est(graph, seed)
    print("Influence spread is {}".format(inf_spread))
    save_seed(seed, inf_spread, dataset, model, serie)
    save_data(dataset, model, serie, len(seed), inf_spread)


if __name__ == "__main__":
    graph = {}
    graph, _ = research_data.import_graph_data('small_graph')

    run(graph, 'small_graph', 'wc' ,0)
