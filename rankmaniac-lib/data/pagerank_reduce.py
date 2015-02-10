#!/usr/bin/env python

import sys

DAMP = .85
# Used for key sorting. C > maximum number of nodes in input.
C = 999999.0

info = None

rank = 0.0
cur_node = None
while True:
    line = sys.stdin.readline()
    if not line:
        break

    # Iteration line: I\tn.
    if line[0] == 'I':
        # Format: 0\tn
        n = int(line.strip().split('\t')[1])
        sys.stdout.write('%6.15f\t%s\n' %(0, n))
    # Counter line: C\tm.
    elif line[0] == 'C':
        # Format: 1\m
        m = int(line.strip().split('\t')[1])
        sys.stdout.write('%6.15f\t%s\n' %(1, m))
    else:
        nodeID, data = line.strip().split('\t')

        if cur_node is None:
            cur_node = nodeID
        if cur_node != nodeID:
            rank = rank * DAMP + 1 - DAMP
            # info is None for deleted/frozen nodes.
            if info:
                # Here, info is N-prerank-neigbor1-neighbor2-....
                sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, cur_node, rank, info))
            rank = 0.0
            cur_node = nodeID
            info = None

        # data can be of two forms:
        # 1) starts with N, then it is the info of pre-rank and neighbors.
        # 2) otherwise, it is part of new-rank.
        if data[0] == 'N':
            info = data
        else:
            rank += float(data)

# Process the last node.
rank = rank * DAMP + 1 - DAMP
if info:
    sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, cur_node, rank, info))
