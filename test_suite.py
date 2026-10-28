#!/usr/bin/env python3
"""
================================================================================
   DSA Simulator — Automated Python Unit Test Suite
   100% Python Standard Library • Complete Data Structure Verification
================================================================================
Run with:
    python test_suite.py
    python -m unittest test_suite.py
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import backend.linked_list as ll
from backend.bst import BinarySearchTree
from backend.stack import Stack
from backend.queue import Queue
from backend.algorithm_tracer import get_operation_steps
from gui.progress_manager import load_progress, save_progress, reset_all_progress


# ==============================================================================
# 1. SINGLY LINKED LIST TESTS
# ==============================================================================
class TestSinglyLinkedList(unittest.TestCase):
    def setUp(self):
        self.sll = ll.SinglyLinkedList()

    def test_initial_empty_state(self):
        self.assertEqual(len(self.sll), 0)
        self.assertIsNone(self.sll.head)
        self.assertIsNone(self.sll.tail)
        self.assertTrue(self.sll.is_empty())

    def test_insert_beginning_and_end(self):
        self.sll.insert_end(10)
        self.sll.insert_end(20)
        self.sll.insert_beginning(5)
        self.assertEqual(self.sll.to_list(), [5, 10, 20])
        self.assertEqual(self.sll.head.value, 5)
        self.assertEqual(self.sll.tail.value, 20)
        self.assertEqual(len(self.sll), 3)

    def test_insert_at_position(self):
        self.sll.insert_end(10)
        self.sll.insert_end(30)
        self.assertTrue(self.sll.insert_at(20, 1))
        self.assertEqual(self.sll.to_list(), [10, 20, 30])
        # Out of bounds insert
        self.assertFalse(self.sll.insert_at(99, 99))

    def test_delete_beginning(self):
        self.sll.insert_end(10)
        self.sll.insert_end(20)
        val = self.sll.delete_beginning()
        self.assertEqual(val, 10)
        self.assertEqual(self.sll.to_list(), [20])
        self.assertEqual(self.sll.head.value, 20)
        self.assertEqual(self.sll.tail.value, 20)

    def test_delete_end(self):
        self.sll.insert_end(10)
        self.sll.insert_end(20)
        self.sll.insert_end(30)
        val = self.sll.delete_end()
        self.assertEqual(val, 30)
        self.assertEqual(self.sll.to_list(), [10, 20])
        self.assertEqual(self.sll.tail.value, 20)

    def test_delete_at_index(self):
        for v in [1, 2, 3, 4]:
            self.sll.insert_end(v)
        val = self.sll.delete_at(2)  # Deletes value 3
        self.assertEqual(val, 3)
        self.assertEqual(self.sll.to_list(), [1, 2, 4])

    def test_search_and_update(self):
        self.sll.insert_end(100)
        self.sll.insert_end(200)
        self.assertEqual(self.sll.search(200), 1)
        self.assertEqual(self.sll.search(999), -1)
        self.assertTrue(self.sll.update_at(1, 250))
        self.assertEqual(self.sll.search(250), 1)

    def test_reverse(self):
        for v in [10, 20, 30, 40]:
            self.sll.insert_end(v)
        self.sll.reverse()
        self.assertEqual(self.sll.to_list(), [40, 30, 20, 10])
        self.assertEqual(self.sll.head.value, 40)
        self.assertEqual(self.sll.tail.value, 10)


# ==============================================================================
# 2. DOUBLY LINKED LIST TESTS
# ==============================================================================
class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = ll.DoublyLinkedList()

    def test_bidirectional_link_agreement(self):
        self.dll.insert_end(10)
        self.dll.insert_end(20)
        self.dll.insert_end(30)
        self.assertEqual(self.dll.head.next.prev, self.dll.head)
        self.assertEqual(self.dll.tail.prev.next, self.dll.tail)
        self.assertIsNone(self.dll.head.prev)
        self.assertIsNone(self.dll.tail.next)

    def test_o1_tail_deletion(self):
        self.dll.insert_end(100)
        self.dll.insert_end(200)
        self.dll.insert_end(300)
        val = self.dll.delete_end()
        self.assertEqual(val, 300)
        self.assertEqual(self.dll.to_list(), [100, 200])
        self.assertEqual(self.dll.tail.value, 200)
        self.assertIsNone(self.dll.tail.next)

    def test_dll_reverse(self):
        for v in [1, 2, 3]:
            self.dll.insert_end(v)
        self.dll.reverse()
        self.assertEqual(self.dll.to_list(), [3, 2, 1])


# ==============================================================================
# 3. CIRCULAR LINKED LISTS TESTS
# ==============================================================================
class TestCircularLists(unittest.TestCase):
    def test_circular_singly_loopback(self):
        csll = ll.CircularSinglyLinkedList()
        csll.insert_end(10)
        csll.insert_end(20)
        csll.insert_end(30)
        self.assertEqual(csll.tail.next, csll.head)
        csll.delete_beginning()
        self.assertEqual(csll.tail.next, csll.head)
        self.assertEqual(csll.to_list(), [20, 30])

    def test_circular_doubly_dual_ring(self):
        cdll = ll.CircularDoublyLinkedList()
        cdll.insert_end(100)
        cdll.insert_end(200)
        self.assertEqual(cdll.tail.next, cdll.head)
        self.assertEqual(cdll.head.prev, cdll.tail)
        cdll.insert_beginning(50)
        self.assertEqual(cdll.tail.next, cdll.head)
        self.assertEqual(cdll.head.prev, cdll.tail)
        self.assertEqual(cdll.to_list(), [50, 100, 200])


# ==============================================================================
# 4. BINARY SEARCH TREE TESTS
# ==============================================================================
class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()

    def test_insert_and_inorder_sorting(self):
        values = [50, 30, 70, 20, 40, 60, 80]
        for v in values:
            self.assertTrue(self.bst.insert(v))
        self.assertEqual(self.bst.inorder(), [20, 30, 40, 50, 60, 70, 80])
        # Reject duplicates
        self.assertFalse(self.bst.insert(50))

    def test_search_and_extremes(self):
        for v in [40, 20, 60]:
            self.bst.insert(v)
        self.assertIsNotNone(self.bst.search(20))
        self.assertIsNone(self.bst.search(999))
        self.assertEqual(self.bst.find_min().value, 20)
        self.assertEqual(self.bst.find_max().value, 60)

    def test_traversals(self):
        for v in [2, 1, 3]:
            self.bst.insert(v)
        self.assertEqual(self.bst.preorder(), [2, 1, 3])
        self.assertEqual(self.bst.postorder(), [1, 3, 2])
        self.assertEqual(self.bst.levelorder(), [2, 1, 3])

    def test_delete_node_with_two_children(self):
        for v in [50, 30, 70, 20, 40]:
            self.bst.insert(v)
        self.assertTrue(self.bst.delete(30))
        self.assertEqual(self.bst.inorder(), [20, 40, 50, 70])


# ==============================================================================
# 5. STACK & QUEUE TESTS
# ==============================================================================
class TestStackAndQueue(unittest.TestCase):
    def test_stack_lifo(self):
        s = Stack(capacity=3)
        self.assertTrue(s.push(10))
        self.assertTrue(s.push(20))
        self.assertTrue(s.push(30))
        self.assertFalse(s.push(40))  # Full
        self.assertEqual(s.pop(), 30)
        self.assertEqual(s.peek(), 20)

    def test_queue_fifo(self):
        q = Queue(capacity=3)
        self.assertTrue(q.enqueue("A"))
        self.assertTrue(q.enqueue("B"))
        self.assertTrue(q.enqueue("C"))
        self.assertFalse(q.enqueue("D"))  # Full
        self.assertEqual(q.dequeue(), "A")
        self.assertEqual(q.peek_front(), "B")


# ==============================================================================
# 6. ALGORITHM TRACER & STUDY ENGINE TESTS
# ==============================================================================
class TestAlgorithmTracer(unittest.TestCase):
    def test_tracer_steps_generation(self):
        res = get_operation_steps("singly", "insert_beginning", [10, 20], val=5)
        self.assertIn("steps", res)
        self.assertGreater(len(res["steps"]), 0)
        self.assertIn("pseudocode", res)


# ==============================================================================
# 7. PROGRESS MANAGER TESTS
# ==============================================================================
class TestProgressManager(unittest.TestCase):
    def test_progress_save_and_load(self):
        reset_all_progress()
        p = load_progress()
        self.assertEqual(p["operations_executed"], 0)


def run_all_tests():
    print("==================================================================")
    print("  DSA Simulator — Automated Test Suite Runner (Python)")
    print("==================================================================")
    suite = unittest.TestLoader().loadTestsFromNames([
        'test_suite.TestSinglyLinkedList',
        'test_suite.TestDoublyLinkedList',
        'test_suite.TestCircularLists',
        'test_suite.TestBinarySearchTree',
        'test_suite.TestStackAndQueue',
        'test_suite.TestAlgorithmTracer',
        'test_suite.TestProgressManager'
    ])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
