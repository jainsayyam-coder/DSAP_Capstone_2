"""
DSA Simulator - Master Desktop Application Window
Coordinates sidebar navigation, view switching, and top navbar status.
"""

import tkinter as tk
from tkinter import ttk
from gui.theme import (
    apply_theme, BG_DARK, BG_SIDEBAR, BG_CARD, BG_SURFACE, BORDER, BORDER_LIGHT,
    TEXT_MAIN, TEXT_MUTED, CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL,
    FONT_CODE, FONT_CODE_BOLD
)
from gui.view_home import HomeView
from gui.view_simulator import SimulatorView
from gui.view_study import StudyView
from gui.view_tree import TreeView
from gui.view_stack_queue import StackQueueView
from gui.view_code import CodeView
from gui.view_complexity import ComplexityView
from gui.view_quiz import QuizView
from gui.view_challenges import ChallengesView
from gui.view_progress import ProgressView
from gui.view_tests import TestsView


class DSASimulatorApp(tk.Tk):
    """Primary window layout and navigation orchestrator for the pure Python Capstone Simulator."""

    def __init__(self):
        super().__init__()
        self.title("DSA Simulator — Capstone Interactive Laboratory")
        self.geometry("1280x800")
        self.minsize(1024, 680)
        self.configure(bg=BG_DARK)

        apply_theme(self)

        # Active view state
        self.views = {}
        self.active_tab_key = "home"
        self.nav_buttons = {}

        self._build_layout()
        self.switch_tab("home")

    def _build_layout(self):
        # 1. Left Sidebar Navigation
        self.sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=240, highlightbackground=BORDER, highlightthickness=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Brand header
        brand_frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR, padx=16, pady=16)
        brand_frame.pack(fill=tk.X)

        brand_logo = tk.Label(brand_frame, text="🔗  DSA LAB", bg=BG_SIDEBAR, fg=CYAN, font=("Segoe UI", 15, "bold"))
        brand_logo.pack(anchor="w")

        brand_sub = tk.Label(brand_frame, text="Interactive Data Structures", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=FONT_SMALL)
        brand_sub.pack(anchor="w", pady=(2, 0))

        # Nav items separator
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill=tk.X, padx=14, pady=(4, 10))

        tk.Label(self.sidebar, text="LEARNING MODULES", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=FONT_SMALL, padx=16).pack(anchor="w", pady=(0, 4))

        # Navigation menu items
        nav_items = [
            ("home", "⌂  Dashboard Overview"),
            ("simulator", "⛓  Linked List Simulator"),
            ("study", "▷  Step-by-Step Study"),
            ("tree", "🌳  Binary Search Tree"),
            ("stack_queue", "📚  Stack & Queue"),
            ("code", "</>  Algorithm & Code"),
            ("complexity", "▥  Complexity Matrix"),
            ("quiz", "📝  Quiz & Assessment"),
            ("challenges", "✦  Practice Challenges"),
            ("progress", "↗  My Learning Progress"),
            ("tests", "✓  Automated Tests")
        ]

        self.nav_container = tk.Frame(self.sidebar, bg=BG_SIDEBAR)
        self.nav_container.pack(fill=tk.X, padx=8)

        for key, label in nav_items:
            btn = tk.Button(
                self.nav_container,
                text=label,
                bg=BG_SIDEBAR,
                fg=TEXT_MUTED,
                font=FONT_BODY,
                relief=tk.FLAT,
                padx=12,
                pady=6,
                cursor="hand2",
                anchor="w",
                command=lambda k=key: self.switch_tab(k)
            )
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons[key] = btn

        # Sidebar footer
        footer_frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR, padx=16, pady=14)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(footer_frame, text="Capstone Project Edition", bg=BG_SIDEBAR, fg=CYAN, font=FONT_SMALL).pack(anchor="w")
        tk.Label(footer_frame, text="100% Python • Pure Offline", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")

        # 2. Main Workspace (Right)
        self.main_wrapper = tk.Frame(self, bg=BG_DARK)
        self.main_wrapper.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Top Navbar
        self.topbar = tk.Frame(self.main_wrapper, bg=BG_SIDEBAR, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=8)
        self.topbar.pack(fill=tk.X)

        self.lbl_breadcrumb = tk.Label(self.topbar, text="DSA Simulator / Dashboard", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=FONT_BODY)
        self.lbl_breadcrumb.pack(side=tk.LEFT)

        self.lbl_mode_pill = tk.Label(self.topbar, text="● Offline Mode: Active", bg=BG_SURFACE, fg=EMERALD, font=FONT_CODE_BOLD, padx=10, pady=3)
        self.lbl_mode_pill.pack(side=tk.RIGHT)

        # Container for swappable views
        self.content_container = tk.Frame(self.main_wrapper, bg=BG_DARK)
        self.content_container.pack(fill=tk.BOTH, expand=True)

        # Instantiate all views
        self.views["home"] = HomeView(self.content_container, self)
        self.views["simulator"] = SimulatorView(self.content_container, self)
        self.views["study"] = StudyView(self.content_container, self)
        self.views["tree"] = TreeView(self.content_container, self)
        self.views["stack_queue"] = StackQueueView(self.content_container, self)
        self.views["code"] = CodeView(self.content_container, self)
        self.views["complexity"] = ComplexityView(self.content_container, self)
        self.views["quiz"] = QuizView(self.content_container, self)
        self.views["challenges"] = ChallengesView(self.content_container, self)
        self.views["progress"] = ProgressView(self.content_container, self)
        self.views["tests"] = TestsView(self.content_container, self)

    def switch_tab(self, tab_key: str):
        if tab_key not in self.views:
            return

        self.active_tab_key = tab_key

        # Update sidebar active styling
        for key, btn in self.nav_buttons.items():
            if key == tab_key:
                btn.config(bg=BG_CARD, fg=CYAN, font=FONT_BODY_BOLD)
            else:
                btn.config(bg=BG_SIDEBAR, fg=TEXT_MUTED, font=FONT_BODY)

        # Update breadcrumb title
        titles = {
            "home": "Dashboard Overview",
            "simulator": "Linked List Laboratory",
            "study": "Step-by-Step Study Mode",
            "tree": "Binary Search Tree Laboratory",
            "stack_queue": "Stack & Queue Laboratory",
            "code": "Algorithm & Multi-Language Code Viewer",
            "complexity": "Time & Space Complexity Matrix",
            "quiz": "Interactive Quiz & Assessment",
            "challenges": "Practice Challenges",
            "progress": "My Learning Progress & Portfolio",
            "tests": "Automated Unit Test Suite"
        }
        self.lbl_breadcrumb.config(text=f"DSA Simulator / {titles.get(tab_key, '')}")

        # Hide all views and show active view
        for view in self.views.values():
            view.pack_forget()

        active_view = self.views[tab_key]
        active_view.pack(fill=tk.BOTH, expand=True)

        # Refresh stats if switching to progress or home
        if tab_key == "progress":
            active_view.refresh_stats()
        elif tab_key == "home":
            active_view.refresh_metrics()
