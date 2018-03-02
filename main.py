#!/usr/bin/python3
'''
    From here run any type of algorithm on any dataset with any user
    availability model
'''

import argparse
import rtim
import random_im
import optimal_size_mp
import research_data

datasets = ['small_graph', 'hep', 'hept', 'phy']
models = ['wc', '0.1', '0.01', '0.3', '0.5', '0.8', '0.9']
algorithms = ['rtim', 'rand_repeat', 'rand_no_repeat', 'opt_size']

if __name__ == "__main__":
    parser = parser = argparse.ArgumentParser(description="Main")
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help='{}'.format(datasets))
    parser.add_argument('-m', '--model', default='wc',
                        help='{}'.format(models))
    parser.add_argument('-a', '--algorithm', default='random',
                        help='{}'.format(algorithms))
    parser.add_argument('--series', default=[0], type=int, nargs='+',
                        help='What availability series to use.')
    parser.add_argument("--pre", default=False, action="store_true",
                        help="Whether you want to RTIM pre-process")
    parser.add_argument("--live", default=False, action="store_true",
                        help="Whether you want to run RTIM live")
    args = parser.parse_args()

    if args.dataset not in datasets:
        msg = "Invalid arguments [dataset] -> Received: {}"
        raise Exception(msg.format(args.dataset))

    if args.model not in models:
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))
    else:
        if args.model != 'wc':
            args.model = float(args.model)

    if args.algorithm not in algorithms:
        msg = "Invalid arguments [algorithm] -> Received: {}"
        raise Exception(msg.format(args.algorithm))

    print("-------- Parameters --------")
    print("Dataset \t [{}]".format(args.dataset))
    print("Model \t\t [{}]".format(args.model))
    print("Algorithm \t [{}]".format(args.algorithm))
    print("Series \t\t {}".format(args.series))
    print("Pre-processing \t [{}]".format(args.pre))
    print("Live \t\t [{}]".format(args.live))
    print("----------------------------")

    graph = {}
    graph, _ = research_data.import_graph_data(args.dataset, args.model)

    if (args.pre and args.algorithm != 'random_im'
        and args.algorithm != 'opt_size'):
        print("Launched {} pre-processing!".format(args.algorithm))
        for serie in series:
            if args.algorithm == 'rtim':
                rtim.run_pre_processing(graph, args.dataset, args.model, serie)

    if args.live and args.algorithm != 'opt_size':
        print("Launched {} live!".format(args.algorithm))
        for serie in args.series:
            if args.algorithm == 'rtim':
                rtim.run_live(graph, args.dataset, args.model, serie)
            elif args.algorithm == 'rand_repeat':
                random_im.run_repeat(graph, args.dataset, args.model, serie)
            elif args.algorithm == 'rand_no_repeat':
                random_im.run_no_repeat(graph, args.dataset, args.model, serie)

    if args.algorithm == 'opt_size':
        print("Computing optimal size of seed set!")
        size = optimal_size_mp.run(graph, args.dataset, args.model)
