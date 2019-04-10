# nodes_two_hops.py

# Computes the mean and median number of nodes reachable in two hops


from mrjob.job import MRJob
from mrjob.job import MRStep


class TwoHopNodesAnalyzer(MRJob):

    def mapper(self, key, value):
        if '#' not in value and len(value.strip()) > 0:
            yield

    def reducer(self, key, value):
        yield

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    TwoHopNodesAnalyzer.run()
