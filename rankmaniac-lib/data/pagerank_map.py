#!/usr/bin/env python

import sys

def decode(line):
    """Reads line from stdin and returns appropriate values.
    
    Returns (op, nodeID, cur_rank, prev_rank, neighbors, deg), where op = 0
    (False) if line was sent to stdout."""
    
    # Save information for reduce and process steps.
    sys.stdout.write(line)
    
    if line[0] == 'I' or line[0] == 'C' or line[0] == 'F':
        # Format: I\tn or C\tm or F\tNodeId: PageRank
        return (0, None, None, None, None, None)
    else:
        # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
        data = line.strip().split('\t')
        nodeID = int(data[0][7:])       
        info = data[1].split(',')        
        cur_rank = float(info[0])
        prev_rank = float(info[1])
        
        if info[2][0:2] == 'C:':
            # Fixed contributions and degree are missing in first iteration.
            deg = int(info[3][4:])
            neighbors = info[4:]
        else:
            neighbors = info[3:]
            deg = len(neighbors)
        return (1, nodeId, cur_rank, prev_rank, neighbors, deg)
        
def encode(nodeId, prob_contribution):
    # Format: NodeID:node_id\tprob_contribution\n
    sys.stdout.write('NodeID:%s\t%s\n' %(nodeID, prob_contribution))

for line in sys.stdin:
    (op, nodeID, cur_rank, prev_rank, neighbors, deg) = decode(line)
    
    if op:
        if deg == 0:
            encode(nodeID, cur_rank)
        else:
            for j in neighbors:
                encode(j, cur_rank / deg)
