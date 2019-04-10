# num_nodes_indeg.py

# Computes the number of nodes with indegree > 100


from mrjob.job import MRJob
from mrjob.job import MRStep


T = 100


class NumIndegreeNodesCounter(MRJob):

    def mapper(self, key, value):
        if '#' not in value and len(value.strip()) > 0:
            values = value.split()
            to_id = int(values[1])
            yield to_id, 1

    def reducer(self, key, value):
        yield key, sum(value)

    def mapper2(self, key, value):
        if value > T:
            yield 'num nodes with indegree > {}'.format(T), value

    def reducer2(self, key, value):
        yield key, len(list(value))

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer),
                MRStep(mapper=self.mapper2, reducer=self.reducer2)]


if __name__ == '__main__':
    NumIndegreeNodesCounter.run()
