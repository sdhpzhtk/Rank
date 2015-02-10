#!/usr/bin/env python

import sys

#############################################

# Feed forward first two lines specifying number of iterations and nodes.
sys.stdout.write(sys.stdin.readline())
sys.stdout.write(sys.stdin.readline())

# Process node information and freeze converged nodes.
for line in sys.stdin:
    # data format: nodeId-rank-N-prerank-neighbor1-neighbor2-...
    data = (line.strip().split('\t')[1]).split('-')
    nodeID = data[0]
    rank = float(data[1])
    # Skip data[2] which is 'N'.
    pre_rank = float(data[3])
    neighbors = data[4:]    

    # Freeze converged nodes. Process_reduce.py will bundle up contributions of
    # frozen node to its neighbors.
    if (abs(rank - pre_rank)/pre_rank < .001):
        # Capital 'C' indicates node has converged.
        output_line = 'NodeID:%s\tC%t%6.15f' %(nodeID, rank)
        if neighbors:
            for page in neighbors:
                # Start with 2 to feed before into process_reduce.py before
                # unconverged pages.
                sys.stdout.write('2\t%s\t%6.15f'
                                 %(page, rank / len(neighbors)));
    
    # Continue iterating on pages that have not converged.
    else:
        output_line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
        if neighbors:
            output_line += ',' + ','.join(neighbors)
        output_line += '\n'
        
    sys.stdout.write(output_line)

#############################################
