#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

# Number of nodes for printing in final rank
NUM_SHOW = 20
# Number of nodes we check for convergence
N = max(20, NUM_SHOW)

sum = 0.0

# The lines for "FinalRank"
final_ranks = []

# the pre-rank of the previous node, for checking stopping criteria
last_pre_rank = None

# The lines of actuall node info
lines = []
stop = True

# cnt keeps the number of lines in final_ranks
cnt = 0

# We first process N nodes
for i in xrange(N):
    line = sys.stdin.readline()
    if not line:
        break
    
    # Note we combined the data with '-' in pagerank_process
    data = (line.strip().split('\t')[1]).split('-')
    nodeID = data[0]
    rank = float(data[1])
    pre_rank = float(data[2][1:])
    links = data[3:]

    line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
    if links:
        line += ',' + ','.join(links)
    line += '\n'
    lines.append(line)

    # Stop criteria:
    # 1) difference between the current and previous rank is small
    # 2) the relative ranking between the current N nodes has not changed
    if last_pre_rank is not None and (abs(rank - pre_rank) > .005 or last_pre_rank < pre_rank):
        stop = False
        break
    last_pre_rank = pre_rank

    if cnt < NUM_SHOW:
        cnt += 1
        final_ranks.append('FinalRank:%f\t%s\n' %(rank, nodeID))

if stop:
    # If we have reached the stopping criteria, then print out results
    # and consume all inputs
    for line in final_ranks[:NUM_SHOW]:
        sys.stdout.write(line)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
else:
    # Otherwise, read in all inputs and output back the corresponding format
    for line in lines:
        sys.stdout.write(line)
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        data = (line.strip().split('\t')[1]).split('-')
        nodeID = data[0]
        rank = float(data[1])
        pre_rank = float(data[2][1:])
        links = data[3:]
        
        line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
        if links:
            line += ',' + ','.join(links)
        line += '\n'
        sys.stdout.write(line)




