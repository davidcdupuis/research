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
import plot

datasets = ['small_graph', 'hep', 'hept', 'phy']
models = ['wc', '0.1', '0.01', '0.3', '0.5', '0.7', '0.8', '0.9', '1.0']
algorithms = ['rtim', 'rand_repeat', 'rand_no_repeat', 'opt_size']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main")
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help='{}'.format(datasets))
    parser.add_argument('-m', '--models', default=['wc'], nargs='+',
                        help='{}'.format(models))
    parser.add_argument('-a', '--algorithm', default='rand_repeat',
                        help='{}'.format(algorithms))
    parser.add_argument('-s', '--series', default=[0], type=int, nargs='+',
                        help='What availability series to use.')
    parser.add_argument("--pre", default=False, action="store_true",
                        help="Whether you want to RTIM pre-process")
    parser.add_argument("--live", default=False, action="store_true",
                        help="Whether you want to run RTIM live")
    parser.add_argument("--test", default=False, action="store_true",
                        help="RTIM: Test top and theta_ap parameters")
    parser.add_argument("--new", default=False, action="store_true",
                        help="Launch new test")
    args = parser.parse_args()

    if args.dataset not in datasets:
        msg = "Invalid arguments [dataset] -> Received: {}"
        raise Exception(msg.format(args.dataset))

    if not set(args.models).issubset(models):
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.models))
    else:
        args.models = [float(m) if m != 'wc' else m for m in args.models]

    if args.algorithm not in algorithms:
        msg = "Invalid arguments [algorithm] -> Received: {}"
        raise Exception(msg.format(args.algorithm))

    print("-------- Parameters --------")
    print("Dataset \t [{}]".format(args.dataset))
    print("Models \t\t {}".format(args.models))
    print("Algorithm \t [{}]".format(args.algorithm))
    print("Series \t\t {}".format(args.series))
    print("Pre-processing \t [{}]".format(args.pre))
    print("Live \t\t [{}]".format(args.live))
    print("----------------------------")

    if (args.pre and args.algorithm != 'random_im'
        and args.algorithm != 'opt_size'):
        print("Launched {} pre-processing!".format(args.algorithm))
        for model in args.models:
            graph = {}
            graph, _ = research_data.import_graph_data(args.dataset, model)
            if args.algorithm == 'rtim':
                rtim.run_pre_processing(graph, args.dataset, model)

    if args.live and args.algorithm != 'opt_size':
        print("Launched {} live!".format(args.algorithm))
        for model in args.models:
            graph = {}
            graph, _ = research_data.import_graph_data(args.dataset, model)
            for serie in args.series:
                if args.algorithm == 'rtim':
                    rtim.run_live(graph, args.dataset, model, serie)
                elif args.algorithm == 'rand_repeat':
                    random_im.run_repeat(graph, args.dataset, model, serie)
                elif args.algorithm == 'rand_no_repeat':
                    random_im.run_no_repeat(graph, args.dataset, model, serie)

    if args.algorithm == 'opt_size':
        print("Computing optimal size of seed set!")
        for model in args.models:
            graph = {}
            graph, _ = research_data.import_graph_data(args.dataset, model)
            size = optimal_size_mp.run(graph, args.dataset, model)

    if args.test:
        # tops = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80,
        #        85, 90, 95, 100]
        tops = [45, 50, 55, 60, 65, 70]
        theta_aps = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
        new = False
        for model in args.models:
            graph = {}
            graph, _ = research_data.import_graph_data(args.dataset, model)
            for serie in args.series:
                for thresh in theta_aps:
                    for t in tops:
                        print(" Parameters: {} - {}%".format(thresh, t))
                        rtim.run_live(graph, args.dataset, model, serie, thresh,
                                      t, float('inf'), True, new)
                        if new:
                            new = False
            # plot.rtim_plot_test_parameters(args.dataset)
