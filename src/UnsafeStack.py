class UnsafeStack:
    __slots__ = ("stack", "pointer", "capacity", "max_unpop")
    def __init__(self):
        self.stack = []
        self.pointer = -1
        self.capacity = 0
        self.max_unpop = 0 # We cannot unpop element from the get-go

    def push(self, item):
        """Adds an element to the stack"""
        self.max_unpop = 0
        self.pointer += 1
        if self.pointer < self.capacity:    # If the list has unused space 
            self.stack[self.pointer] = item
        else:
            self.stack.append(item)
            self.capacity += 1

    def pop(self):
        """Returns the last element of the stack and moves the pointer"""
        if self.is_empty():
            raise Exception("Stack Underflow")
        val = self.stack[self.pointer]
        self.pointer -= 1
        self.max_unpop += 1
        return val

    def is_empty(self):
        """Returns True if the stack is empty, False otherwise"""
        return self.pointer == -1

    def unpop(self):
        """ Returns the previous element of the stack """
        if self.max_unpop < 1:
            raise Exception("Cannot Unpop")
        self.pointer += 1
        self.max_unpop -= 1
        return self.stack[self.pointer]

    def __str__(self) -> str:
        return str(self.stack[:self.pointer])

if __name__ == "__main__":
    s = UnsafeStack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.pop())
    print(s.pop())
    #print(s.pop())
    #print(s.pop()) # Should raise an exception
    print(s.unpop())
    s.push(4)
    print(s.pointer)
    print(s)
    print(s.stack)