import heapq

class Directions:
    NORTH = 'NORTH'
    SOUTH = 'SOUTH'
    EAST = 'EAST'
    WEST = 'WEST'
    STOP = 'STOP'

class Actions:
    DIRECTIONS = {Directions.NORTH : (-1, 0),
                  Directions.SOUTH : (1, 0),
                  Directions.EAST : (0, 1),
                  Directions.WEST : (0, -1)}

    # -1 pull, 1 push
    ACTIONS = {'PUSH_' + key: value + (1,) for key, value in DIRECTIONS.items()}
    ACTIONS.update({'PULL_' + key: value + (-1,) for key, value in DIRECTIONS.items()})

class Levels:
    LETTERS = 'ABCDEFGHIJKLMN'
    SIZES = {'ABCDEFGHIJKLMN'[i]: i + 1 for i in range(len('ABCDEFGHIJKLMN'))}
    SIZES.update({k.lower(): -v for k, v in SIZES.items()})
    SYMBOLS = {v: k for k, v in SIZES.items()}

    @staticmethod
    def from_string(size):
        return Levels.SIZES[size]


#Code below is borrowed from UC Berkeley's AI class.
class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)