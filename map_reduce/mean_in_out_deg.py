# mean_in_out_deg.py

# Computes the mean and median indegree and outdegree


import numpy as np

from mrjob.job import MRJob
from mrjob.job import MRStep


OUT = 'outdegree'
IN = 'indegree'


class InOutDegreeAnalyzer(MRJob):

    def mapper(self, key, value):
        if '#' not in value and len(value.strip()) > 0:
            values = value.split()
            from_id = int(values[0])
            to_id = int(values[1])
            yield from_id, OUT
            yield to_id, IN

    def reducer(self, key, value):
        value = list(value)
        outdeg = [1 for v in value if v == OUT]
        indeg = [1 for v in value if v == IN]
        yield key, (sum(outdeg), OUT)
        yield key, (sum(indeg), IN)

    def mapper2(self, key, value):
        yield value[1], value[0]

    def reducer2(self, key, value):
        value = list(value)
        yield 'mean ' + key, np.mean(value)
        yield 'median ' + key, np.median(value)

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer),
                MRStep(mapper=self.mapper2, reducer=self.reducer2)]


if __name__ == '__main__':
    InOutDegreeAnalyzer.run()
