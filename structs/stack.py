class Stack:
    def __init__(self):
        """
        Create a new stack. We will do that by creating an instance variable
        named items that is an empty list to begin with.
        """
        self._items = []

    def push(self, item):
        """
        Push a new item onto the top of the stack.

        In actuality, append on a list pushes the item onto the end of a list.
        However, because we are also popping from the end of the list, this is
        not important. If we were pushing/popping from the beginning of a list,
        the operations would not be O(1).  As we learned earlier,
        inserting at position 0 is an O(n) operation.
        """
        self._items.append(item)

    def pop(self):
        """
        Return and remove the item from the top of the stack.

        If the stack is empty, raise an IndexError.
        """
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """
        Return the item from the top of the stack.

        If the stack is empty, raise an IndexError.
        """
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return self._items == []
        
    def __len__(self):
        """
        Return the size of the stack.
        """
        return len(self._items)
















