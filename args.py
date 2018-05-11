
import argparse
import params
import math


def getArguments(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-n", "--simulations", type=int, default=100,
                        help="Number of simulations.")
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help='{}'.format(params.datasets))
    parser.add_argument('-m', '--models', default=['wc'], nargs='+',
                        help='{}'.format(params.models))
    parser.add_argument('-a', '--algorithm', default='rand_repeat',
                        help='{}'.format(params.algorithms))
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
    parser.add_argument("-r", "--reach", default=['100'], nargs='+')
    parser.add_argument("--depth", type=int, default=math.inf)
    args = parser.parse_args()

    if args.dataset not in params.datasets:
        msg = "Invalid arguments [dataset] -> Received: {}"
        raise Exception(msg.format(args.dataset))

    if not set(args.models).issubset(params.models):
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.models))
    else:
        args.models = [float(m) if m != 'wc' else m for m in args.models]

    if args.algorithm not in params.algorithms:
        msg = "Invalid arguments [algorithm] -> Received: {}"
        raise Exception(msg.format(args.algorithm))

    print("-------- Parameters --------")
    print("Dataset \t [{}]".format(args.dataset))
    print("Models \t\t {}".format(args.models))
    print("Reach \t\t {}".format(args.reach))
    print("Algorithm \t [{}]".format(args.algorithm))
    print("Simulations \t {}".format(args.simulations))
    print("Series \t\t {}".format(args.series))
    print("Pre-processing \t [{}]".format(args.pre))
    print("Live \t\t [{}]".format(args.live))
    print("----------------------------")

    return args

if __name__ == "__main__":
    arguments = getArguments("Args")
    print(arguments)
