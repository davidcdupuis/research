import random

class IMServer():
    def __init__(self):
        self.activated = set()
        self.graph = {'A':{},
                'B':{'A':1},
                'C':{'A':1},
                'D':{'B':0.2, 'C':0.2, 'E':0.2, 'I':0.2, 'G':0.2},
                'E':{'C':0.3, 'D':0.3, 'H':0.3},
                'F':{'E':1},
                'G':{'D':0.3, 'H':0.3, 'L':0.3},
                'H':{'G':0.25, 'E':0.25, 'R':0.25, 'O':0.25},
                'I':{'J':0.25, 'K':0.25, 'D':0.25, 'L':0.25},
                'J':{},
                'K':{'I':1},
                'L':{'I':0.25, 'G':0.25, 'M':0.25, 'N':0.25},
                'M':{'L':1},
                'N':{'L':1},
                'O':{'N':0.3, 'H':0.3, 'P':0.3},
                'P':{'O':0.5, 'R':0.5},
                'Q':{'P':1},
                'R':{'H':0.5, 'S':0.5},
                'S':{'R':1},
                'T':{'R':0.5, 'P':0.5},
                }

    def run(self):
        # runs model on graph while communicating with RTBServer
        pass

    def pre_process(self):
        pass

    def live_process(self):
        pass

if __name__ == '__main__':
    imserver = IMServer()
    imserver.run()
