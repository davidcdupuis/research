'''
    Run GREEDY algorithm on dataset to get seeds
    Inputs:
    * k : if defined stop when reached limit
    * dataset
'''

from monte_carlo import inf_score_est_mp
# from greedy_queue
import matplotlib.pyplot as plt
import research_data
import copy

def getBestSeed(graph, seed = set()):
    '''
        Get best seed of size k
    '''
    print("Starting seed: {}".format(seed))
    best_spread = -1
    best_seed = set()
    for key in graph.keys():
        if key not in seed:
            seed.append(key)
            inf_score = inf_score_est_mp(graph, seed)
            if best_spread < inf_score:
                best_spread = inf_score
                best_seed = copy.deepcopy(seed)
                print("Curr best: {}".format((best_spread, best_seed)))
            seed.remove(key)
    best = (best_spread, best_seed)
    print("Best found: {}".format(best))
    return best


def run(dataset, graph, lim):
    '''
    '''
    seeds = []
    spread = []

    best_seed = []
    for k in range(1, lim+1):
        best = getBestSeed(graph, best_seed)
        best_seed = best[1]
        seeds.append(len(best_seed))
        spread.append(best[0])
        if best[0] >= float(len(graph.keys())):
            break

    plt.plot(seeds, spread, color='blue',label='inf score of seeds')
    plt.xlabel('seeds')
    plt.ylabel('spread')
    plt.title('Influence score vs seeds found')
    plt.savefig('data/{}/greedy.png'.format(dataset))
    plt.close()
    return best_seed

if __name__ == "__main__":
    graph = {}
    graph, _ = research_data.import_graph_data("small_graph", "wc")
    best = run("small_graph", graph, 11)
    print("Best: {}".format(best))
