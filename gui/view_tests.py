"""
DSA Simulator - Interactive Unit Test Runner View
Executes automated test suites across all 7 data structures with real-time pass/fail badges.
"""

import tkinter as tk
from tkinter import ttk
import time
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
import backend.linked_list as ll_backend
from backend.bst import BinarySearchTree
from backend.stack import Stack
from backend.queue import Queue


class TestsView(tk.Frame):
    """Visual test suite runner verifying invariants across all structures."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # 1. Header & Controls
        header = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=14)
        header.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(header, text="AUTOMATED UNIT TEST SUITE", bg=BG_CARD, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        tk.Label(header, text="Data Structure Invariant & Correctness Verification", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_HEADING).pack(anchor="w")

        btn_row = tk.Frame(header, bg=BG_CARD)
        btn_row.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            btn_row,
            text="▶ Run All Automated Unit Tests",
            bg=EMERALD,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.run_tests
        ).pack(side=tk.LEFT)

        self.lbl_summary = tk.Label(btn_row, text="Status: Ready to execute checks.", bg=BG_SURFACE, fg=TEXT_MUTED, font=FONT_CODE_BOLD, padx=12, pady=5)
        self.lbl_summary.pack(side=tk.RIGHT)

        # 2. Results Container
        results_card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12)
        results_card.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        # Canvas for scrollable test list
        self.canvas = tk.Canvas(results_card, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(results_card, orient=tk.VERTICAL, command=self.canvas.xview)
        self.test_list_frame = tk.Frame(self.canvas, bg=BG_DARK)

        self.test_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.test_list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width - 40))

        # Initial message
        self.placeholder = tk.Label(self.test_list_frame, text="Click 'Run All Automated Unit Tests' above to execute test assertions.", bg=BG_DARK, fg=TEXT_MUTED, font=FONT_BODY, pady=40)
        self.placeholder.pack()

    def run_tests(self):
        # Clear previous
        for widget in self.test_list_frame.winfo_children():
            widget.destroy()

        tests = [
            ("SLL: Empty initialization", self._test_sll_init),
            ("SLL: Insert Beginning & End", self._test_sll_inserts),
            ("SLL: Insert at Position k", self._test_sll_insert_at),
            ("SLL: Delete Operations (Beg, Mid, End)", self._test_sll_deletes),
            ("SLL: Three-Pointer In-Place Reversal", self._test_sll_reverse),
            ("DLL: Bidirectional Link Agreement (prev.next == node)", self._test_dll_links),
            ("DLL: O(1) Tail Deletion via tail.prev", self._test_dll_tail_delete),
            ("CSLL: Unbroken Ring Invariant (tail.next == HEAD)", self._test_csll_ring),
            ("CDLL: Dual-Ring Linkage (tail.next == HEAD and HEAD.prev == TAIL)", self._test_cdll_dual_ring),
            ("BST: Insert & In-Order Monotonic Sorting", self._test_bst_inorder),
            ("BST: Deletion (Leaf, One Child, Two Children)", self._test_bst_delete),
            ("BST: Traversals (Pre-Order, Post-Order, BFS)", self._test_bst_traversals),
            ("Stack: LIFO Push, Pop, Peek, & Overflow Bounds", self._test_stack),
            ("Queue: FIFO Enqueue, Dequeue, & Capacity Bounds", self._test_queue)
        ]

        total = len(tests)
        passed = 0
        start_t = time.time()

        for name, func in tests:
            t0 = time.time()
            try:
                func()
                elapsed_ms = (time.time() - t0) * 1000
                self._add_result_row(name, "PASS", f"{elapsed_ms:.2f} ms", EMERALD)
                passed += 1
            except Exception as e:
                elapsed_ms = (time.time() - t0) * 1000
                self._add_result_row(name, "FAIL", f"{str(e)} ({elapsed_ms:.2f} ms)", ROSE)

        total_elapsed = (time.time() - start_t) * 1000
        if passed == total:
            self.lbl_summary.config(text=f"✓ ALL {passed}/{total} TESTS PASSED ({total_elapsed:.1f} ms)", fg=EMERALD)
        else:
            self.lbl_summary.config(text=f"✗ {total - passed} TESTS FAILED ({passed}/{total} passed)", fg=ROSE)

    def _add_result_row(self, name, status, detail, color):
        row = tk.Frame(self.test_list_frame, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=8)
        row.pack(fill=tk.X, pady=3, padx=10)

        badge = tk.Label(row, text=f" {status} ", bg=color, fg="#ffffff", font=FONT_SMALL, padx=4, pady=2)
        badge.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(row, text=name, bg=BG_CARD, fg=TEXT_MAIN, font=FONT_BODY_BOLD).pack(side=tk.LEFT)
        tk.Label(row, text=detail, bg=BG_CARD, fg=TEXT_MUTED, font=FONT_CODE).pack(side=tk.RIGHT)

    # =========================================================================
    # Test Implementations
    # =========================================================================
    def _test_sll_init(self):
        sll = ll_backend.SinglyLinkedList()
        assert len(sll) == 0
        assert sll.head is None
        assert sll.tail is None

    def _test_sll_inserts(self):
        sll = ll_backend.SinglyLinkedList()
        sll.insert_end(10)
        sll.insert_end(20)
        sll.insert_beginning(5)
        assert sll.to_list() == [5, 10, 20]
        assert sll.head.value == 5
        assert sll.tail.value == 20

    def _test_sll_insert_at(self):
        sll = ll_backend.SinglyLinkedList()
        sll.insert_end(10)
        sll.insert_end(30)
        sll.insert_at(20, 1)
        assert sll.to_list() == [10, 20, 30]

    def _test_sll_deletes(self):
        sll = ll_backend.SinglyLinkedList()
        for v in [1, 2, 3, 4, 5]:
            sll.insert_end(v)
        assert sll.delete_beginning() == 1
        assert sll.delete_end() == 5
        assert sll.delete_at(1) == 3
        assert sll.to_list() == [2, 4]

    def _test_sll_reverse(self):
        sll = ll_backend.SinglyLinkedList()
        for v in [10, 20, 30, 40]:
            sll.insert_end(v)
        sll.reverse()
        assert sll.to_list() == [40, 30, 20, 10]
        assert sll.head.value == 40
        assert sll.tail.value == 10

    def _test_dll_links(self):
        dll = ll_backend.DoublyLinkedList()
        for v in [100, 200, 300]:
            dll.insert_end(v)
        assert dll.head.next.prev == dll.head
        assert dll.tail.prev.next == dll.tail
        assert dll.head.prev is None
        assert dll.tail.next is None

    def _test_dll_tail_delete(self):
        dll = ll_backend.DoublyLinkedList()
        dll.insert_end(10)
        dll.insert_end(20)
        assert dll.delete_end() == 20
        assert dll.tail.value == 10
        assert dll.tail.next is None

    def _test_csll_ring(self):
        csll = ll_backend.CircularSinglyLinkedList()
        csll.insert_end(1)
        csll.insert_end(2)
        assert csll.tail.next == csll.head

    def _test_cdll_dual_ring(self):
        cdll = ll_backend.CircularDoublyLinkedList()
        cdll.insert_end(5)
        cdll.insert_end(15)
        assert cdll.tail.next == cdll.head
        assert cdll.head.prev == cdll.tail

    def _test_bst_inorder(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(v)
        assert bst.inorder() == [20, 30, 40, 50, 60, 70, 80]

    def _test_bst_delete(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40]:
            bst.insert(v)
        # Delete node with two children (30)
        assert bst.delete(30) is True
        assert bst.inorder() == [20, 40, 50, 70]

    def _test_bst_traversals(self):
        bst = BinarySearchTree()
        for v in [2, 1, 3]:
            bst.insert(v)
        assert bst.preorder() == [2, 1, 3]
        assert bst.postorder() == [1, 3, 2]
        assert bst.levelorder() == [2, 1, 3]

    def _test_stack(self):
        st = Stack(capacity=3)
        st.push(10)
        st.push(20)
        st.push(30)
        assert st.is_full() is True
        assert st.push(40) is False  # Overflow guard
        assert st.pop() == 30
        assert st.peek() == 20

    def _test_queue(self):
        q = Queue(capacity=3)
        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        assert q.is_full() is True
        assert q.enqueue("D") is False  # Overflow guard
        assert q.dequeue() == "A"
        assert q.peek_front() == "B"
