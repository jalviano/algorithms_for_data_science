# count_min_sketch.py
#
# For this exercise we will use the following twitter data set:
# https://www.cs.duke.edu/courses/fall15/compsci590.4/assignment2/tweetstream.zip (2.1G). The meaning of the fields
# of a tweet can be found at https://dev.twitter.com/overview/api/tweets.


import argparse
import binascii
import json
import zipfile
import numpy as np


BREAK_POINT = np.inf


class MinHeap(object):

    def __init__(self, heap=None):
        if heap is not None:
            self.heap = heap
            self._heapify()
        else:
            self.heap = []
        self.item_finder = {}

    def __str__(self):
        return str(self.heap)

    def __len__(self):
        return len(self.heap)

    def __getitem__(self, index):
        return self.heap[index]

    def add_item(self, key, val):
        # Delete item if already in heap
        if val in self.item_finder:
            self._remove(val)
        # Insert item into heap
        item = [key, val]
        self.item_finder[val] = item
        self._push(item)

    def extract_min(self):
        # Pop minimum item in heap
        while self.heap:
            min_item = self._pop()
            del self.item_finder[min_item[1]]
            return min_item

    def get_min(self):
        # Return minimum item in heap
        return self.heap[0]

    def _push(self, item):
        self.heap.append(item)
        self._sift_down(len(self.heap) - 1, 0)

    def _pop(self):
        last = self.heap.pop()
        if self.heap:
            min_item = self.heap[0]
            self.heap[0] = last
            self._sift_up(0)
            return min_item
        return last

    def _remove(self, val):
        item = self.item_finder.pop(val)
        i = self.heap.index(item)
        self.heap[i] = self.heap[-1]
        self.heap.pop()
        if i < len(self.heap):
            self._sift_up(i)
            self._sift_down(i, 0)

    def _heapify(self):
        n = len(self.heap)
        for i in reversed(range(n // 2)):
            self._sift_up(i)

    def _sift_down(self, i, start_i):
        item = self.heap[i]
        while i > start_i:
            parent_i = (i - 1) >> 1
            parent = self.heap[parent_i]
            if item < parent:
                self.heap[i] = parent
                i = parent_i
            else:
                break
        self.heap[i] = item

    def _sift_up(self, i):
        item = self.heap[i]
        start_i = i
        end_i = len(self.heap)
        child_i = 2 * i + 1
        while child_i < end_i:
            right_i = child_i + 1
            if right_i < end_i and not self.heap[child_i] < self.heap[right_i]:
                child_i = right_i
            self.heap[i] = self.heap[child_i]
            i = child_i
            child_i = 2 * i + 1
        self.heap[i] = item
        self._sift_down(i, start_i)


def naive_frequency(target_freq, k):
    """
    Maintain a list of items being counted. Initially the list is empty. For each item, if it is the same as some item
    on the list, increment its counter by one. If it differs from all the items on the list, then if there are less than
    k items on the list, add the item to the list with its counter set to one. If there are already k items on the list
    decrement each of the current counters by one. Delete an element from the list if its count becomes zero.

    Implement for k = 500, and return all the hashtags that occur at least 0.002th fraction of times in the dataset.
    It is ok to return the first 15 characters of the hashtag.
    """
    heavy_hitters = []
    items = {}
    stream_size = 0
    # Open JSON tweet data file
    with zipfile.ZipFile('tweetstream.zip') as zf:
        with zf.open('tweetstream.txt') as f:
            # Read file one line at a time
            for line in f:
                try:
                    stream = json.loads(line)
                    # Get hashtags for tweet
                    hashtags = stream['entities']['hashtags']
                    for ht in hashtags:
                        # Update estimated stream size
                        stream_size += 1
                        tag = ht['text'].lower()
                        # Check if hashtag is already in the list
                        if tag in items:
                            # Hashtag is in list: increment counter by one
                            items[tag] += 1
                        elif len(items) < k:
                            # Hashtag is not in list and there are few than k items: add hashtag to list
                            items[tag] = 1
                        else:
                            # Hashtag is not in list and there are at least k items: decrement all item counters in list
                            # and remove if counter becomes zero
                            for key in list(items.keys()):
                                items[key] -= 1
                                if items[key] <= 0:
                                    del items[key]
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
    # Get all items with frequency >= m / k
    second_pass = {}
    stream_size = 0
    with zipfile.ZipFile('tweetstream.zip') as zf:
        with zf.open('tweetstream.txt') as f:
            # Read file one line at a time
            for line in f:
                try:
                    stream = json.loads(line)
                    # Get hashtags for tweet
                    hashtags = stream['entities']['hashtags']
                    for ht in hashtags:
                        stream_size += 1
                        tag = ht['text'].lower()
                        if tag in items:
                            if tag in second_pass:
                                second_pass[tag] += 1
                            else:
                                second_pass[tag] = 1
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
    for tag, freq in second_pass.items():
        if freq >= target_freq * stream_size:
            heavy_hitters.append(tag)
    return heavy_hitters


def count_min_sketch(target_freq, epsilon):
    """
    Implement the Count-Min data structure along with min-heap such that any hashtag that occurs at least 0.002th
    fraction of times are returned, and any hashtag that is returned has frequency at least 0.001th fraction of the
    whole dataset size. You should have sufficient confidence on your answer.
    """
    heavy_hitters = MinHeap()
    w = int(np.e / epsilon)
    num_hash = int(np.ceil(np.log(1 / target_freq)))
    print(num_hash)
    sketch = np.zeros((num_hash, w))
    H = _get_hash_family(num_hash, w)
    stream_size = 0
    # Open JSON tweet data file
    with zipfile.ZipFile('tweetstream.zip') as zf:
        with zf.open('tweetstream.txt') as f:
            # Read file one line at a time
            for line in f:
                try:
                    stream = json.loads(line)
                    # Get hashtags for tweet
                    hashtags = stream['entities']['hashtags']
                    for ht in hashtags:
                        # Update estimated stream size
                        stream_size += 1
                        tag = ht['text'].lower()
                        counts = []
                        # Get hashes for all functions in hash family
                        for i, h in enumerate(H):
                            j = h(tag)
                            sketch[i, j] += 1
                            counts.append(sketch[i, j])
                        # Get frequency as minimum count
                        freq = min(counts)
                        # Check if hashtag has frequency >= m / k
                        if freq >= target_freq * stream_size:
                            # Add hashtag to min-heap or update existing key if hashtag already in heap
                            heavy_hitters.add_item(freq, tag)
                            # Remove all hashtags in min-heap with frequency < m / k
                            while heavy_hitters.get_min()[0] < target_freq * stream_size:
                                heavy_hitters.extract_min()
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
    return heavy_hitters


def _get_hash_family(num_hash, m):
    """
    Let p be a prime.
    For any a, b ∈ Z_p = {0, 1, 2, ..., p−1}, define h_a,b : Z_p ⇒ Z_p by h_a,b(x) = ((ax + b) mod p) mod m.
    The resulting collection of functions H = {h_a,b|a, b ∈ Z_p} is a pairwise independent hash family.
    """
    # Set random number generator seed for consistency
    np.random.seed(1)
    H = []
    # Generate hash family
    for _ in range(num_hash):
        _p = _get_prime()
        _a = np.random.randint(1, _p)
        _b = np.random.randint(0, _p)

        def h(x, a=_a, b=_b, p=_p):
            # Convert string to integer representation
            x = int(binascii.hexlify(x.encode('utf8')), 16)
            return int(((a * x + b) % p) % m)

        H.append(h)
    return H


def _get_prime():
    while True:
        prime = np.random.random_integers(2 ** 32, 2 ** 34)
        if all(prime % i != 0 for i in range(3, int((prime ** 0.5) + 1), 2)):
            return prime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    # Required arguments
    parser.add_argument('-A', '--algorithm', nargs=1, required=True, type=str,
                        help='Frequency algorithm to solve heavy hitters problem')
    # Parse and gather arguments
    args = parser.parse_args()
    # Initialize variables
    arg_algorithm = args.algorithm[0]
    # Solve heavy hitters problem
    if arg_algorithm == 'a':
        # Use simple frequency algorithm
        results = naive_frequency(0.002, 500)
        print('Simple frequency algorithm heavy hitters:')
        print(results)
    else:
        # Use count-min sketch algorithm
        results = [i[1] for i in count_min_sketch(0.002, 0.001)]
        print('Count-min sketch algorithm heavy hitters:')
        print(results)
