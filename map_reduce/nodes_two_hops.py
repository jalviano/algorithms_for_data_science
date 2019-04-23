# nodes_two_hops.py

# Computes the mean and median number of nodes reachable in two hops


import numpy as np

from mrjob.job import MRJob
from mrjob.job import MRStep


class TwoHopNodesAnalyzer(MRJob):

    def mapper1(self, key, value):
        if '#' not in value and len(value.strip()) > 0:
            u, v = value.split()
            yield int(v), (int(u), int(v))
            yield int(u), (int(u), int(v))

    def reducer1(self, key, values):
        outg, inc = set(), set()
        for val in values:
            if val[0] == key:
                outg.add(val[1])
            elif val[1] == key:
                inc.add(val[0])
        all_edges = outg.union(inc)
        for edge in all_edges:
            if edge in list(inc):
                out_edges = [out_edge for out_edge in list(outg)]
                yield edge, out_edges
            else:
                yield edge, []

    def reducer2(self, key, values):
        values = [j for i in list(values) for j in i]
        yield 'nodes', len(set(values))

    def reducer3(self, key, values):
        nodes = list(values)
        yield 'mean nodes reachable in 2 hops', np.mean(nodes)
        yield 'median nodes reachable in 2 hops', np.median(nodes)

    def steps(self):
        return [MRStep(mapper=self.mapper1, reducer=self.reducer1),
                MRStep(reducer=self.reducer2),
                MRStep(reducer=self.reducer3)]


if __name__ == '__main__':
    TwoHopNodesAnalyzer.run()
