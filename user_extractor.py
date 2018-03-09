#!/usr/bin/python3
'''
'''

import csv
import argparse

def extract_users():
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

def extract_num_followers():
    with open('../TwitterData/num_followers.csv', 'w', newline='') as f:
        writer= csv.writer(f)
    count = 0
    with open('../TwitterData/twitter_rv.net', 'r') as f1:
        with open('../TwitterData/num_followers.csv', 'a', newline='') as f2:
            reader = csv.reader(f1, delimiter='\t')
            writer = csv.writer(f2, delimiter='\t')
            first_line = next(reader)
            user = first_line[0]
            follower_count = 1
            for line in reader:
                count += 1
                if line[0] != user:
                    writer.writerow([user, follower_count])
                    user = line[0]
                    follower_count = 1
                else:
                    follower_count += 1
                if count % 10000000 == 0:
                    print("Processed {} lines!".format(count))
            writer.writerow([user, follower_count])

def extract_sample_edges():
    with open('../TwitterData/twitter_sample.csv', 'w', newline='') as f:
        writer = csv.writer(f)
    with open('../TwitterData/twitter_rv.net', 'r') as f1:
        with open('../TwitterData/twitter_sample.csv', 'a', newline='') as f2:
            reader = csv.reader(f1, delimiter='\t')
            writer = csv.writer(f2, delimiter='\t')
            line_count = 0
            first_line = next(reader)
            user = first_line[0]
            user_count = 1
            for line in reader:
                follower = line[1]
                if line[0] != user:
                    user = line[0]
                    user_count = 1
                    writer.writerow([user, follower])
                    line_count += 1
                else:
                    if user_count <= 100:
                        writer.writerow([user, follower])
                        line_count += 1
                        user_count += 1
                if line_count >= 10000000:
                    print("Line_count: {}".format(line_count))
                    break

def extract_sample_users():
    with open('../TwitterData/nodes_sample.csv', 'w', newline='') as f:
        writer = csv.writer(f)

    nodes = set()
    count = 0
    with open('../TwitterData/twitter_sample.csv', 'r') as f1:
        with open('../TwitterData/nodes_sample.csv', 'a', newline='') as f2:
            reader = csv.reader(f1, delimiter='\t')
            writer = csv.writer(f2)
            for line in reader:
                count += 1
                user = line[0]
                follower = line[1]
                if user not in nodes:
                    writer.writerow([user])
                    nodes.add(user)
                if follower not in nodes:
                    writer.writerow([follower])
                if len(nodes) == 1000:
                    nodes.pop()
                if count % 10000000 == 0:
                    print("Processed {} lines!".format(count))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main")
    parser.add_argument("--users", default=False, action="store_true",
                        help="run extract_users")
    parser.add_argument("--followers", default=False, action="store_true",
                        help="run extract_num_followers")
    parser.add_argument("--sampleEdges", default=False, action="store_true",
                        help="run extract_num_followers")
    parser.add_argument("--sampleUsers", default=False, action="store_true",
                        help="run extract_num_followers")
    args = parser.parse_args()

    if args.users:
        extract_users
    if args.followers:
        extract_num_followers()
    if args.sampleEdges:
        extract_sample_edges()
    if args.sampleUsers:
        extract_sample_users()
