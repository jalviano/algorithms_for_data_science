# num_nodes.py

# Computes the number of nodes in the graph


from mrjob.job import MRJob
from mrjob.job import MRStep


class NumNodesCounter(MRJob):

    def mapper(self, key, value):
        if '#' not in value and len(value.strip()) > 0:
            values = value.split()
            from_id = int(values[0])
            to_id = int(values[1])
            yield 'num nodes', from_id
            yield 'num nodes', to_id

    def reducer(self, key, value):
        yield key, len(set(value))

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    NumNodesCounter.run()
