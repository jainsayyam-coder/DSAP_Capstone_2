"""
DSA Simulator - Interactive Quiz & Assessment System View
Curated question bank across Beginner, Intermediate, and Advanced tiers
with instant pedagogical feedback, score tracking, and offline persistence.
"""

import tkinter as tk
from tkinter import ttk
import random
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
from gui.progress_manager import record_quiz_score

QUIZ_BANK = [
    # Beginner Tier
    {
        "id": "b1",
        "tier": "Beginner",
        "question": "What does the HEAD reference in a standard Singly Linked List point to?",
        "options": [
            "The memory address of the first node in the sequence",
            "The total number of nodes currently allocated",
            "The last node in the chain",
            "The predecessor of the NULL terminator"
        ],
        "answer_idx": 0,
        "explanation": "HEAD is the primary entry pointer to the list. It holds the 64-bit memory address of node 0. If HEAD is NULL, the list is empty."
    },
    {
        "id": "b2",
        "tier": "Beginner",
        "question": "In a non-circular Singly Linked List, what value does TAIL.next hold?",
        "options": [
            "NULL (or None/nullptr)",
            "The HEAD memory address",
            "Its own address (self-loop)",
            "An undefined random memory garbage value"
        ],
        "answer_idx": 0,
        "explanation": "In linear singly linked lists, the final node terminates at NULL, indicating that no further successor nodes exist in the chain."
    },
    {
        "id": "b3",
        "tier": "Beginner",
        "question": "What is the time complexity to insert a new node at the beginning of a Linked List?",
        "options": [
            "O(1) Constant Time",
            "O(n) Linear Time",
            "O(log n) Logarithmic Time",
            "O(n²) Quadratic Time"
        ],
        "answer_idx": 0,
        "explanation": "Prepending at the head requires only two pointer operations (newNode.next = HEAD; HEAD = newNode), regardless of how many elements exist."
    },
    {
        "id": "b4",
        "tier": "Beginner",
        "question": "Which pointer enables backwards traversal in a Doubly Linked List?",
        "options": [
            "PREV pointer",
            "NEXT pointer",
            "HEAD pointer",
            "DATA pointer"
        ],
        "answer_idx": 0,
        "explanation": "Every node in a Doubly Linked List holds both a forward NEXT pointer and a backward PREV pointer connecting to its predecessor."
    },
    {
        "id": "b5",
        "tier": "Beginner",
        "question": "In a Circular Singly Linked List, what does TAIL.next point to?",
        "options": [
            "The HEAD node",
            "NULL",
            "TAIL itself",
            "The middle node"
        ],
        "answer_idx": 0,
        "explanation": "By definition, the final node in a circular list loops back to HEAD, establishing an unbroken ring with zero NULL terminators."
    },

    # Intermediate Tier
    {
        "id": "i1",
        "tier": "Intermediate",
        "question": "Why is deleting the tail node O(n) in a Singly Linked List even if a TAIL pointer is kept?",
        "options": [
            "Because we must walk from HEAD to find the second-to-last node to update TAIL",
            "Because memory reclamation in C requires traversing all preceding nodes",
            "Because TAIL.next cannot be modified",
            "Because the array must be shifted to fill the gap"
        ],
        "answer_idx": 0,
        "explanation": "To delete the tail, you must set tail = second_to_last. Since singly linked nodes do not possess a backward pointer, you must walk n-1 steps from HEAD."
    },
    {
        "id": "i2",
        "tier": "Intermediate",
        "question": "When inserting a node between predecessor A and successor B, which link order is safe?",
        "options": [
            "Set newNode.next = A.next first, then set A.next = newNode",
            "Set A.next = newNode first, then set newNode.next = B",
            "Order does not matter in linked list rewiring",
            "Clear A.next to NULL first, then assign newNode"
        ],
        "answer_idx": 0,
        "explanation": "You must link newNode.next to the successor BEFORE overwriting A.next; otherwise, the pointer to B and the rest of the list is permanently lost!"
    },
    {
        "id": "i3",
        "tier": "Intermediate",
        "question": "How many pointers are required to reverse a Singly Linked List in-place in O(1) auxiliary space?",
        "options": [
            "3 pointers (prev, curr, nextTemp)",
            "1 pointer only",
            "2 pointers only",
            "4 pointers (head, tail, slow, fast)"
        ],
        "answer_idx": 0,
        "explanation": "Three pointers are essential: 'curr' tracks the active node, 'prev' stores the inverted target, and 'nextTemp' caches curr.next before it is overwritten."
    },
    {
        "id": "i4",
        "tier": "Intermediate",
        "question": "How does Tortoise & Hare (Floyd's algorithm) identify the middle node in one pass?",
        "options": [
            "Fast advances 2 nodes while Slow advances 1 node; when Fast reaches end, Slow is at the middle",
            "Both pointers move at equal speeds from opposite ends",
            "Fast counts the total nodes, then Slow walks half the count",
            "Slow advances only when node values are even numbers"
        ],
        "answer_idx": 0,
        "explanation": "Because the fast pointer moves at 2x the velocity of the slow pointer, when the fast pointer reaches the end, the slow pointer is precisely halfway."
    },
    {
        "id": "i5",
        "tier": "Intermediate",
        "question": "What is the memory overhead per node in a 64-bit Doubly Linked List (excluding data payload)?",
        "options": [
            "16 Bytes (two 8-byte 64-bit pointers: PREV and NEXT)",
            "4 Bytes",
            "8 Bytes (one 64-bit pointer)",
            "32 Bytes"
        ],
        "answer_idx": 0,
        "explanation": "On a 64-bit CPU architecture, every pointer address occupies 8 bytes (64 bits). Two pointers (prev and next) sum to 16 bytes overhead."
    },

    # Advanced Tier
    {
        "id": "a1",
        "tier": "Advanced",
        "question": "In a Circular Doubly Linked List (CDLL), what is HEAD.prev equal to?",
        "options": [
            "The TAIL node",
            "NULL",
            "HEAD itself",
            "Undefined"
        ],
        "answer_idx": 0,
        "explanation": "In a Circular Doubly Linked List, the backward ring wraps around from HEAD to TAIL: HEAD.prev == TAIL and TAIL.next == HEAD."
    },
    {
        "id": "a2",
        "tier": "Advanced",
        "question": "What invariant must be enforced during circular list traversal to prevent an infinite loop?",
        "options": [
            "Check either (curr == HEAD on subsequent steps) or cap loop count at list length",
            "Check if curr.next == NULL",
            "Check if node value is negative",
            "Check if curr.data == TAIL.data"
        ],
        "answer_idx": 0,
        "explanation": "Because a circular list has no NULL terminator, traversing without a cycle guard (or length counter) will loop infinitely."
    },
    {
        "id": "a3",
        "tier": "Advanced",
        "question": "What is the worst-case time complexity of searching an unbalanced Binary Search Tree?",
        "options": [
            "O(n) Linear Time (skewed degenerate tree equivalent to a linked list)",
            "O(log n) Strictly",
            "O(1) Constant",
            "O(n log n)"
        ],
        "answer_idx": 0,
        "explanation": "If elements are inserted in sorted order (e.g., 10, 20, 30, 40), an unbalanced BST degenerates into a linear linked list with O(n) height."
    },
    {
        "id": "a4",
        "tier": "Advanced",
        "question": "Which tree traversal visits BST nodes in monotonically increasing sorted order?",
        "options": [
            "In-Order Traversal (Left, Root, Right)",
            "Pre-Order Traversal",
            "Post-Order Traversal",
            "Level-Order Traversal (BFS)"
        ],
        "answer_idx": 0,
        "explanation": "By definition of a BST (left < root < right), recursive in-order traversal yields elements in strictly sorted order."
    }
]


