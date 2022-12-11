class UnsafeStack:
    def __init__(self, n):
        self.stack = [None for _ in range(n)]
        self.pointer = -1
        self.capacity = n
        self.maxUnPop = 0 # We cannot unpop element from the get-go

    def push(self, value):
        """Adds an element to the stack"""
        if self.pointer < self.capacity:
            self.pointer += 1
            self.stack[self.pointer] = value
        else:
            raise Exception("Stack overflow")
    
    def pop(self):
        """Returns the last element of the stack and moves the pointer"""
        if self.pointer >= 0:
            val = self.stack[self.pointer]
            self.pointer -= 1
            self.maxUnPop += 1
            return val
        else:
            raise Exception("Stack underflow")

    def isEmpty(self):
        """Returns True if the stack is empty, False otherwise"""
        return self.pointer == -1

    def UnPop(self):
        """Returns the previous element of the stack"""
        if self.pointer < self.maxUnPop:
            self.pointer += 1
            return self.stack[self.pointer]
        else:
            raise Exception("Cannot unpop")


if __name__ == "__main__":
    s = UnsafeStack(10)
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.pop())
    print(s.pop())
    #print(s.pop())
    #print(s.pop()) # Should raise an exception
    s.push(4)
    print(s.pointer)
    print(s.stack)
    print(s.UnPop())