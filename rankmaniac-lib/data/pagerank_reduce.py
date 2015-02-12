#!/usr/bin/env python

import sys

DAMP = .85

def decode(line):
    """ """
    if line[0] == 'I':
        # Format: I\tn
        sys.stdout.write(line)
        return (0, None, None, None, None, None)    
    else:
        data = line.strip().split('\t')  
        info = data[1].split(',')
        nodeID = data[0][7:]
        
        if len(info) == 2:
            # Frozen page format: NodeID:node_id\tF,pagerank
            # Op = 0
            sys.stdout.write(line)
            return (0, nodeID, None, None, None, None)
            
        elif len(info) == 1:
            # Format: NodeID:node_id\tprob_contribution
            # Op = 1
            prob_contribution = float(info[0])
            return (1, nodeID, prob_contribution, None, None, None)
        
        elif len(info) == 3:
            # Format: NodeID:node_id\tF,fixed_node_id,fixed_contribution
            # Op = 2
            fixed_node_id = info[1]
            fixed_cont = float(info[2])
            return (2, nodeID, fixed_node_id, fixed_cont, None, None)
        
        else:
            # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
            # Op = 3
            cur_rank = float(info[0])
            prev_rank = float(info[1])
            fixed_cont = float(info[2][2:])
            deg = int(float(info[3][4:]))
            neighbors = info[4:]
            return (3, nodeID, cur_rank, fixed_cont, deg, neighbors)

def encode(nodeID, rank, prev_rank, fixed_cont, deg, neighbors):
    """Feed new PageRanks to processing."""
    
    # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
    sys.stdout.write('NodeID:%s\t%6.15f,%6.15f,C:%6.15f,Deg:%6.15f,%s'
        %(nodeID, rank, prev_rank, fixed_cont, deg, ','.join(neighbors)))

cur_node = None
rank = 0.0
prev_rank = 0.0
fixed_cont = 0.0
deg = 0
neighbors = None
frozen_neighbors = []   
for line in sys.stdin:    
    (op, nodeID, field1, field2, field3, field4) = decode(line)
    
    if op == 0:
        continue
    
    if cur_node is None:
        # First iteration.
        cur_node = nodeID

    elif cur_node != nodeID:
        if neighbors is not None:
            # New block of pages and previous block was not for frozen page.
            rank += fixed_cont
            rank = rank * DAMP + 1 - DAMP
            # Remove frozen pages from adjacency list.
            neighbors = list(set(neighbors).difference(set(frozen_neighbors)))
            encode(cur_node, rank, prev_rank, fixed_cont, deg, neighbors)
        
        # Reset parameters.
        rank = 0.0
        prev_rank = 0.0
        fixed_cont = 0.0
        deg = 0
        neighbors = None
        frozen_neighbors = []
        cur_node = nodeID
        
    if op == 1:
        # Format: NodeID:node_id\tprob_contribution
        prob_contribution = field1
        rank += prob_contribution        
        
    elif op == 2:
        fixed_node_id = field1
        cont_from_fixed_node = field2
        
        frozen_neighbors.append(fixed_node_id)
        fixed_cont += cont_from_fixed_node
    
    elif op == 3:
        # Information line.*
        prev_rank = field1
        original_cont_from_fixed_nodes = field2
        fixed_cont += original_cont_from_fixed_nodes
        deg = field3
        neighbors = field4

# Process last node.
rank += fixed_cont
rank = rank * DAMP + 1 - DAMP
# Remove frozen pages from adjacency list.
neighbors = list(set(neighbors).difference(set(frozen_neighbors)))
encode(cur_node, rank, prev_rank, fixed_cont, deg, neighbors)
