# min_heap.py


import heapq


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
        if val in self.item_finder:
            self.remove_item(val)
        item = [key, val]
        self.item_finder[val] = item
        self._push(item)

    def remove_item(self, val):
        item = self.item_finder.pop(val)
        self.heap.remove(item)
        self._heapify()

    def extract_min(self):
        while self.heap:
            min_item = self._pop()
            del self.item_finder[min_item[1]]
            return min_item

    def get_min(self):
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

    def _replace(self, item):
        min_item = self.heap[0]
        self.heap[0] = item
        self._sift_up(0)
        return min_item

    def _push_pop(self, item):
        if self.heap and self.heap[0] < item:
            item, self.heap[0] = self.heap[0], item
            self._sift_up(0)
        return item

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
                i = parent
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


class MinHeap2(object):

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
