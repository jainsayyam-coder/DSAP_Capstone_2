"""
DSA Simulator - Practice Challenge Mode View
8 Interactive Algorithmic Puzzles with multi-tier hints and automated verification.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
from gui.visualizer_canvas import VisualizerCanvas
from gui.progress_manager import record_challenge, load_progress
import backend.linked_list as ll_backend

CHALLENGES = [
    {
        "id": "chal_insert_pos",
        "title": "1. Insert at Position 3",
        "tier": "Beginner",
        "type": "singly",
        "initial": [10, 20, 30, 40, 50],
        "instr": "Insert the value 99 at index 3 of the Singly Linked List.",
        "hints": [
            "Hint 1: Indexing is 0-based. Index 3 is the 4th element in the chain.",
            "Hint 2: Walk to index 2 (predecessor node 30), then splice the new node 99 before 40.",
            "Hint 3: Use the 'Insert at Pos' button with Value = 99 and Index = 3."
        ],
        "validator": lambda lst: len(lst) >= 4 and lst.to_list()[3] == 99
    },
    {
        "id": "chal_delete_val",
        "title": "2. Delete Specified Value",
        "tier": "Beginner",
        "type": "singly",
        "initial": [10, 20, 99, 40, 50],
        "instr": "Delete the node with value 99 from the list without breaking the chain.",
        "hints": [
            "Hint 1: Search for 99 first to locate its 0-based index (index 2).",
            "Hint 2: Connect node 20's next pointer directly to node 40.",
            "Hint 3: Use 'Delete at Pos' with Index = 2."
        ],
        "validator": lambda lst: 99 not in lst.to_list() and len(lst) == 4
    },
    {
        "id": "chal_reverse_sll",
        "title": "3. Reverse a Singly Linked List",
        "tier": "Intermediate",
        "type": "singly",
        "initial": [1, 2, 3, 4, 5],
        "instr": "Invert all next pointers so that [1, 2, 3, 4, 5] becomes [5, 4, 3, 2, 1].",
        "hints": [
            "Hint 1: Three pointers (prev, curr, nextTemp) are needed for in-place reversal.",
            "Hint 2: Each node's next link must be made to point backward to its predecessor.",
            "Hint 3: Click the 'Reverse List' button to execute the three-pointer reversal."
        ],
        "validator": lambda lst: lst.to_list() == [5, 4, 3, 2, 1]
    },
    {
        "id": "chal_find_middle",
        "title": "4. Find the Middle Node (Tortoise & Hare)",
        "tier": "Intermediate",
        "type": "singly",
        "initial": [10, 20, 30, 40, 50],
        "instr": "Identify the midpoint node value (for an odd list of 5 nodes, the middle is index 2, value 30).",
        "hints": [
            "Hint 1: Tortoise advances 1 node per cycle, Hare advances 2 nodes.",
            "Hint 2: For length 5, floor(5/2) = 2, which corresponds to value 30.",
            "Hint 3: Search for value 30 to highlight the midpoint."
        ],
        "validator": lambda lst: len(lst) > 0 and lst.to_list()[len(lst) // 2] == 30
    },
    {
        "id": "chal_circular_link",
        "title": "5. Verify Circular Linkage",
        "tier": "Intermediate",
        "type": "circular-singly",
        "initial": [10, 20, 30],
        "instr": "Append value 40 to the circular list and confirm that TAIL.next points back to HEAD.",
        "hints": [
            "Hint 1: In a circular singly list, the last node's NEXT pointer never equals NULL.",
            "Hint 2: Insert value 40 at the end (tail).",
            "Hint 3: Verify that TAIL.next is the HEAD node with value 10."
        ],
        "validator": lambda lst: len(lst) == 4 and lst.tail and lst.tail.next == lst.head and lst.tail.value == 40
    },
    {
        "id": "chal_dll_deletion",
        "title": "6. Doubly Linked List Two-Way Deletion",
        "tier": "Advanced",
        "type": "doubly",
        "initial": [100, 200, 300, 400],
        "instr": "Delete the tail node in O(1) time utilizing the backward PREV pointer.",
        "hints": [
            "Hint 1: In DLL, tail.prev is immediately accessible in O(1) without scanning from head.",
            "Hint 2: Set TAIL = TAIL.prev, then set new TAIL.next = NULL.",
            "Hint 3: Click 'Delete from End'."
        ],
        "validator": lambda lst: len(lst) == 3 and lst.tail and lst.tail.value == 300 and lst.tail.next is None
    },
    {
        "id": "chal_cycle_detect",
        "title": "7. Detect a Cycle (Floyd's Algorithm)",
        "tier": "Advanced",
        "type": "circular-singly",
        "initial": [5, 15, 25, 35],
        "instr": "Confirm whether the active structure contains an unbroken cyclic loop.",
        "hints": [
            "Hint 1: Floyd's cycle detection checks whether fast and slow pointers eventually meet.",
            "Hint 2: Circular Singly Linked Lists possess a cycle by architectural design.",
            "Hint 3: Verify the circular loopback arc on the canvas."
        ],
        "validator": lambda lst: lst.tail is not None and lst.tail.next == lst.head
    },
    {
        "id": "chal_merge_sorted",
        "title": "8. Merge Two Sorted Lists",
        "tier": "Advanced",
        "type": "singly",
        "initial": [10, 30, 50],
        "instr": "Merge elements [20, 40, 60] into the sorted list [10, 30, 50] to produce [10, 20, 30, 40, 50, 60].",
        "hints": [
            "Hint 1: Insert 20 at index 1.",
            "Hint 2: Insert 40 at index 3, and 60 at the end.",
            "Hint 3: All elements must be in monotonically ascending order."
        ],
        "validator": lambda lst: lst.to_list() == [10, 20, 30, 40, 50, 60]
    }
]


class ChallengesView(tk.Frame):
    """Practice Challenges View with automated solution verification and hint drawer."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self.current_chal_idx = 0
        self.revealed_hints = 0
        self.live_list = None

        self._build_ui()
        self.load_challenge(0)

    def _build_ui(self):
        # 1. Top Challenge Selector Bar
        top_bar = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=8)
        top_bar.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(top_bar, text="SELECT CHALLENGE:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 6))

        self.combo_chal = ttk.Combobox(
            top_bar,
            values=[c["title"] for c in CHALLENGES],
            state="readonly",
            width=32
        )
        self.combo_chal.current(0)
        self.combo_chal.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_chal.bind("<<ComboboxSelected>>", lambda e: self.load_challenge(self.combo_chal.current()))

        self.btn_hint = tk.Button(
            top_bar,
            text="💡 Reveal Hint (0/3)",
            bg=BG_SURFACE,
            fg=AMBER,
            font=FONT_SMALL,
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.reveal_next_hint
        )
        self.btn_hint.pack(side=tk.LEFT, padx=4)

        # Verification Buttons on Right
        tk.Button(
            top_bar,
            text="✓ Check Solution",
            bg=EMERALD,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=14,
            pady=3,
            cursor="hand2",
            command=self.verify_solution
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            top_bar,
            text="↺ Reset",
            bg=BG_SURFACE,
            fg=TEXT_MAIN,
            font=FONT_SMALL,
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=lambda: self.load_challenge(self.current_chal_idx)
        ).pack(side=tk.RIGHT)

        # 2. Main Workspace
        workspace = tk.Frame(self, bg=BG_DARK)
        workspace.pack(fill=tk.BOTH, expand=True, padx=14, pady=0)

        # Left Column: Canvas & Status
        left_col = tk.Frame(workspace, bg=BG_DARK)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Instructions Banner
        instr_card = tk.Frame(left_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=10)
        instr_card.pack(fill=tk.X, pady=(0, 6))

        self.lbl_chal_title = tk.Label(instr_card, text="Challenge Title", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_HEADING)
        self.lbl_chal_title.pack(anchor="w")

        self.lbl_chal_instr = tk.Label(instr_card, text="Task instructions...", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_BODY, wraplength=700, justify=tk.LEFT)
        self.lbl_chal_instr.pack(anchor="w", pady=(2, 0))

        # Hint Drawer (Hidden initially)
        self.hint_drawer = tk.Frame(left_col, bg="#271d0c", highlightbackground=AMBER, highlightthickness=1, padx=12, pady=8)
        self.lbl_hint_text = tk.Label(self.hint_drawer, text="", bg="#271d0c", fg=GOLD, font=FONT_BODY, wraplength=700, justify=tk.LEFT)
        self.lbl_hint_text.pack(anchor="w")

        # Visualizer Canvas
        self.visualizer = VisualizerCanvas(left_col)
        self.visualizer.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Bottom Feedback Bar
        feedback_bar = tk.Frame(left_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=6)
        feedback_bar.pack(fill=tk.X, pady=(4, 0))

        self.feedback_dot = tk.Label(feedback_bar, text="●", bg=BG_CARD, fg=CYAN, font=FONT_HEADING)
        self.feedback_dot.pack(side=tk.LEFT, padx=(0, 6))

        self.feedback_text = tk.Label(feedback_bar, text="Perform the required operation using controls on the right.", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_BODY)
        self.feedback_text.pack(side=tk.LEFT)

        # Right Column: Interactive Operations
        ops_panel = tk.Frame(workspace, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, width=240, padx=12, pady=12)
        ops_panel.pack(side=tk.RIGHT, fill=tk.Y)
        ops_panel.pack_propagate(False)

        tk.Label(ops_panel, text="CHALLENGE CONTROLS", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(anchor="w", pady=(0, 8))

        # Inputs
        tk.Label(ops_panel, text="Value:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")
        self.entry_val = tk.Entry(ops_panel, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT)
        self.entry_val.insert(0, "99")
        self.entry_val.pack(fill=tk.X, pady=(2, 6))

        tk.Label(ops_panel, text="Index (0..N):", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")
        self.entry_pos = tk.Entry(ops_panel, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT)
        self.entry_pos.insert(0, "3")
        self.entry_pos.pack(fill=tk.X, pady=(2, 10))

        # Action Buttons
        self._action_btn(ops_panel, "➕ Insert Beginning", self.chal_insert_beg)
        self._action_btn(ops_panel, "➕ Insert End", self.chal_insert_end)
        self._action_btn(ops_panel, "➕ Insert at Index", self.chal_insert_at)
        self._action_btn(ops_panel, "− Delete Beginning", self.chal_delete_beg, color=ROSE)
        self._action_btn(ops_panel, "− Delete End", self.chal_delete_end, color=ROSE)
        self._action_btn(ops_panel, "− Delete at Index", self.chal_delete_at, color=ROSE)
        self._action_btn(ops_panel, "↶ Reverse List", self.chal_reverse, color=PURPLE)

    def _action_btn(self, parent, text, cmd, color=BG_SURFACE):
        btn = tk.Button(
            parent,
            text=text,
            bg=color,
            fg="#ffffff" if color == ROSE else TEXT_MAIN,
            font=FONT_BODY,
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            anchor="w",
            command=cmd
        )
        btn.pack(fill=tk.X, pady=2)
        return btn

    def load_challenge(self, idx: int):
        self.current_chal_idx = idx
        chal = CHALLENGES[idx]
        self.combo_chal.current(idx)

        self.lbl_chal_title.config(text=f"{chal['title']}  [{chal['tier'].upper()}]")
        self.lbl_chal_instr.config(text=chal["instr"])

        self.revealed_hints = 0
        self.btn_hint.config(text="💡 Reveal Hint (0/3)")
        self.hint_drawer.pack_forget()

        # Instantiate fresh list
        self.live_list = ll_backend.create_list(chal["type"])
        for v in chal["initial"]:
            self.live_list.insert_end(v)

        self.refresh_canvas()
        self.set_feedback("Challenge loaded. Modify the list to meet the target criteria.", ok=True)

    def refresh_canvas(self, highlight=-1):
        chal = CHALLENGES[self.current_chal_idx]
        items = self.live_list.to_list()
        self.visualizer.render_linked_list(
            items=items,
            list_type=chal["type"],
            highlight_index=highlight
        )

    def set_feedback(self, msg: str, ok: bool = True):
        self.feedback_text.config(text=msg)
        self.feedback_dot.config(fg=EMERALD if ok else ROSE)

    def reveal_next_hint(self):
        chal = CHALLENGES[self.current_chal_idx]
        hints = chal.get("hints", [])
        if self.revealed_hints < len(hints):
            self.revealed_hints += 1
            all_revealed = "\n\n".join(hints[:self.revealed_hints])
            self.lbl_hint_text.config(text=all_revealed)
            self.hint_drawer.pack(fill=tk.X, pady=(0, 6))
            self.btn_hint.config(text=f"💡 Reveal Hint ({self.revealed_hints}/{len(hints)})")
        else:
            messagebox.showinfo("Hints", "All available hints for this challenge are already revealed.")

    def verify_solution(self):
        chal = CHALLENGES[self.current_chal_idx]
        is_passed = chal["validator"](self.live_list)

        if is_passed:
            record_challenge(chal["id"])
            self.set_feedback(f"🎉 CHALLENGE PASSED! Successfully solved '{chal['title']}'.", ok=True)
            messagebox.showinfo("Challenge Complete", f"Congratulations! You verified the solution for:\n{chal['title']}")
        else:
            self.set_feedback("Validation failed. Current list does not satisfy the challenge requirements. Review the hints!", ok=False)

    # Operations
    def _val(self):
        return int(self.entry_val.get().strip() or "0")

    def _pos(self):
        return int(self.entry_pos.get().strip() or "0")

    def chal_insert_beg(self):
        self.live_list.insert_beginning(self._val())
        self.refresh_canvas(highlight=0)

    def chal_insert_end(self):
        self.live_list.insert_end(self._val())
        self.refresh_canvas(highlight=len(self.live_list) - 1)

    def chal_insert_at(self):
        pos = self._pos()
        self.live_list.insert_at(self._val(), pos)
        self.refresh_canvas(highlight=pos)

    def chal_delete_beg(self):
        self.live_list.delete_beginning()
        self.refresh_canvas()

    def chal_delete_end(self):
        self.live_list.delete_end()
        self.refresh_canvas()

    def chal_delete_at(self):
        self.live_list.delete_at(self._pos())
        self.refresh_canvas()

    def chal_reverse(self):
        if hasattr(self.live_list, "reverse"):
            self.live_list.reverse()
            self.refresh_canvas()
        else:
            self.set_feedback("Reverse not supported on this list type.", ok=False)
