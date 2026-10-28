"""
Binary Search Tree (BST) Implementation with Step Generation & Tree Layout
Zero external dependencies, standard library only.
"""

from typing import Optional, List, Dict, Any, Generator
import random


class BSTNode:
    def __init__(self, value: int, address: Optional[str] = None):
        self.value = value
        self.address = address or f"0x{random.randint(0x7ffe00, 0x7fffef):06x}"
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.x: float = 0.0
        self.y: float = 0.0
        self.level: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "address": self.address,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "x": self.x,
            "y": self.y,
            "level": self.level
        }


class BinarySearchTree:
    """Complete Binary Search Tree with automated 2D coordinates computation."""

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.root is None

    def clear(self) -> None:
        self.root = None
        self._size = 0

    def insert(self, value: int) -> bool:
        """Insert value into BST. Returns True if inserted, False if duplicate."""
        if self.root is None:
            self.root = BSTNode(value)
            self._size = 1
            self.compute_coordinates()
            return True

        curr = self.root
        while True:
            if value == curr.value:
                return False  # Duplicate values disallowed in standard BST
            elif value < curr.value:
                if curr.left is None:
                    curr.left = BSTNode(value)
                    self._size += 1
                    self.compute_coordinates()
                    return True
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(value)
                    self._size += 1
                    self.compute_coordinates()
                    return True
                curr = curr.right

    def search(self, value: int) -> Optional[BSTNode]:
        """Search for a value in BST."""
        curr = self.root
        while curr:
            if curr.value == value:
                return curr
            elif value < curr.value:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def find_min(self, node: Optional[BSTNode] = None) -> Optional[BSTNode]:
        """Find minimum value node in subtree."""
        curr = node if node else self.root
        if not curr:
            return None
        while curr.left:
            curr = curr.left
        return curr

    def find_max(self, node: Optional[BSTNode] = None) -> Optional[BSTNode]:
        """Find maximum value node in subtree."""
        curr = node if node else self.root
        if not curr:
            return None
        while curr.right:
            curr = curr.right
        return curr

    def delete(self, value: int) -> bool:
        """Delete a value from BST. Returns True if deleted, False if not found."""
        if not self.root:
            return False

        def _delete_node(node: Optional[BSTNode], val: int) -> tuple[Optional[BSTNode], bool]:
            if not node:
                return None, False

            deleted = False
            if val < node.value:
                node.left, deleted = _delete_node(node.left, val)
            elif val > node.value:
                node.right, deleted = _delete_node(node.right, val)
            else:
                deleted = True
                # Case 1: Leaf node
                if not node.left and not node.right:
                    return None, True
                # Case 2: One child
                if not node.left:
                    return node.right, True
                if not node.right:
                    return node.left, True
                # Case 3: Two children -> Replace with In-order Successor (min of right subtree)
                succ = self.find_min(node.right)
                node.value = succ.value
                node.address = succ.address
                node.right, _ = _delete_node(node.right, succ.value)

            return node, deleted

        self.root, was_deleted = _delete_node(self.root, value)
        if was_deleted:
            self._size -= 1
            self.compute_coordinates()
        return was_deleted

    def get_height(self, node: Optional[BSTNode] = None) -> int:
        """Compute height of tree."""
        if node is None and self.root is None:
            return 0
        target = node if node else self.root

        def _h(n: Optional[BSTNode]) -> int:
            if not n:
                return 0
            return 1 + max(_h(n.left), _h(n.right))

        return _h(target)

    # --------------------------------------------------------------------------
    # Traversals
    # --------------------------------------------------------------------------
    def inorder(self) -> List[int]:
        res = []
        def _in(n):
            if n:
                _in(n.left)
                res.append(n.value)
                _in(n.right)
        _in(self.root)
        return res

    def preorder(self) -> List[int]:
        res = []
        def _pre(n):
            if n:
                res.append(n.value)
                _pre(n.left)
                _pre(n.right)
        _pre(self.root)
        return res

    def postorder(self) -> List[int]:
        res = []
        def _post(n):
            if n:
                _post(n.left)
                _post(n.right)
                res.append(n.value)
        _post(self.root)
        return res

    def levelorder(self) -> List[int]:
        """Breadth-First Search (Level-order) traversal."""
        if not self.root:
            return []
        res = []
        q = [self.root]
        while q:
            curr = q.pop(0)
            res.append(curr.value)
            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)
        return res

    # --------------------------------------------------------------------------
    # Step-by-Step Traversal Tracing for Visualizer
    # --------------------------------------------------------------------------
    def trace_traversal(self, order: str) -> List[Dict[str, Any]]:
        """Returns ordered steps for animation with visited nodes and descriptions."""
        steps = []
        visited = []

        if not self.root:
            return [{"node": None, "visited": [], "action": "Tree is empty", "code_line": 1}]

        if order.lower() == "inorder":
            def _in(n):
                if not n:
                    return
                steps.append({"node": n, "visited": list(visited), "action": f"Traverse left subtree of {n.value}", "code_line": 2})
                _in(n.left)
                visited.append(n.value)
                steps.append({"node": n, "visited": list(visited), "action": f"Visit node {n.value}", "code_line": 3})
                steps.append({"node": n, "visited": list(visited), "action": f"Traverse right subtree of {n.value}", "code_line": 4})
                _in(n.right)
            _in(self.root)

        elif order.lower() == "preorder":
            def _pre(n):
                if not n:
                    return
                visited.append(n.value)
                steps.append({"node": n, "visited": list(visited), "action": f"Visit node {n.value} (Root)", "code_line": 2})
                _pre(n.left)
                _pre(n.right)
            _pre(self.root)

        elif order.lower() == "postorder":
            def _post(n):
                if not n:
                    return
                steps.append({"node": n, "visited": list(visited), "action": f"Traverse left subtree of {n.value}", "code_line": 2})
                _post(n.left)
                steps.append({"node": n, "visited": list(visited), "action": f"Traverse right subtree of {n.value}", "code_line": 3})
                _post(n.right)
                visited.append(n.value)
                steps.append({"node": n, "visited": list(visited), "action": f"Visit node {n.value}", "code_line": 4})
            _post(self.root)

        elif order.lower() == "levelorder":
            q = [self.root]
            while q:
                curr = q.pop(0)
                visited.append(curr.value)
                steps.append({"node": curr, "visited": list(visited), "action": f"Dequeue and visit node {curr.value}", "code_line": 3})
                if curr.left:
                    q.append(curr.left)
                if curr.right:
                    q.append(curr.right)

        return steps

    # --------------------------------------------------------------------------
    # 2D Coordinate Layout Engine for Clean Visual Tree Rendering
    # --------------------------------------------------------------------------
    def compute_coordinates(self, canvas_width: float = 800.0, top_y: float = 60.0, level_height: float = 70.0) -> None:
        """Assign (x, y) coordinates to all nodes for aesthetic rendering without overlaps."""
        if not self.root:
            return

        def _assign_inorder_positions(node: Optional[BSTNode], level: int, counter: List[int]):
            if not node:
                return
            _assign_inorder_positions(node.left, level + 1, counter)
            node.x_rank = counter[0]
            node.level = level
            node.y = top_y + level * level_height
            counter[0] += 1
            _assign_inorder_positions(node.right, level + 1, counter)

        counter = [0]
        _assign_inorder_positions(self.root, 0, counter)
        total_nodes = max(counter[0], 1)

        # Scale x positions evenly across canvas width
        padding = 50.0
        available_width = max(canvas_width - 2 * padding, 200.0)
        spacing = available_width / max(total_nodes, 1)

        def _finalize_x(node: Optional[BSTNode]):
            if not node:
                return
            node.x = padding + (node.x_rank + 0.5) * spacing
            _finalize_x(node.left)
            _finalize_x(node.right)

        _finalize_x(self.root)
