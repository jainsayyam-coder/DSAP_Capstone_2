"""
DSA Simulator - Home Dashboard View
Welcome Hero, Structure Launch Cards, and Core Learning Paths
"""

import tkinter as tk
from tkinter import ttk
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL
)
from gui.progress_manager import load_progress


class HomeView(tk.Frame):
    """Home Dashboard presenting project summary, quick-launch cards, and metrics."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app

        # Canvas container for scrollable home
        self.canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BG_DARK)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.bind("<Configure>", self._on_resize)
        self._build_ui()

    def _on_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width - 20)

    def _build_ui(self):
        # 1. Hero Card
        hero = tk.Frame(self.scroll_frame, bg="#111d33", highlightbackground=BORDER, highlightthickness=1, padx=25, pady=22)
        hero.pack(fill=tk.X, padx=20, pady=(15, 15))

        lbl_tag = tk.Label(hero, text="VIRTUAL DATA STRUCTURES LABORATORY • CAPSTONE EDITION", bg="#1e2f50", fg=CYAN, font=FONT_SMALL, padx=8, pady=3)
        lbl_tag.pack(anchor="w", pady=(0, 8))

        lbl_title = tk.Label(hero, text="DSA Interactive Learning Simulator", bg="#111d33", fg=TEXT_MAIN, font=FONT_TITLE)
        lbl_title.pack(anchor="w")

        lbl_desc = tk.Label(
            hero,
            text="Master dynamic pointer mechanics, memory allocation, circular loopbacks, bidirectional traversals,\nand binary trees with real-time vector animations and synchronized step-by-step algorithms.",
            bg="#111d33",
            fg=TEXT_MUTED,
            font=FONT_BODY,
            justify=tk.LEFT
        )
        lbl_desc.pack(anchor="w", pady=(6, 16))

        # Hero Action Buttons
        btn_bar = tk.Frame(hero, bg="#111d33")
        btn_bar.pack(anchor="w")

        tk.Button(
            btn_bar,
            text="🚀 Open Linked List Lab",
            bg=BLUE,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.app.switch_tab("simulator")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_bar,
            text="🌳 Binary Search Tree Lab",
            bg=EMERALD,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.app.switch_tab("tree")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_bar,
            text="🎓 Step-by-Step Study Mode",
            bg=PURPLE,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.app.switch_tab("study")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_bar,
            text="📝 Take Knowledge Quiz",
            bg=BG_SURFACE,
            fg=TEXT_MAIN,
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.app.switch_tab("quiz")
        ).pack(side=tk.LEFT)

        # 2. Key Metrics Bar
        self.metrics_bar = tk.Frame(self.scroll_frame, bg=BG_DARK)
        self.metrics_bar.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.refresh_metrics()

        # 3. Four Core Linked List Architecture Cards
        sec_title = tk.Label(self.scroll_frame, text="Four Core Linked List Implementations", bg=BG_DARK, fg=TEXT_MAIN, font=FONT_HEADING)
        sec_title.pack(anchor="w", padx=20, pady=(5, 10))

        grid = tk.Frame(self.scroll_frame, bg=BG_DARK)
        grid.pack(fill=tk.X, padx=20, pady=(0, 15))
        grid.columnconfigure((0, 1), weight=1, uniform="group1")

        # Card 1: Singly
        c1 = self._create_structure_card(
            grid,
            title="Singly Linked List (SLL)",
            tag="UNIDIRECTIONAL",
            color=CYAN,
            desc="Chain of nodes containing data and single forward NEXT pointer. Terminates at NULL.\nO(1) head insertion, O(n) tail deletion paradox.",
            action_text="Simulate SLL →",
            command=lambda: self._select_type_and_go("singly")
        )
        c1.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        # Card 2: Doubly
        c2 = self._create_structure_card(
            grid,
            title="Doubly Linked List (DLL)",
            tag="BIDIRECTIONAL",
            color=PURPLE,
            desc="Dual-pointer nodes with PREV and NEXT links. Allows backward traversal.\nEnables true O(1) tail deletion via tail.prev without walking from head.",
            action_text="Simulate DLL →",
            command=lambda: self._select_type_and_go("doubly")
        )
        c2.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        # Card 3: Circular Singly
        c3 = self._create_structure_card(
            grid,
            title="Circular Singly (CSLL)",
            tag="CONTINUOUS RING",
            color=EMERALD,
            desc="Unbroken loop where tail.next connects back to HEAD. Zero NULL pointers.\nSafe traversal requires cycle guards to avoid infinite execution.",
            action_text="Simulate CSLL →",
            command=lambda: self._select_type_and_go("circular-singly")
        )
        c3.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")

        # Card 4: Circular Doubly
        c4 = self._create_structure_card(
            grid,
            title="Circular Doubly (CDLL)",
            tag="DUAL-RING TOPOLOGY",
            color=AMBER,
            desc="Maximum pointer flexibility: tail.next == HEAD and HEAD.prev == TAIL.\nInstant O(1) round-trip navigation from any node in both directions.",
            action_text="Simulate CDLL →",
            command=lambda: self._select_type_and_go("circular-doubly")
        )
        c4.grid(row=1, column=1, padx=6, pady=6, sticky="nsew")

        # 4. Intuition Callout (Arrays vs Linked Lists)
        callout = tk.Frame(self.scroll_frame, bg=BG_CARD, highlightbackground=BLUE, highlightthickness=1, padx=18, pady=14)
        callout.pack(fill=tk.X, padx=20, pady=(5, 20))

        tk.Label(callout, text="💡 Core Intuition: Contiguous Arrays vs Dynamic Linked Lists", bg=BG_CARD, fg=CYAN, font=FONT_SUBHEADING).pack(anchor="w")
        tk.Label(
            callout,
            text="Unlike arrays which occupy a continuous, pre-allocated block of RAM, linked lists allocate memory dynamically on the heap\nfor individual nodes as needed. This grants effortless O(1) insertions at the head without memory shifts, at the tradeoff of\nrequiring sequential O(n) traversals to access arbitrary positions by index.",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=FONT_BODY,
            justify=tk.LEFT
        ).pack(anchor="w", pady=(4, 0))

    def _create_structure_card(self, parent, title, tag, color, desc, action_text, command):
        card = tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=14)
        top_row = tk.Frame(card, bg=BG_CARD)
        top_row.pack(fill=tk.X, pady=(0, 6))

        tk.Label(top_row, text=title, bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(side=tk.LEFT)
        tk.Label(top_row, text=tag, bg=BG_SURFACE, fg=color, font=FONT_SMALL, padx=6, pady=2).pack(side=tk.RIGHT)

        tk.Label(card, text=desc, bg=BG_CARD, fg=TEXT_MUTED, font=FONT_BODY, justify=tk.LEFT).pack(anchor="w", pady=(0, 12))

        tk.Button(
            card,
            text=action_text,
            bg=BG_SURFACE,
            fg=color,
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=command
        ).pack(anchor="w")

        return card

    def _select_type_and_go(self, l_type: str):
        if hasattr(self.app, "views") and "simulator" in self.app.views:
            self.app.views["simulator"].set_list_type(l_type)
        self.app.switch_tab("simulator")

    def refresh_metrics(self):
        for widget in self.metrics_bar.winfo_children():
            widget.destroy()

        prog = load_progress()
        ops = prog.get("operations_executed", 0)
        best_quiz = prog.get("quiz_best_score", 0)
        chals = len(prog.get("challenges_solved", []))

        self.metrics_bar.columnconfigure((0, 1, 2, 3), weight=1)

        def _metric_box(col, val, label, color):
            box = tk.Frame(self.metrics_bar, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=10)
            box.grid(row=0, column=col, padx=5, sticky="nsew")
            tk.Label(box, text=str(val), bg=BG_CARD, fg=color, font=("Segoe UI", 16, "bold")).pack()
            tk.Label(box, text=label, bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack()

        _metric_box(0, f"{ops}", "Operations Executed", CYAN)
        _metric_box(1, f"{best_quiz}%", "Best Quiz Accuracy", EMERALD)
        _metric_box(2, f"{chals} / 8", "Challenges Solved", PURPLE)
        _metric_box(3, "100% Offline", "Zero Remote Telemetry", BLUE)
