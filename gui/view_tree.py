"""
DSA Simulator - Binary Search Tree (BST) Laboratory View
Visual tree growth, node allocations, and step-by-step tree traversals (Inorder, Preorder, Postorder, BFS).
"""

import tkinter as tk
from tkinter import ttk
import random
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
from gui.visualizer_canvas import VisualizerCanvas
from backend.bst import BinarySearchTree
from gui.progress_manager import record_operation


class TreeView(tk.Frame):
    """Binary Search Tree Laboratory with automated layout and animated traversals."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self.bst = BinarySearchTree()

        # Seed with balanced initial nodes [50, 25, 75, 15, 35, 60, 85]
        for v in [50, 25, 75, 15, 35, 60, 85]:
            self.bst.insert(v)

        self._build_ui()
        self.refresh_tree()

    def _build_ui(self):
        # 1. Top Controls Bar
        ctrl_bar = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=10)
        ctrl_bar.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(ctrl_bar, text="Value:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 4))
        self.entry_val = tk.Entry(ctrl_bar, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT, width=8)
        self.entry_val.insert(0, "45")
        self.entry_val.pack(side=tk.LEFT, padx=(0, 10))

        # Basic Operations
        self._action_btn(ctrl_bar, "➕ Insert", BLUE, self.op_insert)
        self._action_btn(ctrl_bar, "− Delete", ROSE, self.op_delete)
        self._action_btn(ctrl_bar, "🔍 Search", BG_SURFACE, self.op_search)
        self._action_btn(ctrl_bar, "⬇ Min", BG_SURFACE, self.op_find_min)
        self._action_btn(ctrl_bar, "⬆ Max", BG_SURFACE, self.op_find_max)

        # Separator
        tk.Frame(ctrl_bar, bg=BORDER, width=1, height=20).pack(side=tk.LEFT, padx=10)

        # Presets
        self._action_btn(ctrl_bar, "🎲 Random Tree", BG_SURFACE, self.op_random)
        self._action_btn(ctrl_bar, "✕ Clear", BG_SURFACE, self.op_clear)

        # Right-side tree metrics
        self.metrics_label = tk.Label(ctrl_bar, text="Nodes: 7 | Height: 3", bg=BG_SURFACE, fg=CYAN, font=FONT_CODE_BOLD, padx=8, pady=3)
        self.metrics_label.pack(side=tk.RIGHT)

        # 2. Main Area (Canvas + Traversals Panel)
        workspace = tk.Frame(self, bg=BG_DARK)
        workspace.pack(fill=tk.BOTH, expand=True, padx=14, pady=0)

        # Left: Canvas
        canvas_col = tk.Frame(workspace, bg=BG_DARK)
        canvas_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Visualizer Canvas
        self.visualizer = VisualizerCanvas(canvas_col, on_node_click=self.on_node_clicked)
        self.visualizer.pack(fill=tk.BOTH, expand=True)

        # Bottom Status Bar
        status_bar = tk.Frame(canvas_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=6)
        status_bar.pack(fill=tk.X, pady=(4, 0))

        self.status_dot = tk.Label(status_bar, text="●", bg=BG_CARD, fg=EMERALD, font=FONT_HEADING)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 6))

        self.status_text = tk.Label(status_bar, text="BST ready. Insert values or trigger an animated traversal.", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_BODY)
        self.status_text.pack(side=tk.LEFT)

        # Right: Traversals Panel
        trav_panel = tk.Frame(workspace, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, width=260, padx=14, pady=12)
        trav_panel.pack(side=tk.RIGHT, fill=tk.Y)
        trav_panel.pack_propagate(False)

        tk.Label(trav_panel, text="TREE TRAVERSALS", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(anchor="w", pady=(0, 8))
        tk.Label(trav_panel, text="Step through nodes in rigorous mathematical order:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL, wraplength=230, justify=tk.LEFT).pack(anchor="w", pady=(0, 10))

        self._trav_btn(trav_panel, "In-Order (L, Root, R)", EMERALD, "inorder", "Visits values in ascending sorted order.")
        self._trav_btn(trav_panel, "Pre-Order (Root, L, R)", CYAN, "preorder", "Useful for tree serialization / cloning.")
        self._trav_btn(trav_panel, "Post-Order (L, R, Root)", PURPLE, "postorder", "Useful for bottom-up node deletions.")
        self._trav_btn(trav_panel, "Level-Order (BFS)", AMBER, "levelorder", "Breadth-first search level by level.")

        # Traversal Output Card
        tk.Label(trav_panel, text="TRAVERSAL OUTPUT:", bg=BG_CARD, fg=CYAN, font=FONT_SMALL).pack(anchor="w", pady=(14, 4))
        self.txt_trav_output = tk.Text(trav_panel, bg=BG_INPUT, fg=TEXT_MAIN, font=FONT_CODE_BOLD, relief=tk.FLAT, padx=8, pady=8, height=4, wrap=tk.WORD)
        self.txt_trav_output.pack(fill=tk.X)
        self.txt_trav_output.insert(tk.END, "No traversal executed yet.")
        self.txt_trav_output.config(state=tk.DISABLED)

    def _action_btn(self, parent, text, color, cmd):
        btn = tk.Button(
            parent,
            text=text,
            bg=color,
            fg="#ffffff" if color in (BLUE, ROSE) else TEXT_MAIN,
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=9,
            pady=3,
            cursor="hand2",
            command=cmd
        )
        btn.pack(side=tk.LEFT, padx=3)
        return btn

    def _trav_btn(self, parent, title, color, order, desc):
        card = tk.Frame(parent, bg=BG_SURFACE, highlightbackground=BORDER, highlightthickness=1, padx=8, pady=8)
        card.pack(fill=tk.X, pady=4)
        tk.Button(
            card,
            text=f"▶ {title}",
            bg=color,
            fg="#000000" if color in (CYAN, AMBER, EMERALD) else "#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=6,
            pady=3,
            cursor="hand2",
            command=lambda: self.run_traversal(order)
        ).pack(anchor="w", fill=tk.X)
        tk.Label(card, text=desc, bg=BG_SURFACE, fg=TEXT_MUTED, font=FONT_SMALL, justify=tk.LEFT, wraplength=220).pack(anchor="w", pady=(4, 0))

    def _parse_val(self) -> int:
        val_str = self.entry_val.get().strip()
        if not val_str:
            raise ValueError("Enter an integer value.")
        try:
            return int(val_str)
        except ValueError:
            raise ValueError(f"'{val_str}' is not a valid integer.")

    def refresh_tree(self, visited=None, curr=None):
        self.visualizer.render_bst(self.bst, visited_nodes=visited, current_node_val=curr)
        h = self.bst.get_height()
        n = len(self.bst)
        self.metrics_label.config(text=f"Nodes: {n} | Height: {h}")

    def set_status(self, msg: str, ok: bool = True):
        self.status_text.config(text=msg)
        self.status_dot.config(fg=EMERALD if ok else ROSE)

    # =========================================================================
    # BST Operations
    # =========================================================================
    def op_insert(self):
        try:
            val = self._parse_val()
            ok = self.bst.insert(val)
            if ok:
                record_operation()
                self.refresh_tree(curr=val)
                self.set_status(f"Inserted value {val} into BST.", ok=True)
            else:
                self.set_status(f"Value {val} already exists. Duplicates are disallowed in BST.", ok=False)
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_delete(self):
        try:
            val = self._parse_val()
            ok = self.bst.delete(val)
            if ok:
                record_operation()
                self.refresh_tree()
                self.set_status(f"Deleted value {val} from BST.", ok=True)
            else:
                self.set_status(f"Value {val} was not found in BST.", ok=False)
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_search(self):
        try:
            val = self._parse_val()
            node = self.bst.search(val)
            record_operation()
            if node:
                self.refresh_tree(curr=val)
                self.set_status(f"Found {val} in BST at heap address {node.address}!", ok=True)
            else:
                self.refresh_tree()
                self.set_status(f"Value {val} not found in BST.", ok=False)
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_find_min(self):
        m = self.bst.find_min()
        if m:
            self.refresh_tree(curr=m.value)
            self.set_status(f"Minimum value in BST: {m.value}", ok=True)
        else:
            self.set_status("Tree is empty.", ok=False)

    def op_find_max(self):
        m = self.bst.find_max()
        if m:
            self.refresh_tree(curr=m.value)
            self.set_status(f"Maximum value in BST: {m.value}", ok=True)
        else:
            self.set_status("Tree is empty.", ok=False)

    def op_random(self):
        self.bst.clear()
        samples = random.sample(range(10, 99), random.randint(5, 9))
        for v in samples:
            self.bst.insert(v)
        self.refresh_tree()
        self.set_status(f"Generated new BST from random values: {samples}.", ok=True)

    def op_clear(self):
        self.bst.clear()
        self.refresh_tree()
        self.set_status("Cleared entire tree.", ok=True)

    # =========================================================================
    # Animated Traversals
    # =========================================================================
    def run_traversal(self, order: str):
        if not self.bst.root:
            self.set_status("Cannot traverse an empty tree.", ok=False)
            return

        steps = self.bst.trace_traversal(order)
        record_operation()

        def _step_anim(idx):
            if idx < len(steps):
                st = steps[idx]
                curr_val = st["node"].value if st["node"] else None
                visited = st["visited"]

                self.refresh_tree(visited=visited, curr=curr_val)
                self.set_status(f"[{order.upper()}] {st['action']}", ok=True)

                # Update output box
                self.txt_trav_output.config(state=tk.NORMAL)
                self.txt_trav_output.delete("1.0", tk.END)
                self.txt_trav_output.insert(tk.END, " -> ".join(map(str, visited)))
                self.txt_trav_output.config(state=tk.DISABLED)

                self.after(350, lambda: _step_anim(idx + 1))
            else:
                self.set_status(f"{order.upper()} Traversal complete!", ok=True)

        _step_anim(0)

    # =========================================================================
    # Node Click Inspector
    # =========================================================================
    def on_node_clicked(self, node_data):
        popup = tk.Toplevel(self)
        popup.title(f"BST Node — Value {node_data['value']}")
        popup.geometry("340x240")
        popup.configure(bg=BG_CARD)
        popup.resizable(False, False)

        header = tk.Frame(popup, bg=BG_SURFACE, padx=12, pady=8)
        header.pack(fill=tk.X)
        tk.Label(header, text="🌳 BST NODE INSPECTION", bg=BG_SURFACE, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        tk.Label(header, text=f"Value: {node_data['value']}", bg=BG_SURFACE, fg=TEXT_MAIN, font=FONT_HEADING).pack(anchor="w")

        body = tk.Frame(popup, bg=BG_CARD, padx=14, pady=10)
        body.pack(fill=tk.BOTH, expand=True)

        def _row(label, val, col=TEXT_MAIN):
            r = tk.Frame(body, bg=BG_CARD)
            r.pack(fill=tk.X, pady=2)
            tk.Label(r, text=label, bg=BG_CARD, fg=TEXT_MUTED, font=FONT_BODY).pack(side=tk.LEFT)
            tk.Label(r, text=str(val), bg=BG_CARD, fg=col, font=FONT_CODE_BOLD).pack(side=tk.RIGHT)

        _row("Heap Address:", node_data["address"], CYAN)
        _row("Left Child:", node_data["left"], EMERALD if node_data["left"] != "NULL" else ROSE)
        _row("Right Child:", node_data["right"], EMERALD if node_data["right"] != "NULL" else ROSE)
        _row("Depth Level:", node_data["level"], TEXT_MAIN)
