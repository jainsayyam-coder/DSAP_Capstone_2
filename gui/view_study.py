"""
DSA Simulator - Step-by-Step Study Mode View
Guided algorithm animation engine with synchronized pseudocode line highlighting,
safety warnings, and pointer ordering explanations.
"""

import tkinter as tk
from tkinter import ttk
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)
from gui.visualizer_canvas import VisualizerCanvas
from backend.algorithm_tracer import get_operation_steps


class StudyView(tk.Frame):
    """Step-by-Step Study Mode with timeline scrubber, pseudocode line tracker, and educational cards."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app

        # Animation state
        self.steps_data = None
        self.current_step = 0
        self.is_playing = False
        self.timer_id = None
        self.speed_ms = 1000

        self._build_ui()
        self.load_study_demo()

    def _build_ui(self):
        # 1. Top Controls Bar
        ctrl_bar = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=10)
        ctrl_bar.pack(fill=tk.X, padx=14, pady=(12, 10))

        # Structure dropdown
        tk.Label(ctrl_bar, text="Structure:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 4))
        self.combo_type = ttk.Combobox(
            ctrl_bar,
            values=["Singly Linked List", "Doubly Linked List", "Circular Singly List", "Circular Doubly List"],
            state="readonly",
            width=18
        )
        self.combo_type.current(0)
        self.combo_type.pack(side=tk.LEFT, padx=(0, 12))
        self.combo_type.bind("<<ComboboxSelected>>", lambda e: self.load_study_demo())

        # Operation dropdown
        tk.Label(ctrl_bar, text="Operation:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 4))
        self.combo_op = ttk.Combobox(
            ctrl_bar,
            values=["Insert at Beginning", "Insert at End", "Insert at Position", "Delete from Beginning", "Delete from End", "Reverse List"],
            state="readonly",
            width=20
        )
        self.combo_op.current(0)
        self.combo_op.pack(side=tk.LEFT, padx=(0, 12))
        self.combo_op.bind("<<ComboboxSelected>>", lambda e: self.load_study_demo())

        # Value input
        tk.Label(ctrl_bar, text="Val:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 2))
        self.entry_val = tk.Entry(ctrl_bar, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief=tk.FLAT, width=5)
        self.entry_val.insert(0, "99")
        self.entry_val.pack(side=tk.LEFT, padx=(0, 12))

        # Reload button
        tk.Button(
            ctrl_bar,
            text="🔄 Load Demo",
            bg=BLUE,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.load_study_demo
        ).pack(side=tk.LEFT)

        # Speed slider on right
        speed_box = tk.Frame(ctrl_bar, bg=BG_CARD)
        speed_box.pack(side=tk.RIGHT)
        tk.Label(speed_box, text="Speed:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 4))
        self.speed_scale = tk.Scale(
            speed_box,
            from_=300,
            to=2200,
            orient=tk.HORIZONTAL,
            showvalue=False,
            bg=BG_CARD,
            troughcolor=BG_SURFACE,
            highlightthickness=0,
            length=100,
            command=self._on_speed_change
        )
        self.speed_scale.set(1000)
        self.speed_scale.pack(side=tk.LEFT)

        # 2. Middle Canvas & Details Area
        middle = tk.Frame(self, bg=BG_DARK)
        middle.pack(fill=tk.BOTH, expand=True, padx=14, pady=0)

        # Left Column: Vector Canvas & Stepper
        canvas_col = tk.Frame(middle, bg=BG_DARK)
        canvas_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Title bar
        hdr = tk.Frame(canvas_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=6)
        hdr.pack(fill=tk.X)
        self.lbl_study_title = tk.Label(hdr, text="Step-by-Step Algorithm Visualization", bg=BG_CARD, fg=CYAN, font=FONT_SUBHEADING)
        self.lbl_study_title.pack(side=tk.LEFT)
        self.lbl_step_counter = tk.Label(hdr, text="Step 1 of 4", bg=BG_CARD, fg=AMBER, font=FONT_CODE_BOLD)
        self.lbl_step_counter.pack(side=tk.RIGHT)

        # Visualizer Canvas
        self.visualizer = VisualizerCanvas(canvas_col)
        self.visualizer.pack(fill=tk.BOTH, expand=True, pady=(2, 6))

        # Stepper Button Controls
        stepper_bar = tk.Frame(canvas_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=8)
        stepper_bar.pack(fill=tk.X)

        self.btn_first = self._step_btn(stepper_bar, "⏮ First", self.step_first)
        self.btn_prev = self._step_btn(stepper_bar, "◀ Prev", self.step_prev)
        self.btn_play = self._step_btn(stepper_bar, "▶ Play", self.toggle_play, is_play=True)
        self.btn_next = self._step_btn(stepper_bar, "Next ▶", self.step_next)
        self.btn_last = self._step_btn(stepper_bar, "⏭ Last", self.step_last)
        self.btn_reset = self._step_btn(stepper_bar, "↺ Reset", self.step_reset)

        self.lbl_badge = tk.Label(stepper_bar, text="O(1) Constant", bg=BG_SURFACE, fg=CYAN, font=FONT_CODE_BOLD, padx=8, pady=3)
        self.lbl_badge.pack(side=tk.RIGHT)

        # Right Column: Pseudocode & Explanations (Cards)
        info_col = tk.Frame(middle, bg=BG_DARK, width=340)
        info_col.pack(side=tk.RIGHT, fill=tk.BOTH)
        info_col.pack_propagate(False)

        # Explanation Card (What is happening)
        exp_card = tk.Frame(info_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12)
        exp_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(exp_card, text="CURRENT ACTION", bg=BG_CARD, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        self.lbl_action_title = tk.Label(exp_card, text="Action Title", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_HEADING, wraplength=310, justify=tk.LEFT)
        self.lbl_action_title.pack(anchor="w", pady=(2, 4))

        self.lbl_action_desc = tk.Label(exp_card, text="Description...", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_BODY, wraplength=310, justify=tk.LEFT)
        self.lbl_action_desc.pack(anchor="w", pady=(0, 8))

        # Why it matters card
        why_card = tk.Frame(exp_card, bg=BG_SURFACE, padx=10, pady=8, highlightbackground=AMBER, highlightthickness=1)
        why_card.pack(fill=tk.X)
        tk.Label(why_card, text="⚠️ WHY POINTER ORDER MATTERS:", bg=BG_SURFACE, fg=AMBER, font=FONT_SMALL).pack(anchor="w")
        self.lbl_why_matters = tk.Label(why_card, text="Pointer rules explanation...", bg=BG_SURFACE, fg=TEXT_MAIN, font=FONT_BODY, wraplength=290, justify=tk.LEFT)
        self.lbl_why_matters.pack(anchor="w", pady=(2, 0))

        # Pseudocode Card
        code_card = tk.Frame(info_col, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12)
        code_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(code_card, text="ALGORITHM PSEUDOCODE", bg=BG_CARD, fg=PURPLE, font=FONT_SMALL).pack(anchor="w", pady=(0, 6))

        self.code_text = tk.Text(
            code_card,
            bg=BG_INPUT,
            fg=TEXT_MUTED,
            font=FONT_CODE_BOLD,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            height=8
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.tag_configure("active_line", background="#1e3a5f", foreground=CYAN)

    def _step_btn(self, parent, text, cmd, is_play=False):
        btn = tk.Button(
            parent,
            text=text,
            bg=BLUE if is_play else BG_SURFACE,
            fg="#ffffff" if is_play else TEXT_MAIN,
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=cmd
        )
        btn.pack(side=tk.LEFT, padx=3)
        return btn

    def _on_speed_change(self, val):
        self.speed_ms = int(val)

    # =========================================================================
    # Step Playback Logic
    # =========================================================================
    def load_study_demo(self):
        self.stop_play()
        st = self.combo_type.get()
        op_text = self.combo_op.get()

        op_map = {
            "Insert at Beginning": "insert_beginning",
            "Insert at End": "insert_end",
            "Insert at Position": "insert_at",
            "Delete from Beginning": "delete_beginning",
            "Delete from End": "delete_end",
            "Reverse List": "reverse"
        }
        op_code = op_map.get(op_text, "insert_beginning")

        try:
            val = int(self.entry_val.get().strip() or "99")
        except ValueError:
            val = 99

        sample_items = [10, 20, 30, 40]
        self.steps_data = get_operation_steps(
            structure_type=st,
            operation=op_code,
            initial_items=sample_items,
            val=val,
            pos=2
        )
        self.current_step = 0
        self.lbl_study_title.config(text=self.steps_data["title"])
        self.lbl_badge.config(text=self.steps_data["complexity_time"])
        self._render_current_step()

    def _render_current_step(self):
        if not self.steps_data:
            return
        steps = self.steps_data["steps"]
        total = len(steps)
        if total == 0:
            return

        step = steps[self.current_step]
        self.lbl_step_counter.config(text=f"Step {self.current_step + 1} of {total}")
        self.lbl_action_title.config(text=step["title"])
        self.lbl_action_desc.config(text=step["description"])
        self.lbl_why_matters.config(text=step["why_it_matters"])
        self.lbl_badge.config(text=step.get("status_badge", "Processing"))

        # Render Pseudocode with active line highlight
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete("1.0", tk.END)
        active_line = step["pseudo_line"]

        for i, line in enumerate(self.steps_data["pseudocode"]):
            line_start = f"{i + 1}.0"
            self.code_text.insert(tk.END, line + "\n")
            if i == active_line:
                self.code_text.tag_add("active_line", line_start, f"{i + 1}.end")

        self.code_text.config(state=tk.DISABLED)

        # Render Vector Canvas
        active_idx = step["active_indices"][0] if step["active_indices"] else -1
        self.visualizer.render_linked_list(
            items=step["items"],
            list_type=self.combo_type.get().lower(),
            highlight_index=active_idx,
            floating_node=step.get("new_node_value")
        )

    def step_next(self):
        if not self.steps_data:
            return
        if self.current_step < len(self.steps_data["steps"]) - 1:
            self.current_step += 1
            self._render_current_step()
        else:
            self.stop_play()

    def step_prev(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._render_current_step()

    def step_first(self):
        self.current_step = 0
        self._render_current_step()

    def step_last(self):
        if self.steps_data:
            self.current_step = len(self.steps_data["steps"]) - 1
            self._render_current_step()

    def step_reset(self):
        self.stop_play()
        self.current_step = 0
        self._render_current_step()

    def toggle_play(self):
        if self.is_playing:
            self.stop_play()
        else:
            self.start_play()

    def start_play(self):
        self.is_playing = True
        self.btn_play.config(text="⏸ Pause", bg=ROSE)
        self._play_loop()

    def stop_play(self):
        self.is_playing = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.btn_play.config(text="▶ Play", bg=BLUE)

    def _play_loop(self):
        if not self.is_playing:
            return
        if self.current_step < len(self.steps_data["steps"]) - 1:
            self.step_next()
            self.timer_id = self.after(self.speed_ms, self._play_loop)
        else:
            self.stop_play()
