#!/usr/bin/env python

import sys

# Maximum number of iterations.
MAX_ITER = 50

# Number of top nodes to be computed.
NUM_SHOW = 20
# Number of nodes checked for convergence.
N = max(50, NUM_SHOW)

# The lines for "FinalRank".
final_ranks = []

# The pre-rank of the previous node, for checking stopping criterion.
last_pre_rank = None

# The input lines (containing node info) for the next iteration.
lines = []
stop = True

# count is the number of lines in final_ranks.
count = 0

# Read the iteration line. It is the first line since only it has key 0.
line = sys.stdin.readline()
num_iter = int(line.strip().split('\t')[1])

# We first process the top N nodes.
for i in xrange(N):
    line = sys.stdin.readline()
    if not line:
        break
    
    # data format: nodeId-rank-N-prerank-neighbor1-neighbor2-...
    data = (line.strip().split('\t')[1]).split('-')
    nodeID = data[0]
    rank = float(data[1])
    # Skip data[2] which is 'N'.
    pre_rank = float(data[3])
    neighbors = data[4:]

    line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
    if neighbors:
        line += ',' + ','.join(neighbors)
    line += '\n'

    lines.append(line)

    # Stopping criteria:
    # 1) Relative change in rank for the node is small.
    # 2) The relative ranking among the current N nodes has not changed.
    if (num_iter < MAX_ITER) and \
       ((abs(rank - pre_rank)/pre_rank > .001) or \
        (last_pre_rank is not None and last_pre_rank < pre_rank)):
        stop = False
        break

    last_pre_rank = pre_rank

    if count < NUM_SHOW:
        count += 1
        final_ranks.append('FinalRank:%f\t%s\n' %(rank, nodeID))

    if count == NUM_SHOW and num_iter == MAX_ITER:
        break

if stop:
    # If we have reached the stopping criteria, then print out results
    # and consume all inputs.
    for line in final_ranks:
        sys.stdout.write(line)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
else:
    # Otherwise, read in all inputs and output back the corresponding format.
  
    # First add iteration line. 
    sys.stdout.write('%s\t%d\n' %('I', num_iter))
  
    for line in lines:
        sys.stdout.write(line)
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        data = (line.strip().split('\t')[1]).split('-')
        nodeID = data[0]
        rank = float(data[1])
        pre_rank = float(data[3])
        neighbors = data[4:]
        
        line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
        if neighbors:
            line += ',' + ','.join(neighbors)
        line += '\n'
        sys.stdout.write(line)
