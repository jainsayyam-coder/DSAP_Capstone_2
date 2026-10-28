"""
DSA Simulator - Interactive Operations Laboratory View
Hands-on execution of all linked list operations with instant visual updates,
node click inspection, animations, and complexity analysis.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, BORDER_LIGHT, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
from gui.visualizer_canvas import VisualizerCanvas
from gui.progress_manager import record_operation
import backend.linked_list as ll_backend


class SimulatorView(tk.Frame):
    """Interactive operations lab for Singly, Doubly, Circular Singly, and Circular Doubly Linked Lists."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app

        # Live data structure models
        self.active_lists = {
            "singly": ll_backend.SinglyLinkedList(),
            "doubly": ll_backend.DoublyLinkedList(),
            "circular-singly": ll_backend.CircularSinglyLinkedList(),
            "circular-doubly": ll_backend.CircularDoublyLinkedList()
        }
        self.current_type = "singly"

        # Prepopulate default nodes [10, 20, 30, 40]
        for l_obj in self.active_lists.values():
            for val in [10, 20, 30, 40]:
                l_obj.insert_end(val)

        self._build_ui()
        self.refresh_canvas()

    def _build_ui(self):
        # 1. Top Type Selector Bar
        top_bar = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=8)
        top_bar.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(top_bar, text="STRUCTURE TYPE:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 10))

        self.type_buttons = {}
        types = [
            ("singly", "Singly Linked", CYAN),
            ("doubly", "Doubly Linked", PURPLE),
            ("circular-singly", "Circular Singly", EMERALD),
            ("circular-doubly", "Circular Doubly", AMBER)
        ]

        for code, label, col in types:
            btn = tk.Button(
                top_bar,
                text=label,
                bg=BG_SURFACE if code != self.current_type else col,
                fg=TEXT_MAIN if code != self.current_type else "#000000",
                font=FONT_BODY_BOLD,
                relief=tk.FLAT,
                padx=12,
                pady=4,
                cursor="hand2",
                command=lambda c=code: self.set_list_type(c)
            )
            btn.pack(side=tk.LEFT, padx=4)
            self.type_buttons[code] = (btn, col)

        # Right side presets
        preset_bar = tk.Frame(top_bar, bg=BG_CARD)
        preset_bar.pack(side=tk.RIGHT)

        tk.Button(
            preset_bar,
            text="↺ Reset Example",
            bg=BG_SURFACE,
            fg=TEXT_MAIN,
            font=FONT_SMALL,
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.load_preset
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            preset_bar,
            text="🎲 Random Sample",
            bg=BG_SURFACE,
            fg=TEXT_MAIN,
            font=FONT_SMALL,
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.random_sample
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            preset_bar,
            text="✕ Clear",
            bg=ROSE,
            fg="#ffffff",
            font=FONT_SMALL,
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.clear_list
        ).pack(side=tk.LEFT, padx=3)

        # 2. Main Middle Workspace (Visualizer + Operations Panel)
        workspace = tk.Frame(self, bg=BG_DARK)
        workspace.pack(fill=tk.BOTH, expand=True, padx=14, pady=0)

        # Left Column: Visualizer Canvas & Status
        left_col = tk.Frame(workspace, bg=BG_DARK)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Canvas Header
        canvas_header = tk.Frame(left_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=6)
        canvas_header.pack(fill=tk.X)

        self.lbl_title = tk.Label(canvas_header, text="Singly Linked List Memory View", bg=BG_CARD, fg=CYAN, font=FONT_SUBHEADING)
        self.lbl_title.pack(side=tk.LEFT)

        self.lbl_node_count = tk.Label(canvas_header, text="Length: 4 Nodes", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL)
        self.lbl_node_count.pack(side=tk.RIGHT)

        # Interactive Vector Canvas
        self.visualizer = VisualizerCanvas(left_col, on_node_click=self.on_node_clicked)
        self.visualizer.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Bottom Status Bar
        status_bar = tk.Frame(left_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=8)
        status_bar.pack(fill=tk.X, pady=(4, 0))

        self.status_dot = tk.Label(status_bar, text="●", bg=BG_CARD, fg=EMERALD, font=FONT_HEADING)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 6))

        self.status_text = tk.Label(status_bar, text="Ready. Select an operation from the right-hand panel.", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_BODY)
        self.status_text.pack(side=tk.LEFT)

        self.lbl_complexity = tk.Label(status_bar, text="Time: O(1) | Space: O(1)", bg=BG_SURFACE, fg=CYAN, font=FONT_CODE_BOLD, padx=8, pady=2)
        self.lbl_complexity.pack(side=tk.RIGHT)

        # Right Column: Operations Panel
        ops_panel = tk.Frame(workspace, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, width=280, padx=14, pady=12)
        ops_panel.pack(side=tk.RIGHT, fill=tk.Y)
        ops_panel.pack_propagate(False)

        tk.Label(ops_panel, text="OPERATIONS PANEL", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(anchor="w", pady=(0, 8))

        # Inputs Section
        input_box = tk.Frame(ops_panel, bg=BG_SURFACE, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        input_box.pack(fill=tk.X, pady=(0, 10))

        # Value input
        tk.Label(input_box, text="Value:", bg=BG_SURFACE, fg=TEXT_MUTED, font=FONT_SMALL).grid(row=0, column=0, sticky="w", pady=2)
        self.entry_val = tk.Entry(input_box, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT, font=FONT_BODY, width=14)
        self.entry_val.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=2)
        self.entry_val.insert(0, "42")

        # Position input
        tk.Label(input_box, text="Index (0..N):", bg=BG_SURFACE, fg=TEXT_MUTED, font=FONT_SMALL).grid(row=1, column=0, sticky="w", pady=2)
        self.entry_pos = tk.Entry(input_box, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT, font=FONT_BODY, width=14)
        self.entry_pos.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=2)
        self.entry_pos.insert(0, "2")

        # Insert Group
        tk.Label(ops_panel, text="INSERTION", bg=BG_CARD, fg=CYAN, font=FONT_SMALL).pack(anchor="w", pady=(4, 2))
        self._create_op_btn(ops_panel, "➕ Insert at Beginning", BLUE, self.op_insert_beg)
        self._create_op_btn(ops_panel, "➕ Insert at End", BLUE, self.op_insert_end)
        self._create_op_btn(ops_panel, "➕ Insert at Index", BLUE, self.op_insert_at)

        # Delete Group
        tk.Label(ops_panel, text="DELETION", bg=BG_CARD, fg=ROSE, font=FONT_SMALL).pack(anchor="w", pady=(8, 2))
        self._create_op_btn(ops_panel, "− Delete from Beginning", ROSE, self.op_delete_beg)
        self._create_op_btn(ops_panel, "− Delete from End", ROSE, self.op_delete_end)
        self._create_op_btn(ops_panel, "− Delete at Index", ROSE, self.op_delete_at)

        # Tools & Traversals
        tk.Label(ops_panel, text="SEARCH & UTILITIES", bg=BG_CARD, fg=PURPLE, font=FONT_SMALL).pack(anchor="w", pady=(8, 2))
        self._create_op_btn(ops_panel, "🔍 Search Value", BG_SURFACE, self.op_search)
        self._create_op_btn(ops_panel, "✎ Update at Index", BG_SURFACE, self.op_update)
        self._create_op_btn(ops_panel, "↪ Animate Traversal", BG_SURFACE, self.op_traverse)
        self.btn_reverse = self._create_op_btn(ops_panel, "↶ Reverse List (In-Place)", BG_SURFACE, self.op_reverse)

    def _create_op_btn(self, parent, text, color, cmd):
        btn = tk.Button(
            parent,
            text=text,
            bg=BG_SURFACE if color == BG_SURFACE else color,
            fg=TEXT_MAIN,
            font=FONT_BODY,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            anchor="w",
            command=cmd
        )
        btn.pack(fill=tk.X, pady=2)
        return btn

    # =========================================================================
    # Operation Handlers
    # =========================================================================
    def set_list_type(self, l_type: str):
        self.current_type = l_type
        for code, (btn, col) in self.type_buttons.items():
            if code == l_type:
                btn.config(bg=col, fg="#000000")
            else:
                btn.config(bg=BG_SURFACE, fg=TEXT_MAIN)

        titles = {
            "singly": "Singly Linked List Memory View",
            "doubly": "Doubly Linked List Memory View",
            "circular-singly": "Circular Singly Linked List Memory View",
            "circular-doubly": "Circular Doubly Linked List Memory View"
        }
        self.lbl_title.config(text=titles.get(l_type, "Linked List View"))
        self.refresh_canvas()
        self.set_status(f"Switched to {l_type.replace('-', ' ').title()}.", ok=True)

    def get_current_list(self):
        return self.active_lists[self.current_type]

    def _parse_val(self):
        val = self.entry_val.get().strip()
        if not val:
            raise ValueError("Please enter a node value.")
        try:
            return int(val)
        except ValueError:
            return val

    def _parse_pos(self):
        pos_str = self.entry_pos.get().strip()
        if not pos_str.isdigit():
            raise ValueError("Position must be a non-negative integer (0-indexed).")
        return int(pos_str)

    def refresh_canvas(self, highlight=-1, found=-1, floating=None):
        l_obj = self.get_current_list()
        items = l_obj.to_list()
        self.lbl_node_count.config(text=f"Length: {len(items)} Nodes")
        self.visualizer.render_linked_list(
            items=items,
            list_type=self.current_type,
            highlight_index=highlight,
            found_index=found,
            floating_node=floating
        )

    def set_status(self, msg: str, ok: bool = True, complexity: str = ""):
        self.status_text.config(text=msg)
        self.status_dot.config(fg=EMERALD if ok else ROSE)
        if complexity:
            self.lbl_complexity.config(text=complexity)

    # 1. Insert Operations
    def op_insert_beg(self):
        try:
            val = self._parse_val()
            l_obj = self.get_current_list()
            l_obj.insert_beginning(val)
            record_operation()
            self.refresh_canvas(highlight=0)
            self.set_status(f"Inserted {val} at beginning.", ok=True, complexity="Time: O(1) | Space: O(1)")
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_insert_end(self):
        try:
            val = self._parse_val()
            l_obj = self.get_current_list()
            l_obj.insert_end(val)
            record_operation()
            n = len(l_obj)
            self.refresh_canvas(highlight=n - 1)
            self.set_status(f"Inserted {val} at end (tail).", ok=True, complexity="Time: O(1) [with tail] | Space: O(1)")
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_insert_at(self):
        try:
            val = self._parse_val()
            pos = self._parse_pos()
            l_obj = self.get_current_list()
            if pos < 0 or pos > len(l_obj):
                raise ValueError(f"Index {pos} out of bounds. Valid range: 0 to {len(l_obj)}.")
            ok = l_obj.insert_at(val, pos)
            if ok:
                record_operation()
                self.refresh_canvas(highlight=pos)
                self.set_status(f"Inserted {val} at index {pos}.", ok=True, complexity=f"Time: O(k) = O({pos}) | Space: O(1)")
            else:
                self.set_status("Failed to insert at specified index.", ok=False)
        except Exception as e:
            self.set_status(str(e), ok=False)

    # 2. Delete Operations
    def op_delete_beg(self):
        l_obj = self.get_current_list()
        if len(l_obj) == 0:
            self.set_status("Underflow error: List is already empty.", ok=False)
            return
        val = l_obj.delete_beginning()
        record_operation()
        self.refresh_canvas(highlight=0 if len(l_obj) > 0 else -1)
        self.set_status(f"Deleted value {val} from beginning.", ok=True, complexity="Time: O(1) | Space: O(1)")

    def op_delete_end(self):
        l_obj = self.get_current_list()
        if len(l_obj) == 0:
            self.set_status("Underflow error: List is already empty.", ok=False)
            return
        is_doubly = "doubly" in self.current_type
        val = l_obj.delete_end()
        record_operation()
        self.refresh_canvas(highlight=len(l_obj) - 1 if len(l_obj) > 0 else -1)
        cmplx = "Time: O(1) [tail.prev available]" if is_doubly else "Time: O(n) [must walk from head]"
        self.set_status(f"Deleted value {val} from end.", ok=True, complexity=cmplx)

    def op_delete_at(self):
        try:
            pos = self._parse_pos()
            l_obj = self.get_current_list()
            if pos < 0 or pos >= len(l_obj):
                raise ValueError(f"Index {pos} out of bounds. Valid range: 0 to {len(l_obj) - 1}.")
            val = l_obj.delete_at(pos)
            record_operation()
            self.refresh_canvas(highlight=min(pos, len(l_obj) - 1))
            self.set_status(f"Deleted value {val} at index {pos}.", ok=True, complexity=f"Time: O(k) = O({pos}) | Space: O(1)")
        except Exception as e:
            self.set_status(str(e), ok=False)

    # 3. Search & Update
    def op_search(self):
        try:
            val = self._parse_val()
            l_obj = self.get_current_list()
            idx = l_obj.search(val)
            record_operation()
            if idx != -1:
                self.refresh_canvas(found=idx)
                self.set_status(f"Found value {val} at index {idx}!", ok=True, complexity=f"Time: O(n) = O({idx + 1} steps)")
            else:
                self.refresh_canvas()
                self.set_status(f"Value {val} was NOT found in the list.", ok=False, complexity="Time: O(n) Full Scan")
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_update(self):
        try:
            val = self._parse_val()
            pos = self._parse_pos()
            l_obj = self.get_current_list()
            if pos < 0 or pos >= len(l_obj):
                raise ValueError(f"Index {pos} out of bounds.")
            ok = l_obj.update_at(pos, val)
            if ok:
                record_operation()
                self.refresh_canvas(highlight=pos)
                self.set_status(f"Updated index {pos} value to {val}.", ok=True, complexity="Time: O(k) | Space: O(1)")
        except Exception as e:
            self.set_status(str(e), ok=False)

    # 4. Animated Traversal
    def op_traverse(self):
        l_obj = self.get_current_list()
        items = l_obj.to_list()
        if not items:
            self.set_status("Cannot traverse: list is empty.", ok=False)
            return

        def _step_visit(idx):
            if idx < len(items):
                self.refresh_canvas(highlight=idx)
                self.set_status(f"Visiting node at index {idx} (Value: {items[idx]})", ok=True, complexity="Time: O(n)")
                self.after(350, lambda: _step_visit(idx + 1))
            else:
                loop_text = " → (loops back to HEAD)" if "circular" in self.current_type else " → NULL"
                val_chain = " → ".join(map(str, items)) + loop_text
                self.refresh_canvas()
                self.set_status(f"Traversal Complete: {val_chain}", ok=True, complexity="Time: O(n)")

        _step_visit(0)

    # 5. In-Place Reversal
    def op_reverse(self):
        l_obj = self.get_current_list()
        if len(l_obj) < 2:
            self.set_status("Add at least 2 nodes before reversing.", ok=False)
            return

        if hasattr(l_obj, "reverse"):
            l_obj.reverse()
            record_operation()
            self.refresh_canvas(highlight=0)
            self.set_status("Reversed entire list in-place using three pointers.", ok=True, complexity="Time: O(n) | Space: O(1)")
        else:
            self.set_status("In-place reversal is supported for Singly and Doubly lists.", ok=False)

    # 6. Presets
    def load_preset(self):
        l_obj = self.get_current_list()
        l_obj.clear()
        for v in [10, 20, 30, 40]:
            l_obj.insert_end(v)
        self.refresh_canvas()
        self.set_status("Loaded default list: [10, 20, 30, 40].", ok=True)

    def random_sample(self):
        l_obj = self.get_current_list()
        l_obj.clear()
        count = random.randint(3, 6)
        samples = random.sample(range(5, 99), count)
        for v in samples:
            l_obj.insert_end(v)
        self.refresh_canvas()
        self.set_status(f"Generated {count} random nodes: {samples}.", ok=True)

    def clear_list(self):
        l_obj = self.get_current_list()
        l_obj.clear()
        self.refresh_canvas()
        self.set_status("List cleared. All nodes released.", ok=True)

    # =========================================================================
    # Node Click Inspector Popover
    # =========================================================================
    def on_node_clicked(self, node_data: Dict[str, Any]):
        """Open detailed memory inspector for the clicked node."""
        popup = tk.Toplevel(self)
        popup.title(f"Node Inspector — Index {node_data['index']}")
        popup.geometry("380x280")
        popup.configure(bg=BG_CARD)
        popup.resizable(False, False)

        header = tk.Frame(popup, bg=BG_SURFACE, padx=14, pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="🔍 DYNAMIC HEAP NODE INSPECTOR", bg=BG_SURFACE, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        tk.Label(header, text=f"Node Index [{node_data['index']}]", bg=BG_SURFACE, fg=TEXT_MAIN, font=FONT_HEADING).pack(anchor="w")

        body = tk.Frame(popup, bg=BG_CARD, padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        def _row(label, val, col=TEXT_MAIN):
            r = tk.Frame(body, bg=BG_CARD)
            r.pack(fill=tk.X, pady=3)
            tk.Label(r, text=label, bg=BG_CARD, fg=TEXT_MUTED, font=FONT_BODY).pack(side=tk.LEFT)
            tk.Label(r, text=str(val), bg=BG_CARD, fg=col, font=FONT_CODE_BOLD).pack(side=tk.RIGHT)

        _row("Stored Value:", node_data["value"], TEXT_MAIN)
        _row("Heap Address:", node_data["address"], CYAN)
        _row("NEXT Pointer ->", node_data["next_addr"], CYAN)
        if node_data.get("prev_addr"):
            _row("PREV Pointer <-", node_data["prev_addr"], PURPLE)

        # Architectural details
        sep = tk.Frame(body, bg=BORDER, height=1)
        sep.pack(fill=tk.X, pady=8)
        tk.Label(body, text="Memory Breakdown (64-bit architecture):", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")
        tk.Label(body, text="• 8 Bytes Payload Value\n• 8 Bytes Next Memory Address\n• 16 Bytes GC / Class Object Header", bg=BG_CARD, fg=TEXT_DIM, font=FONT_SMALL, justify=tk.LEFT).pack(anchor="w", pady=(2, 0))
