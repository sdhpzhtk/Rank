#!/usr/bin/env python

import sys

# Maximum number of iterations.
MAX_ITER = 50
# Number of top nodes to be computed.
NUM_SHOW = 20
# Number of nodes checked for convergence.
N = 25


def is_frozen(line):
   """Returns true if the given page is frozen."""
   data = line.strip().split('\t')
   
   if data[1][0] == 'F':
      return True
   else:
      return False
   
def encode(finished, line):
    """Print out final results or feed to next iteration."""
    data = line.strip().split('\t')
    info = data[1].split(',')
    fixed = is_frozen(line)
    
    if fixed:
        nodeID = info[1]
        rank = float(info[2])
    else:
        nodeID = info[0]
        rank = float(info[1])

    if finished:
        sys.stdout.write('FinalRank:%s\t%6.15f\n' %(rank, nodeID))
    else:
        if fixed:
            sys.stdout.write('NodeID:%s\tF,%6.15f\n' %(nodeID, rank))
        else:
            sys.stdout.write('NodeID:%s\t%s' %(nodeID, ','.join(info[1:]))            

first_iter = True

# Number of iterations.
num_iter = 1

# Read the iteration line. It is the first line since only it has key 0.
line = sys.stdin.readline()
if (line[0] == '0'):
   first_iter = False
   num_iter = int(line.strip().split('\t')[1])

top_N = []
top_N_all_fixed = True
num_fixed_pages = 0

# We first process the top N nodes.
for i in xrange(N):
    # Use the line read above if it wasn't the iteration line.
    if not (first_iter and i == 0):
        line = sys.stdin.readline()
    if not line:
        break

    top_N.append(line)
    if is_frozen(line):
        num_fixed_pages += 1
    else:
        top_N_all_fixed = False
        break

if num_fixed_pages == N or num_iter == MAX_ITER:
    # Print top 20 results and consume all inputs.
   
    num_printed = 0
    for line in top_N:
        # First print up to NUM_SHOW pages from top_N.
        encode(True, line)
        num_printed += 1
        
        if num_printed == NUM_SHOW:
           break
        
    for i in range(num_printed, NUM_SHOW):
        # Print exactly NUM_SHOW results.
        line = sys.stdin.readline()
        encode(True, line)

    for line in sys.stdin:
        # Exhaust remaining lines.
        continue
else:
    for line in top_N:
         encode(False, line)
        
    for line in sys.stdin:
        # Exhaust remaining lines.         
        fixed = is_frozen(line)
        
        if fixed and num_fixed_pages < N:
            encode(False, line)
            num_fixed_pages += 1
        elif not fixed:
            encode(False, line)

    sys.stdout.write('%s\t%d\n' %('I', num_iter + 1))
