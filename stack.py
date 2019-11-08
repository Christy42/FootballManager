
class Stack:
    def __init__(self):
        self.items = []

    @property
    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    @property
    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
