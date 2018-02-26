#!/usr/bin/python3
'''
  RTIM: our Real-Time Bidding Influence Maximization Strategy

  Takes place in two steps:
    * pre-processing: compute independent influence score of all nodes
    * live: compute activation probability of available node
'''
import csv
from multiprocessing import Process, Queue, Lock, cpu_count
from MonteCarlo import monte_carlo_inf_score_est
import argparse
import research_data

THETA_AP = 0.8

SENTINEL = "STOP"


class Feeder(Process):
    """Queue Feeder

    Extends:
        Process

    """
    _queue = None
    _data = None

    def __init__(self, queue, node_list):
        self._queue = queue
        self._data = node_list
        super(Feeder, self).__init__()

    def run(self):
        # Put all data in queue
        for node in self._data:
            self._queue.put(node)

        # Add a specific data to identify end of data
        self._queue.put(SENTINEL)


class Writer(Process):
    """Process who writes resutl to csv

        Will get everything in result_queue and write it to csv
    """
    _queue = None

    def __init__(self, queue):
        self._queue = queue
        super(Writer, self).__init__()

    def run(self):
        with open("results.csv", "w") as f:
            writer = csv.writer(f)
            while True:
                line = self._queue.get()
                if line == SENTINEL:
                    break
                writer.writerow(line)


class Worker(Process):
    """Process that do the job!

    """
    _queue = None
    _lock = None
    _graph = None

    def __init__(self, queue, graph, result_queue):
        self._queue = queue
        self._graph = graph
        self._result_queue = result_queue
        super(Worker, self).__init__()

    def run(self):
        while True:
            node = self._queue.get()
            if node == SENTINEL:
                self._queue.put(SENTINEL)
                break

            res = monte_carlo_inf_score_est(self._graph, [node])
            self._result_queue.put([node, res])


def manage_processes(graph):
    """Launch process for computation.

    Launch:
        - 1 process to fedd data queue (Feeder)
        - 1 process to write result to CSV (Writer)
        - X process for doing the job

    Arguments:
        graph (dict): The grap to compute
    """
    processes = []

    # Instantiate data queue  feeder
    queue = Queue()
    feeder = Feeder(queue, graph.keys())
    processes.append(feeder)

    # Instantiate and start result writer
    result_queue = Queue()
    writer = Writer(result_queue)
    writer.start()

    # Instantiate  workers
    for i in range(cpu_count() - 2):
        p = Worker(queue, graph, result_queue)
        processes.append(p)

    # Launch workers
    for p in processes:
        p.start()

    # Queue is ready!
    queue.close()

    # Wiat for work to be one
    for p in processes:
        p.join()

    # Send STOP signal to writer
    # If this  signal is not sent, process will nevere end!
    result_queue.put(SENTINEL)
    writer.join()


if __name__ == "__main__":
    '''
        pass argument to test RTIM with Python dic or Neo4J database
        second argument is file or database name to define data to use
    '''
    parser = argparse.ArgumentParser(description="Multi-process optsize")
    parser.add_argument('--small', default=False, action="store_true",
                        help="Whether to use the small graph or the big one.")
    parser.add_argument("--model", default="WC", help="Model to use")
    args = parser.parse_args()

    if args.model not in research_data.valid_models():
        msg = "Invalid arguments [model] -> Received: {}"
        raise Exception(msg.format(args.model))

    graph_size = ""
    if args.small:
        graph_size = "small"
    else:
        graph_size = "large"

    msg = "Pre-processing {} graph using RTIM\n"
    msg += "Use model: {}"
    print(msg.format(graph_size, args.model))

    graph = {}
    if args.small:
        graph = research_data.small_graph_data()
    else:
        graph = research_data.big_graph_data(args.model)

    manage_processes(graph)
