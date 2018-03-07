#!/usr/bin/python3
'''
'''

import csv


if __name__ == "__main__":
    with open('../TwitterData/nodes.csv', 'w', newline='') as f:
        writer = csv.writer(f)

    nodes = set()
    count = 0
    with open('../TwitterData/twitter_rv.net', 'r') as f1:
        with open('../TwitterData/nodes.csv', 'a', newline='') as f2:
            reader = csv.reader(f1, delimiter='\t')
            writer = csv.writer(f2)
            for line in reader:
                count += 1
                user = line[0]
                follower = line[1]
                if user not in nodes:
                    writer.writerow([user])
                writer.writerow([follower])
                if len(nodes) == 1000:
                    nodes.pop()
                nodes.add(user)
                if count % 1000000 == 0:
                    print("Processed {} lines!".format(count))
