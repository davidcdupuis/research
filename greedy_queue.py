import csv
import argparse

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
    """Process who writes result to csv

        Will get everything in result_queue and write it to csv
    """
    _queue = None

    def __init__(self, queue):
        self._queue = queue
        self.results_dir = "results.csv"
        super(Writer, self).__init__()

    def run(self):
        with open(self.results_dir, "w", newline='') as f:
            writer = csv.writer(f)
            while True:
                line = self._queue.get()
                if line == SENTINEL:
                    break
                writer.writerow(line)


class Worker(Process):
    """Process that does the job!

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
