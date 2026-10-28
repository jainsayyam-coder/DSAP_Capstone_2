"""
DSA Simulator - Stack & Queue Laboratory View
Interactive LIFO and FIFO visualizers with push, pop, enqueue, dequeue,
boundary overflow/underflow checking, and pointer tracking.
"""

import tkinter as tk
from tkinter import ttk
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
from gui.visualizer_canvas import VisualizerCanvas
from backend.stack import Stack
from backend.queue import Queue
from gui.progress_manager import record_operation


class StackQueueView(tk.Frame):
    """Unified laboratory for Stack (LIFO) and Queue (FIFO) visual manipulation."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self.active_mode = "stack"  # 'stack' or 'queue'

        self.stack = Stack(capacity=7)
        for v in [10, 20, 30]:
            self.stack.push(v)

        self.queue = Queue(capacity=7)
        for v in [10, 20, 30]:
            self.queue.enqueue(v)

        self._build_ui()
        self.refresh_display()

    def _build_ui(self):
        # 1. Mode Selector Bar
        top_bar = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=8)
        top_bar.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(top_bar, text="STRUCTURE:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 8))

        self.btn_stack_mode = tk.Button(
            top_bar,
            text="📚 Stack (LIFO)",
            bg=CYAN,
            fg="#000000",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.switch_mode("stack")
        )
        self.btn_stack_mode.pack(side=tk.LEFT, padx=4)

        self.btn_queue_mode = tk.Button(
            top_bar,
            text="🚶 Queue (FIFO)",
            bg=BG_SURFACE,
            fg=TEXT_MAIN,
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.switch_mode("queue")
        )
        self.btn_queue_mode.pack(side=tk.LEFT, padx=4)

        # Capacity counter on right
        self.lbl_cap = tk.Label(top_bar, text="Size: 3 / 7 | Capacity: 7", bg=BG_SURFACE, fg=CYAN, font=FONT_CODE_BOLD, padx=8, pady=3)
        self.lbl_cap.pack(side=tk.RIGHT)

        # 2. Main Workspace
        workspace = tk.Frame(self, bg=BG_DARK)
        workspace.pack(fill=tk.BOTH, expand=True, padx=14, pady=0)

        # Left Column: Canvas
        left_col = tk.Frame(workspace, bg=BG_DARK)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.lbl_canvas_title = tk.Label(left_col, text="Stack Memory Cylinder (Last In, First Out)", bg=BG_CARD, fg=CYAN, font=FONT_SUBHEADING, padx=12, pady=6)
        self.lbl_canvas_title.pack(fill=tk.X)

        self.visualizer = VisualizerCanvas(left_col)
        self.visualizer.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Bottom Status Bar
        status_bar = tk.Frame(left_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=6)
        status_bar.pack(fill=tk.X, pady=(4, 0))

        self.status_dot = tk.Label(status_bar, text="●", bg=BG_CARD, fg=EMERALD, font=FONT_HEADING)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 6))

        self.status_text = tk.Label(status_bar, text="Ready. Push/Enqueue or Pop/Dequeue elements.", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_BODY)
        self.status_text.pack(side=tk.LEFT)

        # Right Column: Controls Panel
        ctrl_panel = tk.Frame(workspace, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, width=260, padx=14, pady=12)
        ctrl_panel.pack(side=tk.RIGHT, fill=tk.Y)
        ctrl_panel.pack_propagate(False)

        tk.Label(ctrl_panel, text="DATA OPERATIONS", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(anchor="w", pady=(0, 10))

        # Input Value
        tk.Label(ctrl_panel, text="Value to Add:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")
        self.entry_val = tk.Entry(ctrl_panel, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT, font=FONT_BODY)
        self.entry_val.insert(0, "50")
        self.entry_val.pack(fill=tk.X, pady=(2, 10))

        # Action Buttons (Dynamic based on mode)
        self.btn_add = self._btn(ctrl_panel, "➕ Push(val)", BLUE, self.op_add)
        self.btn_remove = self._btn(ctrl_panel, "− Pop()", ROSE, self.op_remove)
        self.btn_peek = self._btn(ctrl_panel, "👁 Peek()", BG_SURFACE, self.op_peek)
        self.btn_clear = self._btn(ctrl_panel, "✕ Clear", BG_SURFACE, self.op_clear)

        # Architectural Concept Box
        sep = tk.Frame(ctrl_panel, bg=BORDER, height=1)
        sep.pack(fill=tk.X, pady=12)

        self.lbl_concept_title = tk.Label(ctrl_panel, text="LIFO PRINCIPLE:", bg=BG_CARD, fg=CYAN, font=FONT_SMALL)
        self.lbl_concept_title.pack(anchor="w")

        self.lbl_concept_desc = tk.Label(
            ctrl_panel,
            text="The last element pushed onto the stack is the first element to be popped off.\n\nAll operations take O(1) constant time.",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=FONT_SMALL,
            justify=tk.LEFT,
            wraplength=230
        )
        self.lbl_concept_desc.pack(anchor="w", pady=(4, 0))

    def _btn(self, parent, text, color, cmd):
        btn = tk.Button(
            parent,
            text=text,
            bg=color,
            fg="#ffffff" if color in (BLUE, ROSE) else TEXT_MAIN,
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            anchor="w",
            command=cmd
        )
        btn.pack(fill=tk.X, pady=3)
        return btn

    def switch_mode(self, mode: str):
        self.active_mode = mode
        if mode == "stack":
            self.btn_stack_mode.config(bg=CYAN, fg="#000000")
            self.btn_queue_mode.config(bg=BG_SURFACE, fg=TEXT_MAIN)
            self.lbl_canvas_title.config(text="Stack Memory Cylinder (Last In, First Out)")
            self.btn_add.config(text="➕ Push(val)", bg=BLUE)
            self.btn_remove.config(text="− Pop()", bg=ROSE)
            self.btn_peek.config(text="👁 Peek()")
            self.lbl_concept_title.config(text="LIFO PRINCIPLE:")
            self.lbl_concept_desc.config(text="The last element pushed onto the stack is the first element to be popped off.\n\nAll operations take O(1) constant time.")
        else:
            self.btn_stack_mode.config(bg=BG_SURFACE, fg=TEXT_MAIN)
            self.btn_queue_mode.config(bg=PURPLE, fg="#ffffff")
            self.lbl_canvas_title.config(text="Queue Conveyor (First In, First Out)")
            self.btn_add.config(text="➕ Enqueue(val)", bg=PURPLE)
            self.btn_remove.config(text="− Dequeue()", bg=ROSE)
            self.btn_peek.config(text="👁 Peek Front / Rear")
            self.lbl_concept_title.config(text="FIFO PRINCIPLE:")
            self.lbl_concept_desc.config(text="The first element inserted into the queue is the first to be removed.\n\nEnqueues occur at REAR, dequeues at FRONT.")

        self.refresh_display()
        self.set_status(f"Switched to {mode.title()} mode.", ok=True)

    def _parse_val(self):
        val_str = self.entry_val.get().strip()
        if not val_str:
            raise ValueError("Enter a value.")
        try:
            return int(val_str)
        except ValueError:
            return val_str

    def refresh_display(self):
        if self.active_mode == "stack":
            items = list(self.stack.items)
            self.visualizer.render_stack(items, capacity=self.stack.capacity, top_index=self.stack.top)
            self.lbl_cap.config(text=f"Size: {len(items)} / {self.stack.capacity} | Cap: {self.stack.capacity}")
        else:
            items = list(self.queue.items)
            self.visualizer.render_queue(items, capacity=self.queue.capacity)
            self.lbl_cap.config(text=f"Size: {len(items)} / {self.queue.capacity} | Cap: {self.queue.capacity}")

    def set_status(self, msg: str, ok: bool = True):
        self.status_text.config(text=msg)
        self.status_dot.config(fg=EMERALD if ok else ROSE)

    # Operations
    def op_add(self):
        try:
            val = self._parse_val()
            if self.active_mode == "stack":
                if self.stack.is_full():
                    self.set_status("Stack Overflow: capacity limit reached (7 max).", ok=False)
                    return
                self.stack.push(val)
                record_operation()
                self.refresh_display()
                self.set_status(f"Pushed {val} onto top of stack.", ok=True)
            else:
                if self.queue.is_full():
                    self.set_status("Queue Overflow: capacity limit reached (7 max).", ok=False)
                    return
                self.queue.enqueue(val)
                record_operation()
                self.refresh_display()
                self.set_status(f"Enqueued {val} at rear of queue.", ok=True)
        except Exception as e:
            self.set_status(str(e), ok=False)

    def op_remove(self):
        if self.active_mode == "stack":
            if self.stack.is_empty():
                self.set_status("Stack Underflow: stack is empty.", ok=False)
                return
            val = self.stack.pop()
            record_operation()
            self.refresh_display()
            self.set_status(f"Popped value {val} from top of stack.", ok=True)
        else:
            if self.queue.is_empty():
                self.set_status("Queue Underflow: queue is empty.", ok=False)
                return
            val = self.queue.dequeue()
            record_operation()
            self.refresh_display()
            self.set_status(f"Dequeued value {val} from front of queue.", ok=True)

    def op_peek(self):
        if self.active_mode == "stack":
            val = self.stack.peek()
            if val is not None:
                self.set_status(f"Top element is: {val}", ok=True)
            else:
                self.set_status("Stack is empty.", ok=False)
        else:
            f = self.queue.peek_front()
            r = self.queue.peek_rear()
            if f is not None:
                self.set_status(f"Front element: {f} | Rear element: {r}", ok=True)
            else:
                self.set_status("Queue is empty.", ok=False)

    def op_clear(self):
        if self.active_mode == "stack":
            self.stack.clear()
        else:
            self.queue.clear()
        self.refresh_display()
        self.set_status("Cleared structure.", ok=True)
