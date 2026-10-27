class Node:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self) -> None:
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_node(self, node: Node):
        head = self.head
        node.next = head.next
        node.prev = head
        head.next.prev = node
        head.next = node

    def remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def remove_last_node(self) -> Node:
        last_node = self.tail.prev
        self.remove_node(last_node)
        return last_node

    def move_node(self, node: Node):
        self.remove_node(node)
        self.add_node(node)


class LRUCache:
    def __init__(self, limit: int):
        self.limit = limit
        self.cache = {}
        self.list = DoubleLinkedList()

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.list.move_node(node)
        return node.value

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.list.move_node(node)
        else:
            if len(self.cache) == self.limit:
                node = self.list.remove_last_node()
                del self.cache[node.key]
            node = Node(key, value)
            self.list.add_node(node)
            self.cache[key] = node
