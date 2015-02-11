#!/usr/bin/env python

import sys

DAMP = .85
# Used for key sorting. C > maximum number of nodes in input.
C = 999999.0

def decode(line):
    """ """
    if line[0] == 'I':
        # Iteration line. Format: 0\tn so process_map.py gets iter_num first.
        n = int(line.strip().split('\t')[1])
        sys.stdout.write('%6.15f\t%s\n' %(0, n))
        return (0, None, None, None)
        
    elif line[0] == 'C':
        # Counter line. Format: 1\tm so process_map.py gets num_nodes second.
        m = int(line.strip().split('\t')[1])
        sys.stdout.write('%6.15f\t%s\n' %(1, m))
        return (0, None, None, None)
    
    elif line[0] == 'F':
        # Pass frozen nodes for processing in process_reduce.py.
        sys.stdout.write(line)
        return (0, None, None, None)
    
    else:
        data = line.strip().split('\t')       
        info = data[1].split(',')
        
        if len(info) == 2:
            # Format: NodeID:node_id\tcur_rank,prev_rank,C,neigbor1,neighbor2....
            nodeID = int(data[0][len('NodeId:'):])
            fixed_cont = float(info[2])
            neighbors = info[3:]
            deg = len(neighbors)
            return (1, nodeId, fixed_cont, info)            
        
        elif len(info) == 1:
            # Format: NodeID:node_id!\tprob_contribution
            nodeID = int(data[0][len('NodeId:'):])
            prob_contribution = float(info)
            return (2, nodeId, prob_contribution, None)

def encode(nodeID, rank, info):
    """Feed new PageRanks to processing. C - rank sorts by PageRank."""
    sys.stdout.write('%6.15f\t%s-%6.15f-%s\n' %(C - rank, nodeID, rank, info))
     
info = None    
rank = 0.0
cur_node = None
while True:
    line = sys.stdin.readline()
    if not line:
        break
    
    (op, nodeId, field1, field2, field3) = decode(line)
    
    if op == 0:
        continue
    
    if cur_node is None:
        # First iteration.
        cur_node = nodeID

    elif cur_node != nodeID:
        # New block of pages.
        rank = rank * DAMP + 1 - DAMP
        # info is None for deleted/frozen nodes.
        if info:
            encode(cur_node, rank, info)
        rank = 0.0
        cur_node = nodeID
        info = None
    
    if op == 1:
        # Information line. Add fixed_contribution.
        fixed_cont = field1
        info = field2
        rank += fixed_cont
        
    elif op == 2:
        prob_contribution = field1
        rank += prob_contribution

# Process the last node.
rank = rank * DAMP + 1 - DAMP
if info:
    encode(cur_node, rank, info)
