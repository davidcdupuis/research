'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''

THETA_AP = 0.8

def inf_scores_graph(graph):
    ''' Compute the influence score of all the nodes in the graph '''
    pass


def target(node):
    ''' Decide whether to target a node or not '''
    if graph[node]['ap'] > THETA_AP or graph[node]['inf'] < theta_inf:
        return False
    return True


def update_ap(graph, node):
    '''
        Updates the activation probability of neighboring nodes
    '''
    pass


def inf_threshold(inf_score_distribution):
    '''
        Compute influence threshold based on influence score distribution
        Selects threshold as top 10% of influencers
    '''
    pass


if __name__ == "__main__":
    '''
        pass argument to test RTIM with Python dic or Neo4J database
        second argument is file or database name to define data to use
    '''

    print("Pre-Processing")

    print("Live")
