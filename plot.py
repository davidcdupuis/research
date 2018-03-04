'''
    functions to plot data from algorithms
'''

import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv

datasets = ['small_graph', 'hep', 'hept', 'phy']

def rtim_plot_test_parameters(dataset):
    '''
        Plot test parameters from RTIM test
    '''
    print("> Plotting test parameter plots!")
    # start by reading data from csv
    file_name = 'data/{0}/rtim/results/{0}_test.csv'
    file_name = file_name.format(dataset)
    df = pd.read_csv(file_name)
    # print(df.head())
    series = df.serie.unique()
    aps = df.theta_ap.unique()
    print(": Done importing data!")
    colors = {0.5: 'blue',
              0.6: 'red',
              0.7: 'green',
              0.8: 'orange',
              0.9: 'purple',
              0.95: 'pink'
              }

    for serie in series:
        plt.figure()
        for ap in aps:
            cols = ['serie', 'spread', 'top', 'theta_ap']
            cond = ((df['theta_ap'] == ap) & (df['serie'] == serie))
            tmp_df = df.loc[cond][cols]
            l = 'theta_ap: {}'.format(ap)
            plt.plot(tmp_df.top, tmp_df.spread, colors[ap],
                     label=l)
        plt.title('% influencers vs inf spread - s{}'.format(serie))
        plt.ylabel('influence spread')
        plt.xlabel('top influencers %')
        lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plot_name = 'data/{0}/rtim/results/{0}_s{1}_test.png'
        plt.savefig(plot_name.format(dataset, serie),
                    bbox_extra_artists=(lgd,),
                    bbox_inches='tight')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main")
    parser.add_argument('-d', '--dataset', default='small_graph',
                        help='{}'.format(datasets))
    args = parser.parse_args()

    if args.dataset not in datasets:
        msg = "Invalid arguments [dataset] -> Received: {}"
        raise Exception(msg.format(args.dataset))

    rtim_plot_test_parameters(args.dataset)
