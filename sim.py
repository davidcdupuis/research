'''
    SIM: Sample Influence Maximization

    Method to find optimal seed set
    1) Run optimal seed size on given graph. Get optimal size k. Save randomly
       selected nodes to csv file.
    2) Load randomly selected seed. Compute node occurrences and order in
       decreasing order.
    3) Select top k users. Verify performance by computing influence score.
'''

import args
from optimal_size import sim_spread
import optimal_size_mp
import research_data
from monte_carlo import inf_score_est_mp
import operator
from math import ceil


def run(dataset, model, simulations):
    graph, guaranteed = research_data.import_graph_data(dataset, model)
    # print("\nGuaranteed: {}".format(guaranteed))
    # size = find_opt_seed_size(graph, simulations, 100, dataset, model)
    size = optimal_size_mp.run(graph, dataset, model, 100, guaranteed,
                                simulations)
    print("Size: {}".format(size))
    # load saved seeds, compute occurrences
    file_path = "data/{0}/sim/{0}_{1}_sets.csv".format(dataset, model)
    seed_sets = []
    with open(file_path, 'r') as f:
        for line in f:
            data = line.strip("\n").strip(" ").split(" ")
            seed_sets.append(data)

    seeds = {}
    for set in seed_sets:
        for seed in set:
            if seed not in seeds:
                seeds[seed] = 1
            else:
                seeds[seed] += 1

    sorted_seeds = sorted(seeds.items(), key=operator.itemgetter(1),
                          reverse=True)
    # print("\nSeeds: {}\n".format(sorted_seeds))
    opt_seed = []
    i = 0
    while len(opt_seed) < size:
        seed = int(sorted_seeds[i][0])
        if (seed not in guaranteed):
            opt_seed.append(seed)
        i += 1
    # select top k users and compute inf_score
    score = inf_score_est_mp(graph, opt_seed)
    file_path = "data/{}/sim/opt_seed_{}.csv".format(dataset, model)
    with open(file_path, 'w') as f:
        for seed in opt_seed:
            f.write(str(seed))
            f.write("\n")
    print("Optimal seed set saved to {}".format(file_path))

    msg = "Best seed set found score is: {} "
    print(msg.format(score))

if __name__ == "__main__":
    args = args.getArguments("SIM")

    # run optimal seed size for given graph
    for model in args.models:
        for reach in args.reach:
            run(args.dataset, model, args.simulations)
