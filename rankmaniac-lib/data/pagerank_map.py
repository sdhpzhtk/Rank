#!/usr/bin/env python

import sys

for line in sys.stdin:
    # Only process lines of the form "NodeId:\t....".
    if line[0] == 'N':
        data = line.strip().split('\t')
        nodeID = data[0][len('NodeId:'):]

        data = data[1].split(',')
        cur_rank = data[0]
        neighbors = data[2:]
        deg = len(neighbors)

        # First transmit the node info, save cur_rank for next iteration.
        # Format: nodeID\tN-cur_rank-neigbor1-neighbor2-....
        sys.stdout.write('%s\tN-%s\n' %(nodeID, '-'.join([cur_rank] + neighbors)))
        
        if deg == 0:
            sys.stdout.write('%s\t%s\n' %(nodeID, cur_rank))
        else:
            cur_rank = float(cur_rank)
            for j in neighbors:
                sys.stdout.write('%s\t%6.15f\n' %(j, cur_rank/deg))
    elif line[0] == 'I':
       # Format: I\tn
       n = int(line.strip().split('\t')[1])
       sys.stdout.write('%s\t%d\n' %('I', n))
    elif line[0] == 'C':
       # Format: C\tm
       m = int(line.strip().split('\t')[1])
       sys.stdout.write('%s\t%d\n' %('C', m))

