#!/usr/bin/env python

import sys

DAMP = .85

def decode(line):
    """ """
    if line[0] == 'I' or line[0] == 'C' or line[0] == 'F':
        # Format: I\tn or C\tm or F\tNodeId: PageRank
        sys.stdout.write(line)
        return (0, None, None, None, None, None)    
    else:
        data = line.strip().split('\t')       
        info = data[1].split(',')
        
        if len(info) == 2:
            # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
            nodeID = int(data[0][7:])      
            cur_rank = float(info[0])
            prev_rank = float(info[1])
            
            if info[2][0:2] == 'C:':
                fixed_cont = float(info[2][2:])
                deg = int(info[3][4:])
                neighbors = info[4:]
            else:
                # Fixed contributions and degree are missing in first iteration.
                fixed_cont = 0.0
                neighbors = info[2:]
                deg = len(neighbors)

            return (1, nodeId, cur_rank, fixed_cont, deg, neighbors)            
        
        elif len(info) == 1:
            # Format: NodeID:node_id\tprob_contribution
            nodeID = int(data[0][len('NodeId:'):])
            prob_contribution = float(info)
            return (2, nodeId, prob_contribution, None, None, None)

def encode(nodeID, rank, prev_rank, fixed_cont, deg, neighbors):
    """Feed new PageRanks to processing. C - rank sorts by PageRank."""
    
    # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
    sys.stdout.write('NodeID:%s\t%6.15f,%6.15f,C:%6.15f,Deg:%6.15f,%s'
        %(nodeID, rank, prev_rank, fixed_cont, deg, ','.join(neighbors)))

cur_node = None
rank = 0.0
prev_rank = 0.0
deg = 0
neighbors = None
while True:
    line = sys.stdin.readline()
    if not line:
        break
    
    (op, nodeId, field1, field2, field3, field4) = decode(line)
    
    if op == 0:
        continue
    
    if cur_node is None:
        # First iteration.
        cur_node = nodeID

    elif cur_node != nodeID:
        # New block of pages.
        rank = rank * DAMP + 1 - DAMP
        encode(cur_node, rank, prev_rank, fixed_cont, deg, neighbors)
        
        # Reset parameters.
        rank = 0.0
        prev_rank = 0.0
        deg = 0
        neighbors = None
        
        cur_node = nodeID
    
    if op == 1:
        # Information line. Add fixed_contribution.
        prev_rank = field1
        fixed_cont = field2
        deg = field3
        neighbors = field4
        
        rank += fixed_cont
        
    elif op == 2:
        prob_contribution = field1
        rank += prob_contribution

# Process the last node.
rank = rank * DAMP + 1 - DAMP
encode(cur_node, rank, info)
