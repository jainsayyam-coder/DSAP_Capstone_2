"""
DSA Simulator - Time & Space Complexity Matrix View
Pedagogical comparison across all 4 linked list types, arrays, stack, queue, and BST.
"""

import tkinter as tk
from tkinter import ttk
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE_BOLD
)

COMPLEXITY_DATA = [
    ("Access by Index", "O(1) Direct", "O(n) Sequential", "O(n) Sequential", "O(n) Sequential", "O(n) Sequential", "O(log n) avg"),
    ("Search Value", "O(n) Scan", "O(n) Linear", "O(n) Linear", "O(n) Linear", "O(n) Linear", "O(log n) avg"),
    ("Insert Beginning", "O(n) Shift", "O(1) Relink", "O(1) Relink", "O(1) Relink", "O(1) Relink", "O(log n) avg"),
    ("Insert End (with Tail)", "O(1)* Amortized", "O(1) Relink", "O(1) Relink", "O(1) Relink", "O(1) Relink", "O(log n) avg"),
    ("Delete Beginning", "O(n) Shift", "O(1) Head Adv", "O(1) Head Adv", "O(1) Head Adv", "O(1) Head Adv", "O(log n) avg"),
    ("Delete End (with Tail)", "O(1) Constant", "O(n) Walk Head", "O(1) tail.prev", "O(n) Walk Head", "O(1) tail.prev", "O(log n) avg"),
    ("Insert/Delete at pos k", "O(n) Shift", "O(k) Walk", "O(min(k,n-k))", "O(k) Walk", "O(min(k,n-k))", "O(log n) avg"),
    ("Auxiliary Space", "O(1) In-Place", "O(1) In-Place", "O(1) In-Place", "O(1) In-Place", "O(1) In-Place", "O(1) In-Place"),
    ("Pointer Overhead/Node", "0 Bytes", "8 Bytes (1 ptr)", "16 Bytes (2 ptr)", "8 Bytes (1 ptr)", "16 Bytes (2 ptr)", "16 Bytes (L/R)")
]


class ComplexityView(tk.Frame):
    """Comparative complexity table with color-coded asymptotic performance ratings."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=14)
        header.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(header, text="ASYMPTOTIC COMPLEXITY COMPARISON MATRIX", bg=BG_CARD, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        tk.Label(header, text="Time & Space Complexity Across Data Structures", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_HEADING).pack(anchor="w")
        tk.Label(
            header,
            text="Observe how explicit memory pointers convert expensive array array-shift operations into instant O(1) pointer swaps,\nand why predecessor access is the key determinant for constant-time tail deletion.",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=FONT_BODY,
            justify=tk.LEFT
        ).pack(anchor="w", pady=(4, 0))

        # 2. Main Matrix Card
        table_card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12)
        table_card.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        # Table Header Row
        headers = ["Operation", "Dynamic Array", "Singly (SLL)", "Doubly (DLL)", "Circular Singly", "Circular Doubly", "Binary Search Tree"]
        header_row = tk.Frame(table_card, bg=BG_SURFACE, padx=8, pady=8)
        header_row.pack(fill=tk.X)

        for col_idx, h_text in enumerate(headers):
            w = 18 if col_idx == 0 else 14
            tk.Label(
                header_row,
                text=h_text,
                bg=BG_SURFACE,
                fg=CYAN if col_idx == 0 else TEXT_MAIN,
                font=FONT_SUBHEADING,
                width=w,
                anchor="w"
            ).pack(side=tk.LEFT, padx=3)

        # Table Rows
        for row_idx, row in enumerate(COMPLEXITY_DATA):
            bg_col = BG_INPUT if row_idx % 2 == 0 else BG_CARD
            row_frame = tk.Frame(table_card, bg=bg_col, padx=8, pady=6)
            row_frame.pack(fill=tk.X)

            op_name = row[0]
            tk.Label(row_frame, text=op_name, bg=bg_col, fg=TEXT_MAIN, font=FONT_BODY_BOLD, width=18, anchor="w").pack(side=tk.LEFT, padx=3)

            for col_val in row[1:]:
                # Color code cell badge
                if "O(1)" in col_val and "O(n)" not in col_val:
                    fg_col = EMERALD
                elif "O(log n)" in col_val:
                    fg_col = CYAN
                elif "O(n)" in col_val or "Shift" in col_val:
                    fg_col = AMBER if "Walk" in col_val else ROSE
                else:
                    fg_col = TEXT_MUTED

                tk.Label(row_frame, text=col_val, bg=bg_col, fg=fg_col, font=FONT_CODE_BOLD, width=14, anchor="w").pack(side=tk.LEFT, padx=3)

        # 3. The Paradox Deep-Dive Callout Card
        callout = tk.Frame(self, bg=BG_SURFACE, highlightbackground=AMBER, highlightthickness=1, padx=16, pady=12)
        callout.pack(fill=tk.X, padx=14, pady=(0, 14))

        tk.Label(callout, text="💡 The 'Delete Tail' Paradox Explained", bg=BG_SURFACE, fg=AMBER, font=FONT_SUBHEADING).pack(anchor="w")
        tk.Label(
            callout,
            text="A frequent misconception is that maintaining a TAIL pointer makes deleting from the end O(1) in a Singly Linked List.\n"
                 "It does NOT! To delete the tail, you must set tail = second_to_last_node and second_to_last_node.next = NULL.\n"
                 "Because SLL nodes only point forward, you cannot step backward from TAIL; you are forced to traverse n nodes from HEAD.\n"
                 "This is the primary motivation for Doubly Linked Lists: tail.prev is immediately available, making tail deletion O(1)!",
            bg=BG_SURFACE,
            fg=TEXT_MAIN,
            font=FONT_BODY,
            justify=tk.LEFT
        ).pack(anchor="w", pady=(4, 0))
