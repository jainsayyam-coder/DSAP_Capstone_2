"""
Linked List Learning Simulator - Python Reference Implementations
Provides complete reference classes for all 4 linked list types:
1. SinglyLinkedList
2. DoublyLinkedList
3. CircularSinglyLinkedList
4. CircularDoublyLinkedList
"""

from typing import Optional, List, Any


# ==============================================================================
# 1. SINGLY LINKED LIST (SLL)
# ==============================================================================
class SinglyNode:
    def __init__(self, value: Any):
        self.value = value
        self.next: Optional['SinglyNode'] = None

    def __repr__(self) -> str:
        return f"SinglyNode({self.value})"


class SinglyLinkedList:
    def __init__(self):
        self.head: Optional[SinglyNode] = None
        self.tail: Optional[SinglyNode] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[Any]:
        res = []
        curr = self.head
        while curr:
            res.append(curr.value)
            curr = curr.next
        return res

    def insert_beginning(self, value: Any) -> None:
        new_node = SinglyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._length += 1

    def insert_end(self, value: Any) -> None:
        new_node = SinglyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def insert_at(self, value: Any, index: int) -> bool:
        if index < 0 or index > self._length:
            return False
        if index == 0:
            self.insert_beginning(value)
            return True
        if index == self._length:
            self.insert_end(value)
            return True

        new_node = SinglyNode(value)
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        new_node.next = prev.next
        prev.next = new_node
        self._length += 1
        return True

    def delete_beginning(self) -> Optional[Any]:
        if not self.head:
            return None
        val = self.head.value
        self.head = self.head.next
        self._length -= 1
        if self._length == 0:
            self.tail = None
        return val

    def delete_end(self) -> Optional[Any]:
        if not self.head:
            return None
        if self.head == self.tail:
            val = self.head.value
            self.head = self.tail = None
            self._length = 0
            return val

        curr = self.head
        while curr.next != self.tail:
            curr = curr.next

        val = self.tail.value
        curr.next = None
        self.tail = curr
        self._length -= 1
        return val

    def delete_at(self, index: int) -> Optional[Any]:
        if index < 0 or index >= self._length:
            return None
        if index == 0:
            return self.delete_beginning()
        if index == self._length - 1:
            return self.delete_end()

        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        target = prev.next
        val = target.value
        prev.next = target.next
        self._length -= 1
        return val

    def search(self, value: Any) -> int:
        curr = self.head
        idx = 0
        while curr:
            if curr.value == value:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def reverse(self) -> None:
        prev = None
        curr = self.head
        self.tail = self.head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head = prev


    def update_at(self, index: int, value: Any) -> bool:
        if index < 0 or index >= self._length:
            return False
        curr = self.head
        for _ in range(index):
            curr = curr.next
        curr.value = value
        return True

    def clear(self) -> None:
        self.head = self.tail = None
        self._length = 0

    def snapshot(self) -> dict:
        return {
            "type": "singly",
            "length": self._length,
            "items": self.to_list(),
            "head": self.head.value if self.head else None,
            "tail": self.tail.value if self.tail else None,
            "is_empty": self.is_empty(),
        }


# ==============================================================================
# 2. DOUBLY LINKED LIST (DLL)
# ==============================================================================
class DoublyNode:
    def __init__(self, value: Any):
        self.value = value
        self.prev: Optional['DoublyNode'] = None
        self.next: Optional['DoublyNode'] = None

    def __repr__(self) -> str:
        return f"DoublyNode({self.value})"


