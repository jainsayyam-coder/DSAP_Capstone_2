"""Bounded array-based stack reference with precise JSON output."""

import json


class Stack:
    """Last-in, first-out stack with a fixed positive capacity."""

    def __init__(self, capacity=7):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self.items = []

    @property
    def top(self):
        return len(self.items) - 1

    def is_empty(self):
        return not self.items

    def is_full(self):
        return len(self.items) == self.capacity

    def push(self, value):
        if self.is_full():
            return False
        self.items.append(value)
        return True

    def pop(self):
        return self.items.pop() if self.items else None

    def peek(self):
        return self.items[-1] if self.items else None

    def clear(self):
        self.items.clear()

    def snapshot(self):
        return {
            "items": list(self.items),
            "top_index": self.top,
            "top_value": self.peek(),
            "size": len(self.items),
            "capacity": self.capacity,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
        }


def _report(operation, result, stack):
    print(json.dumps({
        "operation": operation,
        "result": result,
        "state": stack.snapshot(),
    }, sort_keys=True))


def main():
    stack = Stack(capacity=3)
    _report("push(10)", stack.push(10), stack)
    _report("push(20)", stack.push(20), stack)
    _report("push(30)", stack.push(30), stack)
    _report("push(40)", stack.push(40), stack)
    _report("peek()", stack.peek(), stack)
    _report("pop()", stack.pop(), stack)
    _report("pop()", stack.pop(), stack)


if __name__ == "__main__":
    main()