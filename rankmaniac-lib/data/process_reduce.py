#!/usr/bin/env python

import sys

# Maximum number of iterations.
MAX_ITER = 50
# Number of top nodes to be computed.
NUM_SHOW = 20
# Number of nodes checked for convergence.
N = max(50, NUM_SHOW)

first_iter = True
stop = True

# Number of iterations.
num_iter = 1
# Number of nodes.
num_nodes = 0

# The lines for "FinalRank".
final_ranks = []
# The pre-rank of the previous node, for checking stopping criterion.
last_pre_rank = None
# The input lines (containing node info) for the next iteration.
lines = []
# count is the number of lines in final_ranks.
count = 0

# Read the iteration line. It is the first line since only it has key 0.
line = sys.stdin.readline()
if (line[0] == '0'):
   first_iter = False
   num_iter = int(line.strip().split('\t')[1])
   # Read the number of nodes line. It is the second line since only it has key 1,
   # and there are no lines with key between 0 and 1.
   next_line = sys.stdin.readline()
   num_nodes = int(next_line.strip().split('\t')[1])

# We first process the top N nodes.
for i in xrange(N): 
    # Use the line read above if it wasn't the iteration line.
    if not (first_iter and i == 0):
        line = sys.stdin.readline()
    if not line:
        break
    
    if (first_iter):
        num_nodes += 1

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
    for line in lines:
        sys.stdout.write(line)

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        if (first_iter):
            num_nodes += 1     

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

    sys.stdout.write('%s\t%d\n' %('C', num_nodes))
    sys.stdout.write('%s\t%d\n' %('I', num_iter + 1))