class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[Any]:
        res = []
        curr = self.head
        while curr:
            res.append(curr.value)
            curr = curr.next
        return res

    def insert_beginning(self, value: Any) -> None:
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._length += 1

    def insert_end(self, value: Any) -> None:
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def insert_at(self, value: Any, index: int) -> bool:
        if index < 0 or index > self._length:
            return False
        if index == 0:
            self.insert_beginning(value)
            return True
        if index == self._length:
            self.insert_end(value)
            return True

        new_node = DoublyNode(value)
        curr = self.head
        for _ in range(index):
            curr = curr.next

        prev_node = curr.prev
        new_node.prev = prev_node
        new_node.next = curr
        if prev_node:
            prev_node.next = new_node
        curr.prev = new_node
        self._length += 1
        return True

    def delete_beginning(self) -> Optional[Any]:
        if not self.head:
            return None
        val = self.head.value
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self._length -= 1
        return val

    def delete_end(self) -> Optional[Any]:
        if not self.tail:
            return None
        val = self.tail.value
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self._length -= 1
        return val

    def delete_at(self, index: int) -> Optional[Any]:
        if index < 0 or index >= self._length:
            return None
        if index == 0:
            return self.delete_beginning()
        if index == self._length - 1:
            return self.delete_end()

        curr = self.head
        for _ in range(index):
            curr = curr.next

        val = curr.value
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self._length -= 1
        return val

    def search(self, value: Any) -> int:
        curr = self.head
        idx = 0
        while curr:
            if curr.value == value:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def update_at(self, index: int, value: Any) -> bool:
        if index < 0 or index >= self._length:
            return False
        curr = self.head
        for _ in range(index):
            curr = curr.next
        curr.value = value
        return True

    def reverse(self) -> None:
        if self._length < 2:
            return
        curr = self.head
        self.tail = self.head
        temp = None
        while curr:
            temp = curr.prev
            curr.prev = curr.next
            curr.next = temp
            curr = curr.prev
        if temp:
            self.head = temp.prev

    def clear(self) -> None:
        self.head = self.tail = None
        self._length = 0

    def snapshot(self) -> dict:
        return {
            "type": "doubly",
            "length": self._length,
            "items": self.to_list(),
            "head": self.head.value if self.head else None,
            "tail": self.tail.value if self.tail else None,
            "is_empty": self.is_empty(),
        }


# ==============================================================================
# 3. CIRCULAR SINGLY LINKED LIST (CSLL)
# ==============================================================================
class CircularSinglyLinkedList:
    def __init__(self):
        self.head: Optional[SinglyNode] = None
        self.tail: Optional[SinglyNode] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[Any]:
        res = []
        if not self.head:
            return res
        curr = self.head
        while True:
            res.append(curr.value)
            curr = curr.next
            if curr == self.head or len(res) >= self._length:
                break
        return res

    def insert_beginning(self, value: Any) -> None:
        new_node = SinglyNode(value)
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = new_node
        else:
            new_node.next = self.head
            self.tail.next = new_node
            self.head = new_node
        self._length += 1

    def insert_end(self, value: Any) -> None:
        new_node = SinglyNode(value)
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = new_node
        else:
            new_node.next = self.head
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def insert_at(self, value: Any, index: int) -> bool:
        if index < 0 or index > self._length:
            return False
        if index == 0:
            self.insert_beginning(value)
            return True
        if index == self._length:
            self.insert_end(value)
            return True

        new_node = SinglyNode(value)
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        new_node.next = prev.next
        prev.next = new_node
        self._length += 1
        return True

    def delete_beginning(self) -> Optional[Any]:
        if not self.head:
            return None
        val = self.head.value
        if self._length == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.tail.next = self.head
        self._length -= 1
        return val

    def delete_end(self) -> Optional[Any]:
        if not self.head:
            return None
        if self._length == 1:
            val = self.head.value
            self.head = self.tail = None
            self._length = 0
            return val

        curr = self.head
        while curr.next != self.tail:
            curr = curr.next

        val = self.tail.value
        curr.next = self.head
        self.tail = curr
        self._length -= 1
        return val

    def delete_at(self, index: int) -> Optional[Any]:
        if index < 0 or index >= self._length:
            return None
        if index == 0:
            return self.delete_beginning()
        if index == self._length - 1:
            return self.delete_end()

        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        target = prev.next
        val = target.value
        prev.next = target.next
        self._length -= 1
        return val

    def search(self, value: Any) -> int:
        if not self.head:
            return -1
        curr = self.head
        for i in range(self._length):
            if curr.value == value:
                return i
            curr = curr.next
        return -1

    def update_at(self, index: int, value: Any) -> bool:
        if index < 0 or index >= self._length:
            return False
        curr = self.head
        for _ in range(index):
            curr = curr.next
        curr.value = value
        return True

    def clear(self) -> None:
        self.head = self.tail = None
        self._length = 0

    def snapshot(self) -> dict:
        return {
            "type": "circular-singly",
            "length": self._length,
            "items": self.to_list(),
            "head": self.head.value if self.head else None,
            "tail": self.tail.value if self.tail else None,
            "is_empty": self.is_empty(),
        }


