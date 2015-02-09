#!/usr/bin/env python

import sys

DAMP = .85
C = 999999.0

rank = 0.0
cur_node = None
while True:
    line = sys.stdin.readline()
    if not line:
        break
    nodeID, data = line.strip().split('\t')
    if cur_node is None:
        cur_node = nodeID
    if cur_node != nodeID:
        rank = rank * DAMP + 1 - DAMP
        sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, cur_node, rank, info))
        rank = 0.0
        cur_node = nodeID

    # data with be of the two forms:
    # 1) start with N, then it is the info of deg and pre rank
    # 2) otherwise, current new rank
    if data[0] == 'N':
        info = data
    else:
        rank += float(data)

# Process the last node
rank = rank * DAMP + 1 - DAMP
sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, cur_node, rank, info))


