'''
    Multiprocessing test
'''

import multiprocessing as mp
from multiprocessing import Pool, Array
import numpy as np
import random

def foo(max, size):
    lst = random.sample(range(1, max), size)
    return np.mean(lst)

if __name__ == "__main__":
    '''
    compute foo() x number of times over all cores, each time a foo() ends
    another foo is launched on that server, exactly x foos must be launched
    '''
    pool = Pool(processes = 4)
    results = [pool.apply(foo, (1000, 100)) for x in range(0, 10000)]
    result = np.mean(results)
    print("")
    print(len(results))
    print(result)
