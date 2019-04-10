# nodes_two_hops.py

# Computes the mean and median number of nodes reachable in two hops


from mrjob.job import MRJob
from mrjob.job import MRStep


class MST(MRJob):

    def mapper(self, key, value):
        if '#' not in value and len(value.strip()) > 0:
            values = value.split()
            from_id = int(values[0])
            to_id = int(values[1])
            yield 'num_nodes', from_id
            yield 'num_nodes', to_id

    def reducer(self, key, value):
        yield key, len(set(value))

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    MST.run()