class QuizView(tk.Frame):
    """Interactive quiz simulator with tier filtering, instant explanations, and scoring."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app

        self.filtered_questions = list(QUIZ_BANK)
        self.current_idx = 0
        self.score = 0
        self.answered_count = 0
        self.has_answered = False

        self._build_ui()
        self.load_question()

    def _build_ui(self):
        # 1. Top Filter & Score Header
        header = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=10)
        header.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(header, text="DIFFICULTY TIER:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 6))

        self.tier_btns = {}
        tiers = [("All", "all"), ("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")]
        for label, val in tiers:
            btn = tk.Button(
                header,
                text=label,
                bg=BLUE if val == "all" else BG_SURFACE,
                fg="#ffffff" if val == "all" else TEXT_MAIN,
                font=FONT_SMALL,
                relief=tk.FLAT,
                padx=10,
                pady=3,
                cursor="hand2",
                command=lambda v=val: self.filter_tier(v)
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.tier_btns[val] = btn

        # Right-side Score Counter
        self.lbl_score = tk.Label(header, text="Score: 0 / 0 (0%)", bg=BG_SURFACE, fg=CYAN, font=FONT_CODE_BOLD, padx=10, pady=3)
        self.lbl_score.pack(side=tk.RIGHT)

        # 2. Main Question Card
        card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=24, pady=20)
        card.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        # Question Metadata
        meta_row = tk.Frame(card, bg=BG_CARD)
        meta_row.pack(fill=tk.X, pady=(0, 6))

        self.lbl_q_num = tk.Label(meta_row, text="QUESTION 1 OF 14", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL)
        self.lbl_q_num.pack(side=tk.LEFT)

        self.lbl_tier_badge = tk.Label(meta_row, text="BEGINNER", bg=BG_SURFACE, fg=CYAN, font=FONT_SMALL, padx=8, pady=2)
        self.lbl_tier_badge.pack(side=tk.RIGHT)

        # Question Title
        self.lbl_question = tk.Label(card, text="Question text here...", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_TITLE, wraplength=760, justify=tk.LEFT)
        self.lbl_question.pack(anchor="w", pady=(8, 16))

        # Options Container
        self.options_container = tk.Frame(card, bg=BG_CARD)
        self.options_container.pack(fill=tk.X, pady=(0, 14))

        # Explanation Card (Revealed upon answering)
        self.exp_frame = tk.Frame(card, bg=BG_SURFACE, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=10)
        self.lbl_result_badge = tk.Label(self.exp_frame, text="CORRECT", bg=EMERALD, fg="#ffffff", font=FONT_SMALL, padx=6, pady=2)
        self.lbl_result_badge.pack(anchor="w", pady=(0, 4))
        self.lbl_explanation = tk.Label(self.exp_frame, text="Explanation text...", bg=BG_SURFACE, fg=TEXT_MAIN, font=FONT_BODY, wraplength=720, justify=tk.LEFT)
        self.lbl_explanation.pack(anchor="w")

        # Bottom Next Button
        self.btn_next = tk.Button(
            card,
            text="Next Question ▶",
            bg=BLUE,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.next_question
        )
        self.btn_next.pack(anchor="e", pady=(12, 0))

    def filter_tier(self, tier: str):
        for val, btn in self.tier_btns.items():
            btn.config(bg=BLUE if val == tier else BG_SURFACE, fg="#ffffff" if val == tier else TEXT_MAIN)

        if tier == "all":
            self.filtered_questions = list(QUIZ_BANK)
        else:
            self.filtered_questions = [q for q in QUIZ_BANK if q["tier"].lower() == tier.lower()]

        random.shuffle(self.filtered_questions)
        self.current_idx = 0
        self.score = 0
        self.answered_count = 0
        self.load_question()

    def load_question(self):
        if not self.filtered_questions:
            return

        self.has_answered = False
        self.exp_frame.pack_forget()
        self.btn_next.config(state=tk.DISABLED)

        q = self.filtered_questions[self.current_idx]
        total = len(self.filtered_questions)

        self.lbl_q_num.config(text=f"QUESTION {self.current_idx + 1} OF {total}")
        self.lbl_tier_badge.config(text=q["tier"].upper())
        self.lbl_question.config(text=q["question"])

        # Render options
        for widget in self.options_container.winfo_children():
            widget.destroy()

        self.option_buttons = []
        for i, opt in enumerate(q["options"]):
            btn = tk.Button(
                self.options_container,
                text=f"  {chr(65 + i)}.   {opt}",
                bg=BG_SURFACE,
                fg=TEXT_MAIN,
                font=FONT_BODY,
                relief=tk.FLAT,
                padx=14,
                pady=10,
                anchor="w",
                cursor="hand2",
                command=lambda idx=i: self.select_answer(idx)
            )
            btn.pack(fill=tk.X, pady=4)
            self.option_buttons.append(btn)

        pct = int((self.score / max(self.answered_count, 1)) * 100) if self.answered_count else 0
        self.lbl_score.config(text=f"Score: {self.score} / {self.answered_count} ({pct}%)")

    def select_answer(self, chosen_idx: int):
        if self.has_answered:
            return

        self.has_answered = True
        self.answered_count += 1
        q = self.filtered_questions[self.current_idx]
        correct_idx = q["answer_idx"]

        is_correct = (chosen_idx == correct_idx)
        if is_correct:
            self.score += 1
            self.option_buttons[chosen_idx].config(bg="#064e3b", fg="#ffffff")
            self.lbl_result_badge.config(text="✓ CORRECT!", bg=EMERALD)
        else:
            self.option_buttons[chosen_idx].config(bg="#4c0519", fg="#ffffff")
            self.option_buttons[correct_idx].config(bg="#064e3b", fg="#ffffff")
            self.lbl_result_badge.config(text="✗ INCORRECT", bg=ROSE)

        # Disable all option buttons
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)

        # Reveal explanation and enable next
        self.lbl_explanation.config(text=q["explanation"])
        self.exp_frame.pack(fill=tk.X, pady=(10, 0))
        self.btn_next.config(state=tk.NORMAL)

        pct = int((self.score / self.answered_count) * 100)
        self.lbl_score.config(text=f"Score: {self.score} / {self.answered_count} ({pct}%)")
        record_quiz_score(pct)

    def next_question(self):
        if self.current_idx < len(self.filtered_questions) - 1:
            self.current_idx += 1
            self.load_question()
        else:
            pct = int((self.score / self.answered_count) * 100)
            self.lbl_question.config(text=f"Quiz Completed!\nYour Final Score: {self.score} / {self.answered_count} ({pct}%)")
            for w in self.options_container.winfo_children():
                w.destroy()
            self.exp_frame.pack_forget()
            self.btn_next.config(text="Restart Quiz ↺", command=self.restart_quiz)

    def restart_quiz(self):
        self.btn_next.config(text="Next Question ▶", command=self.next_question)
        self.current_idx = 0
        self.score = 0
        self.answered_count = 0
        random.shuffle(self.filtered_questions)
        self.load_question()
