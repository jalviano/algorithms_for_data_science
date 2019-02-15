# count_min_sketch.py
#
# For this exercise we will use the following twitter data set:
# https://www.cs.duke.edu/courses/fall15/compsci590.4/assignment2/tweetstream.zip (2.1G). The meaning of the fields
# of a tweet can be found at https://dev.twitter.com/overview/api/tweets.


import binascii
import heapq
import json
import zipfile
import numpy as np


BREAK_POINT = 2000


class MinHeap(object):

    def __init__(self):
        self.heap = []
        self.item_finder = {}

    def __str__(self):
        string = []
        c = self.heap.copy()
        while c:
            string.append(heapq.heappop(c))
        return str(string)
        # return str(self.heap)

    def __len__(self):
        return len(self.heap)

    def __getitem__(self, index):
        return self.heap[index]

    def add_item(self, key, val):
        if val in self.item_finder:
            self.remove_item(val)
        item = [key, val]
        self.item_finder[val] = item
        heapq.heappush(self.heap, item)

    def remove_item(self, val):
        item = self.item_finder.pop(val)
        self.heap.remove(item)

    def extract_min(self):
        while self.heap:
            head = heapq.heappop(self.heap)
            del self.item_finder[head[1]]
            return head

    def get_min(self):
        return self.heap[0]


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
                        tag = ht['text']
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
                if stream_size >= BREAK_POINT: break
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
                        tag = ht['text']
                        if tag in items:
                            if tag in second_pass:
                                second_pass[tag] += 1
                            else:
                                second_pass[tag] = 1
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
                if stream_size >= BREAK_POINT: break
    for tag, freq in second_pass.items():
        if freq >= target_freq * stream_size:
            heavy_hitters.append(tag)
    return heavy_hitters


def count_min_sketch(target_freq, epsilon, delta):
    """
    Implement the Count-Min data structure along with min-heap such that any hashtag that occurs at least 0.002th
    fraction of times are returned, and any hashtag that is returned has frequency at least 0.001th fraction of the
    whole dataset size. You should have sufficient confidence on your answer.
    """
    heavy_hitters = []
    minheap = MinHeap()
    w = int(1 / epsilon)
    num_hash = int(np.ceil(np.log(1 / delta)))
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
                        tag = ht['text']
                        counts = []
                        # Get hashes for all functions in hash family
                        for i, h in enumerate(H):
                            j = h(tag)
                            sketch[i, j] += 1
                            counts.append(sketch[i, j])
                        # Get frequency as minimum count
                        freq = min(counts)
                        # Check if hashtag has frequency >= m / k
                        # TODO: Problem with min-heap ==> some items are out of order for larger streams, but still no
                        #  false negatives, which is good
                        if freq >= target_freq * stream_size:
                            # Add hashtag to min-heap or update existing key if hashtag already in heap
                            minheap.add_item(freq, tag)
                            # Remove all hashtags in min-heap with frequency < m / k
                            while minheap.get_min()[0] < target_freq * stream_size:
                                minheap.extract_min()
                        if stream_size % 10 == 0: print(minheap)  # TODO: Remove helper code
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
                if stream_size >= BREAK_POINT: break  # TODO: Remove helper code
    # TODO: Update return
    while minheap:
        heavy_hitters.append(minheap.extract_min())
    print(heavy_hitters)
    return heavy_hitters


def _get_hash_family(num_hash, m):
    """
    Let p be a prime.
    For any a, b ∈ Z_p = {0, 1, 2, ..., p−1}, define h_a,b : Z_p ⇒ Z_p by h_a,b(x) = ax + b mod p.
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
    results1 = naive_frequency(0.002, 500)
    print(len(results1), sorted(results1))
    results2 = [i[1] for i in count_min_sketch(0.002, 0.001, 0.001)]
    print(len(results2), sorted(results2))
    print(set(results1).issubset(set(results2)))
