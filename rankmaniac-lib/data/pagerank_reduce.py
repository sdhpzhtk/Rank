#!/usr/bin/env python

import sys

DAMP = .85
# Used for key sorting. C > maximum number of nodes in input.
C = 999999.0

# Rank threshold. Nodes with ranks below this threshold are eliminated.
rank_thres = 0.1

rank = 0.0
cur_node = None
while True:
    line = sys.stdin.readline()
    if not line:
        break

    # Iteration line: I\tn.
#    if line[0] == 'I':
       # Format: C\tn
#       sys.stdout.write('%6.15f\t%s\n' %(C, line[2]))
#    else:
    if True:
        nodeID, data = line.strip().split('\t')

        if cur_node is None:
            cur_node = nodeID
        if cur_node != nodeID:
            rank = rank * DAMP + 1 - DAMP

            if rank >= rank_thres:
                # Here, info is N-prerank-neigbor1-neighbor2-....
                sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, cur_node, rank, info))
            rank = 0.0
            cur_node = nodeID

        # data can be of two forms:
        # 1) starts with N, then it is the info of pre-rank and neighbors.
        # 2) otherwise, it is part of new-rank.
        if data[0] == 'N':
            info = data
        else:
            rank += float(data)

# Process the last node.
rank = rank * DAMP + 1 - DAMP
if rank >= rank_thres:
    sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, cur_node, rank, info))
