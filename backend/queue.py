"""Bounded FIFO queue reference with precise JSON output."""

import json
from collections import deque


class Queue:
    """First-in, first-out queue with a fixed positive capacity."""

    def __init__(self, capacity=7):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self.items = deque()

    def is_empty(self):
        return not self.items

    def is_full(self):
        return len(self.items) == self.capacity

    def enqueue(self, value):
        if self.is_full():
            return False
        self.items.append(value)
        return True

    def dequeue(self):
        return self.items.popleft() if self.items else None

    def peek_front(self):
        return self.items[0] if self.items else None

    def peek_rear(self):
        return self.items[-1] if self.items else None

    def clear(self):
        self.items.clear()

    def snapshot(self):
        return {
            "items": list(self.items),
            "front_index": 0 if self.items else None,
            "front_value": self.peek_front(),
            "rear_index": len(self.items) - 1 if self.items else None,
            "rear_value": self.peek_rear(),
            "size": len(self.items),
            "capacity": self.capacity,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
        }


def _report(operation, result, queue):
    print(json.dumps({
        "operation": operation,
        "result": result,
        "state": queue.snapshot(),
    }, sort_keys=True))


def main():
    queue = Queue(capacity=3)
    _report("enqueue(10)", queue.enqueue(10), queue)
    _report("enqueue(20)", queue.enqueue(20), queue)
    _report("enqueue(30)", queue.enqueue(30), queue)
    _report("enqueue(40)", queue.enqueue(40), queue)
    _report("peek_front()", queue.peek_front(), queue)
    _report("dequeue()", queue.dequeue(), queue)
    _report("dequeue()", queue.dequeue(), queue)


if __name__ == "__main__":
    main()