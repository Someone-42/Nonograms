

class UnsafeStack:
    def __init__(self, n):
        self.stack = []
        self.pointer = 0
        self.capacity = n
        self.maxUnPop = 0 # We cannot unpop element from the get-go

    def push(self, value):
        """Adds an element to the stack"""
        if self.pointer < self.capacity:
            self.stack[self.pointer] = value
            self.pointer += 1
        else:
            raise Exception("Stack overflow")
    
    def pop(self):
        """Returns the last element of the stack and moves the pointer"""
        if self.pointer > 0:
            val = self.stack[self.pointer]
            self.pointer -= 1
            self.maxUnPop += 1
            return val
        else:
            raise Exception("Stack underflow")

    def isEmpty(self):
        """Returns True if the stack is empty, False otherwise"""
        return self.pointer == 0

    def UnPop(self):
        """Returns the previous element of the stack"""
        if self.pointer < self.maxUnpop:
            self.pointer += 1
            return self.stack[self.pointer]
        else:
            raise Exception("Cannot unpop")