# ==============================================================================
# 4. CIRCULAR DOUBLY LINKED LIST (CDLL)
# ==============================================================================
class CircularDoublyLinkedList:
    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[Any]:
        res = []
        if not self.head:
            return res
        curr = self.head
        while True:
            res.append(curr.value)
            curr = curr.next
            if curr == self.head or len(res) >= self._length:
                break
        return res

    def insert_beginning(self, value: Any) -> None:
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node
        self._length += 1

    def insert_end(self, value: Any) -> None:
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        self._length += 1

    def insert_at(self, value: Any, index: int) -> bool:
        if index < 0 or index > self._length:
            return False
        if index == 0:
            self.insert_beginning(value)
            return True
        if index == self._length:
            self.insert_end(value)
            return True

        new_node = DoublyNode(value)
        curr = self.head
        for _ in range(index):
            curr = curr.next

        prev_node = curr.prev
        new_node.prev = prev_node
        new_node.next = curr
        prev_node.next = new_node
        curr.prev = new_node
        self._length += 1
        return True

    def delete_beginning(self) -> Optional[Any]:
        if not self.head:
            return None
        val = self.head.value
        if self._length == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = self.tail
            self.tail.next = self.head
        self._length -= 1
        return val

    def delete_end(self) -> Optional[Any]:
        if not self.tail:
            return None
        val = self.tail.value
        if self._length == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = self.head
            self.head.prev = self.tail
        self._length -= 1
        return val

    def delete_at(self, index: int) -> Optional[Any]:
        if index < 0 or index >= self._length:
            return None
        if index == 0:
            return self.delete_beginning()
        if index == self._length - 1:
            return self.delete_end()

        curr = self.head
        for _ in range(index):
            curr = curr.next

        val = curr.value
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self._length -= 1
        return val

    def search(self, value: Any) -> int:
        if not self.head:
            return -1
        curr = self.head
        for i in range(self._length):
            if curr.value == value:
                return i
            curr = curr.next
        return -1

    def update_at(self, index: int, value: Any) -> bool:
        if index < 0 or index >= self._length:
            return False
        curr = self.head
        for _ in range(index):
            curr = curr.next
        curr.value = value
        return True

    def clear(self) -> None:
        self.head = self.tail = None
        self._length = 0

    def snapshot(self) -> dict:
        return {
            "type": "circular-doubly",
            "length": self._length,
            "items": self.to_list(),
            "head": self.head.value if self.head else None,
            "tail": self.tail.value if self.tail else None,
            "is_empty": self.is_empty(),
        }


# ==============================================================================
# Helper Factory & Operation Dispatcher
# ==============================================================================
def create_list(list_type: str):
    normalized = list_type.lower().replace("_", "-")
    if "singly" in normalized and "circular" not in normalized:
        return SinglyLinkedList()
    elif "doubly" in normalized and "circular" not in normalized:
        return DoublyLinkedList()
    elif "circular-singly" in normalized or "csll" in normalized:
        return CircularSinglyLinkedList()
    elif "circular-doubly" in normalized or "cdll" in normalized:
        return CircularDoublyLinkedList()
    return SinglyLinkedList()


