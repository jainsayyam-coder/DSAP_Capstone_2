"""
DSA Simulator Backend Package
Pure Python implementations of fundamental data structures with rich step generators.
"""

from .linked_list import (
    SinglyLinkedList,
    DoublyLinkedList,
    CircularSinglyLinkedList,
    CircularDoublyLinkedList,
    create_list,
    execute_operation
)
from .bst import BinarySearchTree, BSTNode
from .stack import Stack
from .queue import Queue
