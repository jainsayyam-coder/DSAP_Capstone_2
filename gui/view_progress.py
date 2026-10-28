"""
DSA Simulator - Progress & Achievements Dashboard View
Visual completion meters, milestone badges, and persistent offline record storage.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL
)
from gui.progress_manager import load_progress, reset_all_progress


class ProgressView(tk.Frame):
    """Progress & Achievement Dashboard with visual completion indicators."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self._build_ui()
        self.refresh_stats()

    def _build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=16)
        header.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(header, text="CAPSTONE LEARNING PORTFOLIO", bg=BG_CARD, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        tk.Label(header, text="Your Mastery Progress & Achievements", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_TITLE).pack(anchor="w")
        tk.Label(
            header,
            text="All progress metrics, challenges solved, and quiz scores are saved locally offline on your device in progress.json.",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=FONT_BODY
        ).pack(anchor="w", pady=(4, 0))

        # 2. Overall Progress Bar Card
        bar_card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=14)
        bar_card.pack(fill=tk.X, padx=14, pady=(0, 10))

        bar_hdr = tk.Frame(bar_card, bg=BG_CARD)
        bar_hdr.pack(fill=tk.X, pady=(0, 6))

        tk.Label(bar_hdr, text="Overall Capstone Mastery", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(side=tk.LEFT)
        self.lbl_pct = tk.Label(bar_hdr, text="0%", bg=BG_CARD, fg=CYAN, font=("Segoe UI", 13, "bold"))
        self.lbl_pct.pack(side=tk.RIGHT)

        self.progress_bar = ttk.Progressbar(bar_card, orient=tk.HORIZONTAL, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(4, 6))

        self.lbl_milestones = tk.Label(bar_card, text="0 / 12 Core Goals Achieved", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL)
        self.lbl_milestones.pack(anchor="w")

        # 3. Four Metric Widgets Grid
        grid = tk.Frame(self, bg=BG_DARK)
        grid.pack(fill=tk.X, padx=14, pady=(0, 10))
        grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="group_metrics")

        self.box_lessons = self._metric_widget(grid, 0, "Lessons Completed", "0 / 4", CYAN)
        self.box_ops = self._metric_widget(grid, 1, "Operations Executed", "0", BLUE)
        self.box_quiz = self._metric_widget(grid, 2, "Best Quiz Accuracy", "0%", EMERALD)
        self.box_chals = self._metric_widget(grid, 3, "Challenges Solved", "0 / 8", PURPLE)

        # 4. Storage & Reset Card
        reset_card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=16)
        reset_card.pack(fill=tk.X, padx=14, pady=(0, 14))

        tk.Label(reset_card, text="Offline Data Persistence", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_SUBHEADING).pack(anchor="w")
        tk.Label(
            reset_card,
            text="Your progress is stored in a clean JSON format. You can reset your progress history anytime to restart the curriculum.",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=FONT_BODY
        ).pack(anchor="w", pady=(4, 12))

        tk.Button(
            reset_card,
            text="⚠️ Reset All Progress Data",
            bg=ROSE,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.confirm_reset
        ).pack(anchor="w")

    def _metric_widget(self, parent, col, title, initial_val, color):
        card = tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=16)
        card.grid(row=0, column=col, padx=5, sticky="nsew")

        lbl_val = tk.Label(card, text=initial_val, bg=BG_CARD, fg=color, font=("Segoe UI", 20, "bold"))
        lbl_val.pack(anchor="w")

        tk.Label(card, text=title, bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(2, 0))
        return lbl_val

    def refresh_stats(self):
        prog = load_progress()
        ops = prog.get("operations_executed", 0)
        best_quiz = prog.get("quiz_best_score", 0)
        chals = len(prog.get("challenges_solved", []))
        lessons = len(prog.get("lessons_completed", []))

        self.box_lessons.config(text=f"{lessons} / 4")
        self.box_ops.config(text=f"{ops}")
        self.box_quiz.config(text=f"{best_quiz}%")
        self.box_chals.config(text=f"{chals} / 8")

        # Total points out of 16 (4 lessons + 8 challenges + 4 quiz tier milestones)
        total_milestones = min(lessons, 4) + min(chals, 8) + (1 if best_quiz > 0 else 0) + (1 if best_quiz >= 80 else 0) + (1 if ops >= 10 else 0)
        max_milestones = 15
        pct = int((total_milestones / max_milestones) * 100)

        self.progress_bar["value"] = pct
        self.lbl_pct.config(text=f"{pct}%")
        self.lbl_milestones.config(text=f"{total_milestones} / {max_milestones} Core Learning Milestones Completed")

    def confirm_reset(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all saved quiz and challenge progress?"):
            reset_all_progress()
            self.refresh_stats()
            messagebox.showinfo("Reset Complete", "All progress data has been reset to initial state.")
