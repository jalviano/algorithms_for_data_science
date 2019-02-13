# count_min_sketch.py
#
# For this exercise we will use the following twitter data set:
# https://www.cs.duke.edu/courses/fall15/compsci590.4/assignment2/tweetstream.zip (2.1G). The meaning of the fields
# of a tweet can be found at https://dev.twitter.com/overview/api/tweets.


import json
import zipfile
import numpy as np


class Node:
    """
    http://interactivepython.org/courselib/static/pythonds/Trees/SearchTreeImplementation.html
    """

    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.val = val
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def has_left_child(self):
        return self.left_child

    def has_right_child(self):
        return self.right_child

    def is_left_child(self):
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        return self.parent and self.parent.right_child == self

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.right_child or self.left_child)

    def has_any_children(self):
        return self.right_child or self.left_child

    def has_both_children(self):
        return self.right_child and self.left_child

    def replace_node_data(self, key, value, lc, rc):
        self.key = key
        self.val = value
        self.left_child = lc
        self.right_child = rc
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self
    
    def splice_out(self):
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent

    def find_successor(self):
        succ = None
        if self.has_right_child():
            succ = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    succ = self.parent
                else:
                    self.parent.right_child = None
                    succ = self.parent.find_successor()
                    self.parent.right_child = self
        return succ

    def find_min(self):
        current = self
        while current.has_left_child():
            current = current.left_child
        return current

    def update_val(self, value):
        self.val = value


class BST(object):
    """
    http://interactivepython.org/courselib/static/pythonds/Trees/SearchTreeImplementation.html
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def __iter__(self):
        #         yield self
        #         for child in self.children:
        #             for node in child:
        #                 yield node
        return self

    def __next__(self):
        # level = [root]
        # nextLevel = []
        # queue = []
        # while not level:
        #     queue.extend(level)
        #     for l in level:
        #         nextLevel.append(l.left if l.left != None)
        #         nextLevel.append(l.right if l.right != None)
        #     level = nextLevel
        #     nextLevel = []
        pass

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = Node(key, val)
        self.size = self.size + 1

    def _put(self, key, val, current_node):
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, val, current_node.left_child)
            else:
                current_node.left_child = Node(key, val, parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, val, current_node.right_child)
            else:
                current_node.right_child = Node(key, val, parent=current_node)

    def __setitem__(self, k, v):
        self.put(k, v)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.val
            else:
                return None
        else:
            return None

    def _get(self, key, current_node):
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left_child)
        else:
            return self._get(key, current_node.right_child)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove:
                self.remove(node_to_remove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    def increment(self, key):
        if self.root:
            node = self._get(key, self.root)
            if node:
                node.val += 1

    def decrement(self, key):
        if self.root:
            node = self._get(key, self.root)
            if node:
                node.val -= 1
                if node.val == 0:
                    self.delete(node.key)

    def decrement_all(self):
        pass

    @staticmethod
    def remove(current_node):
        if current_node.is_leaf():
            if current_node == current_node.parent.left_child:
                current_node.parent.left_child = None
            else:
                current_node.parent.right_child = None
        elif current_node.has_both_children():
            succ = current_node.find_successor()
            succ.splice_out()
            current_node.key = succ.key
            current_node.val = succ.val
        else:
            if current_node.has_left_child():
                if current_node.is_left_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.left_child
                elif current_node.is_right_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.left_child
                else:
                    current_node.replace_node_data(current_node.left_child.key, current_node.left_child.val,
                                                   current_node.left_child.left_child,
                                                   current_node.left_child.right_child)
            else:
                if current_node.is_left_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.right_child
                elif current_node.is_right_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.right_child
                else:
                    current_node.replace_node_data(current_node.right_child.key, current_node.right_child.val,
                                                   current_node.right_child.left_child,
                                                   current_node.right_child.right_child)


def _naive_frequency(k, epsilon):
    """
    Maintain a list of items being counted. Initially the list is empty. For each item, if it is the same as some item
    on the list, increment its counter by one. If it differs from all the items on the list, then if there are less than
    k items on the list, add the item to the list with its counter set to one. If there are already k items on the list
    decrement each of the current counters by one. Delete an element from the list if its count becomes zero.

    Implement for k = 500, and return all the hashtags that occur at least 0.002th fraction of times in the dataset.
    It is ok to return the first 15 characters of the hashtag.
    """
    items = BST()
    n_hashtags = 0
    with zipfile.ZipFile('tweetstream.zip') as zf:
        with zf.open('tweetstream.txt') as f:
            counter = 0
            for line in f:
                try:
                    stream = json.loads(line)
                    hashtags = stream['entities']['hashtags']
                    for ht in hashtags:
                        tag = ht['text']
                        n_hashtags += 1
                        if tag in items:
                            # increment its counter by one
                            items.increment(tag)
                        elif len(items) < k:
                            items.put(tag, 1)
                        else:
                            # decrement each of the current counters by one
                            pass
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
                counter += 1
                if counter > int(k * 100):
                    break
    for item in items:
        print(item)
    return items


def naive_frequency(k, epsilon):
    """
    Maintain a list of items being counted. Initially the list is empty. For each item, if it is the same as some item
    on the list, increment its counter by one. If it differs from all the items on the list, then if there are less than
    k items on the list, add the item to the list with its counter set to one. If there are already k items on the list
    decrement each of the current counters by one. Delete an element from the list if its count becomes zero.

    Implement for k = 500, and return all the hashtags that occur at least 0.002th fraction of times in the dataset.
    It is ok to return the first 15 characters of the hashtag.
    """
    results = []
    items = {}
    n_hashtags = 0
    with zipfile.ZipFile('tweetstream.zip') as zf:
        with zf.open('tweetstream.txt') as f:
            for line in f:
                try:
                    stream = json.loads(line)
                    hashtags = stream['entities']['hashtags']
                    for ht in hashtags:
                        tag = ht['text']
                        n_hashtags += 1
                        if tag in items:
                            items[tag] += 1
                        elif len(items) < k:
                            items[tag] = 1
                        else:
                            for key in list(items.keys()):
                                items[key] -= 1
                                if items[key] <= 0:
                                    del items[key]
                except (json.decoder.JSONDecodeError, KeyError):
                    pass
    for tag, freq in items.items():
        if freq / n_hashtags >= epsilon:
            results.append(tag)
    return results  # ['Job', 'Jobs', 'TweetMyJobs', 'meteoAlarm', 'Viña2013']


def count_min_sketch():
    """
    Implement the Count-Min data structure along with min-heap such that any hashtag that occurs at least 0.002th
    fraction of times are returned, and any hashtag that is returned has frequency at least 0.001th fraction of the
    whole dataset size. You should have sufficient confidence on your answer.
    """
    return


if __name__ == '__main__':
    results = naive_frequency(500, 0.002)
    print(results)