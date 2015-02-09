#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

NUM_SHOW = 20
N = max(50, NUM_SHOW)

sum = 0.0

final_ranks = []
last_pre_rank = None
lines = []
stop = True
cnt = 0

for i in xrange(N):
    line = sys.stdin.readline()
    if not line:
        break
    data = (line.strip().split('\t')[1]).split('-')
    nodeID = data[0]
    rank = float(data[1])
    sum += rank
    pre_rank = float(data[2][1:])
    links = data[3:]

    line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
    if links:
        line += ',' + ','.join(links)
    line += '\n'
    lines.append(line)

    if last_pre_rank is not None and (abs(rank - pre_rank) > .005 or last_pre_rank < pre_rank):
        stop = False
        break
    last_pre_rank = pre_rank

    if cnt < NUM_SHOW:
        cnt += 1
        final_ranks.append('FinalRank:%f\t%s\n' %(rank, nodeID))

if stop:
    for line in final_ranks[:NUM_SHOW]:
        sys.stdout.write(line)
else:
    for line in lines:
        sys.stdout.write(line)
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        data = (line.strip().split('\t')[1]).split('-')
        nodeID = data[0]
        rank = float(data[1])
        sum += rank
        pre_rank = float(data[2][1:])
        links = data[3:]
        
        line = 'NodeID:%s\t%6.15f,%6.15f' %(nodeID, rank, pre_rank)
        if links:
            line += ',' + ','.join(links)
        line += '\n'
        sys.stdout.write(line)




