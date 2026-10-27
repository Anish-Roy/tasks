# LRU Cache Implementation

Both `get` and `put` operation should have an average time complexity of $O(1)$. The cache lookup is done using a HashMap (Python `dict`) and the order of the elements in the cache is maintained using a Double Linked List.

Each cache element is stored as a `Node` class having 4 attributes:
- key - used for the HashMap lookup. The class stores it so that when an element is removed from the cache, the hashmap can refer to the key of that element and delete its record from the hashmap itself
- value - content of the cached element
- prev - pointer to the previous element in the linked list
- next - pointer to the next element in the linked list

The nodes (`Node` class) are the components of the class `DoubleLinkedList`. The linked list has 2 dummy elements - head and tail, and all other cache elements are stored in between them. The constructor builds a simple linked list: head<-->tail
The class has 4 functions:
- `add_node` - adds a node to the start of the linked list (after head)
- `remove_node` - removes a node in the middle of the linked list. Previous and next of the removed node point to each other
- `remove_last_node` - removes the last element in the list. The second last element now points to tail
- `move_node` - removes a node from its current position and places it at the front (recently used cache element)
All the above functions simply changes the pointers in the nodes, so each have a time complexity of $O(1)$

Finally, the `LRUCache` class defines the `get` and `put` functions. Its constructor builds the HashMap, the double linked list and the cache limit (number of maximum elements the cache can hold at a time)
`get` does a simple dictionary lookup and a $O(1)$ pointer operation, so it has time complexity of $O(1)$.
Similarly `put` does only an additional value comparison, so has time complexity of $O(1)$

Each `get` or `put` only uses a few local variables, and `put` creates at most one new node. So all have average space complexity of $O(1)$.

I have also included a interactive browser visualizer (built by *Claude*) to test the LRU Cache code.

_Why are a combination of a hash map and a doubly linked list often used for an LRU cache?_

We need a fast key-based lookup for cache read and updates, which can be done using a HashMap. To track the recency of usage, we need to maintain an order within the elements. An array will have average $O(n)$ time complexity for changing position of element from middle to front. This can be achieved in $O(1)$ using a double linked list.

_What changes would be required to make the LRU Cache thread-safe?_

Both the functions `get` and `put` should be implemented within a single thread lock, so only one thread runs either method at a time. This keeps the elements in the HashMap and the linked list in sync.

---

# Event Scheduler

*can_attend_all(events): Returns True if a person can attend all events without overlaps, False otherwise.*

A person can only attend all the events if no 2 events overlap. So, we sort all the events by their start time and start checking all adjacent events in the list. If any two adjacents event i and i-1 have start[i] < end[i-1], then there is a overlap and the person cannot attend all the events.

```python
def can_attend_all(events: list[tuple[int, int]]) -> bool:
    events.sort(key=lambda x: x[0])

    for i in range(1, len(events)):
        if events[i][0] < events[i - 1][1]:
            return False
    return True
```

Time Complexity: sorting the list takes O(n log n) and the for loop takes O(n) => total: O(n log n)
Space Complexity: in-place sorting give O(1)

*min_rooms_required(events): Returns the minimum number of meeting rooms required to schedule all events simultaneously.*

The minimum number of rooms needed will be the maximum number of meetings that overlap at any given time. For all other cases, we will have less concurrent meetings than number of rooms available. To do this we first sort the event list according to the start time of the events. Then use a min-heap to store the end times of the meetings that are currently in progress. The root of the heap is the time a room becomes free.
When a new meeting (let's say event A) arrives, we check its start time against the heap's minimum (let's say event B). If event B ends before event A, it's room can be reused else a new room needs to be allocated. For both cases, we push event A's end time, and for the former case pop event B's end time. The size of the heap thus tracks the number of rooms in use, giving us the maximum number of rooms needed.

```python
import heapq

def minMeetingRooms(events: list[tuple[int, int]]) -> int:
    events.sort(key=lambda x: x[0])

    heap = [events[0][1]]

    for i in range(1, len(events)):
        if events[i][0] >= heap[0]:
            heapq.heappop(heap)
            heapq.heappush(heap, events[i][1])

    return len(heap)
```

Time Complexity: Sorting the list takes O(n log n) and heap push/pop is also O(n log n) => total: O(n log n)
Space Complexity: worst case - heap holds all end times => total: O(n)

_How would you modify your scheduler to assign specific room numbers (e.g.,"Room A", "Room B") to each event?_

We modify the heap to not just store end times of the events, but also the rooms of the event. So each node stores something like - (end_time, room_id). When a room is popped from the heap (reusing the room), we assign that very room_id to the new event that is being pushed into the heap in the current step.
