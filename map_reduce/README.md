# MapReduce

We implemented MapReduce to compute the following for our Twitter dataset:

- Number of nodes in the graph
- Average (and median) indegree and outdegree
- Average (and median) number of nodes reachable in two hops
- Number of nodes with indegree > 100

We used the small test dataset `data/testdata.txt` to evaluate the accuracy of our implementations before running 
MapReduce on the full `data/email-EuAll.txt` dataset.

## Execution

To execute all MapReduce computations at once, run the script:

`./run.sh <dataFile>`

where `<dataFile>` is the path to the dataset file (`data/testdata.txt` for the test dataset and `data/email-EuAll.txt` 
for the Twitter dataset).

## Number of nodes

To compute the number of nodes in the graph run:

`python3 num_nodes.py <dataFile>`

Our implementation computed 265214 nodes in the graph for the Twitter dataset:

```
No configs found; falling back on auto-configuration
No configs specified for inline runner
Running step 1 of 1...
Creating temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes.Justin.20190421.202357.980903
job output is in /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes.Justin.20190421.202357.980903/output
Streaming final output from /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes.Justin.20190421.202357.980903/output...
"num nodes"	265214
Removing temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes.Justin.20190421.202357.980903...
```

## Indegree and outdegree

To compute the average and median indegree and outdegree, run:

`python3 mean_in_out_deg.py <dataFile>`

For the Twitter dataset, our MapReduce implementation computed mean and median outdegree of 1.58 and 1.0 respectively 
and mean and median indegree of 1.58 and 0.0 respectively:

```
No configs found; falling back on auto-configuration
No configs specified for inline runner
Running step 1 of 2...
Creating temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/mean_in_out_deg.Justin.20190421.202416.107121
Running step 2 of 2...
job output is in /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/mean_in_out_deg.Justin.20190421.202416.107121/output
Streaming final output from /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/mean_in_out_deg.Justin.20190421.202416.107121/output...
"mean outdegree"	1.5837964813320564
"median outdegree"	1.0
"mean indegree"	1.5837964813320564
"median indegree"	0.0
Removing temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/mean_in_out_deg.Justin.20190421.202416.107121...
```

## Number of nodes reachable in two hops

To compute the average and median number of nodes reachable in two hops, run:

`python3 nodes_two_hops.py <dataFile>`

Our implementation computed the mean and median number of nodes reachable in two hops to be 174.31 and 72.0 respectively 
for the Twitter dataset:

```
No configs found; falling back on auto-configuration
No configs specified for inline runner
Running step 1 of 3...
Creating temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/nodes_two_hops.Justin.20190423.124922.441571
Running step 2 of 3...
Running step 3 of 3...
job output is in /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/nodes_two_hops.Justin.20190423.124922.441571/output
Streaming final output from /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/nodes_two_hops.Justin.20190423.124922.441571/output...
"mean nodes reachable in 2 hops"	174.31289449274925
"median nodes reachable in 2 hops"	72.0
Removing temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/nodes_two_hops.Justin.20190423.124922.441571...
```

## Number of nodes with indegree > 100

Finally, to compute the number of nodes with indegree > 100, run:

`python3 num_nodes_indeg.py <dataFile>`

For the Twitter dataset, our MapReduce implementation computed 702 nodes with indegree > 100:

```
No configs found; falling back on auto-configuration
No configs specified for inline runner
Running step 1 of 2...
Creating temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes_indeg.Justin.20190421.202458.042427
Running step 2 of 2...
job output is in /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes_indeg.Justin.20190421.202458.042427/output
Streaming final output from /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes_indeg.Justin.20190421.202458.042427/output...
"num nodes with indegree > 100"	702
Removing temp directory /var/folders/tm/f789n6g972scxkkd0dsszf_c0000gn/T/num_nodes_indeg.Justin.20190421.202458.042427...
```