def execute_operation(list_obj, op: str, value: Any = None, position: int = None, target: Any = None) -> dict:
    op_clean = op.lower().replace("_", "").replace("-", "")
    success = True
    result_val = None
    msg = ""

    if op_clean in ("insertbeginning", "insertbeg", "pushfront"):
        list_obj.insert_beginning(value)
        msg = f"Inserted {value} at beginning"
    elif op_clean in ("insertend", "append", "pushback"):
        list_obj.insert_end(value)
        msg = f"Inserted {value} at end"
    elif op_clean in ("insertat", "insert"):
        pos = int(position) if position is not None else 0
        success = list_obj.insert_at(value, pos)
        msg = f"Inserted {value} at index {pos}" if success else f"Failed to insert at invalid index {pos}"
    elif op_clean in ("deletebeginning", "deletebeg", "popfront"):
        result_val = list_obj.delete_beginning()
        success = result_val is not None
        msg = f"Deleted {result_val} from beginning" if success else "List is empty, cannot delete from beginning"
    elif op_clean in ("deleteend", "popback", "pop"):
        result_val = list_obj.delete_end()
        success = result_val is not None
        msg = f"Deleted {result_val} from end" if success else "List is empty, cannot delete from end"
    elif op_clean in ("deleteat", "removeat"):
        pos = int(position) if position is not None else 0
        result_val = list_obj.delete_at(pos)
        success = result_val is not None
        msg = f"Deleted {result_val} at index {pos}" if success else f"Failed to delete at invalid index {pos}"
    elif op_clean in ("search", "find"):
        search_val = value if value is not None else target
        idx = list_obj.search(search_val)
        success = idx != -1
        result_val = idx
        msg = f"Found {search_val} at index {idx}" if success else f"Value {search_val} not found in list"
    elif op_clean in ("update", "updateat"):
        pos = int(position) if position is not None else 0
        success = list_obj.update_at(pos, value)
        msg = f"Updated index {pos} with value {value}" if success else f"Failed to update at index {pos}"
    elif op_clean in ("reverse",):
        if hasattr(list_obj, "reverse"):
            list_obj.reverse()
            msg = "Reversed list successfully"
        else:
            success = False
            msg = "Reversal is only supported for Singly and Doubly linked lists"
    elif op_clean in ("clear", "reset"):
        list_obj.clear()
        msg = "List cleared"
    elif op_clean in ("getstate", "snapshot"):
        msg = "Current state retrieved"
    else:
        success = False
        msg = f"Unknown operation: {op}"

    return {
        "success": success,
        "operation": op,
        "message": msg,
        "result": result_val,
        "length": len(list_obj),
        "items": list_obj.to_list(),
        "state": list_obj.snapshot() if hasattr(list_obj, "snapshot") else {"items": list_obj.to_list()}
    }


if __name__ == "__main__":
    print("Testing Python Linked List Reference Implementations...")
    sll = SinglyLinkedList()
    sll.insert_end(10)
    sll.insert_end(20)
    sll.insert_beginning(5)
    assert sll.to_list() == [5, 10, 20]
    sll.reverse()
    assert sll.to_list() == [20, 10, 5]
    print("  [OK] SinglyLinkedList passed")

    dll = DoublyLinkedList()
    dll.insert_end(100)
    dll.insert_end(200)
    dll.insert_beginning(50)
    assert dll.to_list() == [50, 100, 200]
    assert dll.delete_end() == 200
    assert dll.to_list() == [50, 100]
    print("  [OK] DoublyLinkedList passed")

    csll = CircularSinglyLinkedList()
    csll.insert_end(1)
    csll.insert_end(2)
    csll.insert_beginning(0)
    assert csll.to_list() == [0, 1, 2]
    assert csll.tail.next == csll.head
    print("  [OK] CircularSinglyLinkedList passed")

    cdll = CircularDoublyLinkedList()
    cdll.insert_end(11)
    cdll.insert_end(22)
    cdll.insert_beginning(33)
    assert cdll.to_list() == [33, 11, 22]
    assert cdll.tail.next == cdll.head
    assert cdll.head.prev == cdll.tail
    print("  [OK] CircularDoublyLinkedList passed")
    print("All Python backend reference tests passed successfully!")

