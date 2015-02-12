#!/usr/bin/env python

import sys

def handle_frozen(nodeID, cur_rank, prev_rank, deg, neighbors):
    """Checks of given page has converged. If so, freezes the given node and
    allocates fixed contributions to neighbors."""  
    
    if prev_rank != 0.0 and (abs(cur_rank - pre_rank)/pre_rank < .001):
        # Format: NodeID:node_id\tF,pagerank
        sys.stdout.write('NodeID:%s\tF,%6.15f\n' %(nodeID, cur_rank))
        
        # Allocate fixed contributions to neighbors.
        allocate_prob(True, nodeID, cur_rank, deg, neighbors)

        return True
    else:
        return False
    
def allocate_prob(frozen, nodeID, rank, deg, neighbors):
    if frozen:
        if deg > 0.0:
            prob_contribution = rank / deg        
            for j in neighbors:
                # Format: NodeID:node_id\tF,fixed_node_id,prob_contribution
                sys.stdout.write('NodeID:%s\tF,%s,%6.15f\n'
                                 %(j, nodeID, prob_contribution))
    else:
        if deg > 0.0:
                prob_contribution = rank / deg        
                for j in neighbors:
                    # Format: NodeID:node_id\tprob_contribution\n
                    sys.stdout.write('NodeID:%s\t%6.15f\n'
                                     %(j, prob_contribution))
        else:
            # Format: NodeID:node_id\tprob_contribution\n
            sys.stdout.write('NodeID:%s\t%6.15f\n' %(nodeID, rank))

for line in sys.stdin:
    """Reads lines from stdin and returns appropriate values.
    
    Returns (op, nodeID, cur_rank, prev_rank, neighbors, deg), where op = 0
    (False) if line was sent to stdout."""
    
    if line[0] == 'I':
        # Format: I\tn
        sys.stdout.write(line)
        continue
    else:
        data = line.strip().split('\t')
        nodeID = data[0][7:]      
        info = data[1].split(',')
        
        # Frozen page format: NodeID:node_id\tF,pagerank
        if info[0] == 'F':
            sys.stdout.write(line)
            continue
        
        # Else not frozen page.
        # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
        cur_rank = float(info[0])
        prev_rank = float(info[1])              
        
        if len(info) > 2 and info[2][0] == 'C':
            deg = info[3][4:]
            neighbors = info[4:]
        else:
            # Fixed contributions and degree are missing in first iteration.
            neighbors = info[2:]
            deg = len(neighbors)
            fixed_cont = 0.0
            
            # Format: NodeID:node_id\tcur_rank,prev_rank,C:c,Deg:d,neigbor1,...
            line = 'NodeID:%s\t%6.15f,%6.15f,C:%6.15f,Deg:%6.15f,%s' \
                   %(nodeID, cur_rank, prev_rank, fixed_cont, deg, ','.join(neighbors))
            
        if handle_frozen(nodeID, cur_rank, prev_rank, deg, neighbors):
            continue
            
        sys.stdout.write(line)
        allocate_prob(False, nodeID, cur_rank, deg, neighbors)
