#!/usr/bin/env python

import sys

# Used for key sorting. C > maximum number of nodes in input.
C = 999999.0

for line in sys.stdin:
    if line[0] == 'I':
        # Iteration line. Format: 0\tn so process_map.py gets iter_num first.
        n = line.strip().split('\t')[1]
        sys.stdout.write('%6.15f\t%s\n' %(0, n))
    
    else:
        data = line.strip().split('\t')       
        info = data[1].split(',')
        nodeID = data[0][7:]
        
        if info[0] == 'F':
            # Frozen page format: C-rank\tF,node_id,pagerank
            rank = float(info[1])
            sys.stdout.write('%6.15f\tF,nodeID,rank' %(C - rank, nodeID, rank))
        
        else:
            # Non-frozen page format: C-rank\tnodeId,info
            rank = float(info[0])
            sys.stdout.write('%6.15f\t%s,%s' %(C - rank, nodeID, data[1]))
