#!/usr/bin/env bash

DATAFILE=$1

echo "================================================================================"
echo "Computing number of nodes in the graph..."
echo "================================================================================"
python3 num_nodes.py ${DATAFILE}

echo "================================================================================"
echo "Computing average (and median) indegree and outdegree..."
echo "================================================================================"
python3 mean_in_out_deg.py ${DATAFILE}

echo "================================================================================"
echo "Computing average (and median) number of nodes reachable in two hops..."
echo "================================================================================"
python3 nodes_two_hops.py ${DATAFILE}

echo "================================================================================"
echo "Computing number of nodes with indegree > 100..."
echo "================================================================================"
python3 num_nodes_indeg.py ${DATAFILE}
