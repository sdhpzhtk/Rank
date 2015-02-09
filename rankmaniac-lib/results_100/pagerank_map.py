#!/usr/bin/env python

import sys

for line in sys.stdin:
    if line[0] == 'N':
        data = line.strip().split('\t')
        nodeID = data[0][7:]

        data = data[1].split(',')
        cur_rank = data[0]
        neighbors = data[2:]
        deg = len(neighbors)

        # First transmit the node info, save for next iteration
        sys.stdout.write('%s\tN%s\n' %(nodeID, '-'.join([cur_rank] + neighbors)))
        
        if deg == 0:
            sys.stdout.write('%s\t%s\n' %(nodeID, cur_rank))
        else:
            cur_rank = float(cur_rank)
            for j in data[2:]:
                sys.stdout.write('%s\t%6.15f\n' %(j, cur_rank/deg))
