class Queue:

    def __init__(self):
        self._items = []
        
    def enqueue(self, object):
        self._items.insert(0, object)
        
    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        else:
            return self._items.pop()
            
    def peek(self):
        if not self._items:
            raise IndexError("peek at empty queue")
        return self._items[-1]

    def is_empty(self):
        return self._items == []
        
    def __len__(self):
        return len(self._items)





        