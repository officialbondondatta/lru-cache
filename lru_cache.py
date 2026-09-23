class _Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class Cache:
    def __init__(self, capacity):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be a positive integer")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._nodes = {}
        self._head = _Node()  # LRU sentinel
        self._tail = _Node()  # MRU sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _append(self, node):
        node.prev = self._tail.prev
        node.next = self._tail
        self._tail.prev.next = node
        self._tail.prev = node

    def _touch(self, node):
        self._unlink(node)
        self._append(node)

    def get(self, key):
        node = self._nodes.get(key)
        if node is None:
            return -1
        self._touch(node)
        return node.value

    def put(self, key, value):
        node = self._nodes.get(key)
        if node is not None:
            node.value = value
            self._touch(node)
            return
        node = _Node(key, value)
        self._nodes[key] = node
        self._append(node)
        if len(self._nodes) > self._capacity:
            oldest = self._head.next
            self._unlink(oldest)
            del self._nodes[oldest.key]

    def items_lru_to_mru(self):
        """Return a diagnostic snapshot in O(n) time and space."""
        items = []
        node = self._head.next
        while node is not self._tail:
            items.append((node.key, node.value))
            node = node.next
        return items
