"""
DSA Simulator - Theme System & Modern Styling Constants
Dark Navy / Cyan / Slate Palette for Premium Capstone Aesthetic
"""

import tkinter as tk
from tkinter import ttk

# ==============================================================================
# COLOR PALETTE
# ==============================================================================
BG_DARK = "#0a0f1d"          # Main window & canvas background
BG_SIDEBAR = "#0e1626"       # Navigation sidebar
BG_CARD = "#141f36"          # Cards, panels, elevated sections
BG_SURFACE = "#1a2942"       # Sub-cards, table headers, hover states
BG_INPUT = "#0c1322"         # Text boxes, entry inputs
BORDER = "#223554"           # Dividers & card outlines
BORDER_LIGHT = "#2d446b"     # Hover borders

TEXT_MAIN = "#f1f5f9"        # High-contrast text
TEXT_MUTED = "#8da2c0"       # Subtitles, labels, explanations
TEXT_DIM = "#556b8d"          # Disabled / subtle indicators

# Semantic & Data Structure Colors
CYAN = "#00e5ff"             # Singly Linked List & Head pointers
BLUE = "#3b82f6"             # Primary actions & Traverse
PURPLE = "#a855f7"           # Doubly Linked List & Prev pointers
EMERALD = "#10b981"          # Circular Singly & Success badges
AMBER = "#f59e0b"            # Circular Doubly & Tail pointers
ROSE = "#f43f5e"             # Deletions, underflow, errors
GOLD = "#fbbf24"             # Active search match / highlight

# Visual Node Colors
NODE_BG = "#17233d"
NODE_BORDER = "#38bdf8"
NODE_DATA_BG = "#0c1424"
NODE_HIGHLIGHT = "#f59e0b"
NODE_FOUND = "#10b981"
ARROW_FORWARD = "#38bdf8"
ARROW_BACKWARD = "#a855f7"
ARROW_CIRCULAR = "#34d399"

# ==============================================================================
# TYPOGRAPHY
# ==============================================================================
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_HEADING = ("Segoe UI", 12, "bold")
FONT_SUBHEADING = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 9)
FONT_BODY_BOLD = ("Segoe UI", 9, "bold")
FONT_SMALL = ("Segoe UI", 8)
FONT_CODE = ("Consolas", 9)
FONT_CODE_BOLD = ("Consolas", 9, "bold")
FONT_CODE_LG = ("Consolas", 10)


def apply_theme(root: tk.Tk) -> None:
    """Configure modern dark style for ttk widgets."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(".", background=BG_DARK, foreground=TEXT_MAIN, font=FONT_BODY)
    style.configure("TFrame", background=BG_DARK)
    style.configure("Card.TFrame", background=BG_CARD)
    style.configure("Surface.TFrame", background=BG_SURFACE)
    style.configure("Sidebar.TFrame", background=BG_SIDEBAR)

    style.configure("TLabel", background=BG_DARK, foreground=TEXT_MAIN, font=FONT_BODY)
    style.configure("Card.TLabel", background=BG_CARD, foreground=TEXT_MAIN)
    style.configure("Muted.TLabel", background=BG_CARD, foreground=TEXT_MUTED)
    style.configure("Title.TLabel", font=FONT_TITLE, foreground=TEXT_MAIN, background=BG_DARK)
    style.configure("Heading.TLabel", font=FONT_HEADING, foreground=TEXT_MAIN, background=BG_CARD)

    # Buttons
    style.configure(
        "TButton",
        background=BG_SURFACE,
        foreground=TEXT_MAIN,
        borderwidth=1,
        focuscolor="none",
        padding=(8, 4),
        font=FONT_BODY_BOLD
    )
    style.map(
        "TButton",
        background=[("active", BORDER_LIGHT), ("pressed", BLUE)],
        foreground=[("active", TEXT_MAIN)]
    )

    style.configure(
        "Primary.TButton",
        background=BLUE,
        foreground="#ffffff",
        borderwidth=0,
        font=FONT_BODY_BOLD
    )
    style.map(
        "Primary.TButton",
        background=[("active", "#2563eb"), ("pressed", "#1d4ed8")]
    )

    style.configure(
        "Danger.TButton",
        background=ROSE,
        foreground="#ffffff",
        borderwidth=0,
        font=FONT_BODY_BOLD
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#e11d48"), ("pressed", "#be123c")]
    )

    style.configure(
        "Success.TButton",
        background=EMERALD,
        foreground="#ffffff",
        borderwidth=0,
        font=FONT_BODY_BOLD
    )

    style.configure(
        "Purple.TButton",
        background=PURPLE,
        foreground="#ffffff",
        borderwidth=0,
        font=FONT_BODY_BOLD
    )

    # Entry and Combobox
    style.configure(
        "TEntry",
        fieldbackground=BG_INPUT,
        foreground=TEXT_MAIN,
        insertcolor=TEXT_MAIN,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER
    )

    style.configure(
        "TCombobox",
        fieldbackground=BG_INPUT,
        background=BG_SURFACE,
        foreground=TEXT_MAIN,
        arrowcolor=TEXT_MAIN
    )

    # Notebook Tabs
    style.configure(
        "TNotebook",
        background=BG_DARK,
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        background=BG_SIDEBAR,
        foreground=TEXT_MUTED,
        padding=(14, 7),
        font=FONT_BODY_BOLD
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", BG_CARD), ("active", BG_SURFACE)],
        foreground=[("selected", CYAN), ("active", TEXT_MAIN)]
    )

    # Scrollbars
    style.configure(
        "Vertical.TScrollbar",
        background=BG_SURFACE,
        troughcolor=BG_DARK,
        borderwidth=0,
        arrowsize=10
    )
    style.configure(
        "Horizontal.TScrollbar",
        background=BG_SURFACE,
        troughcolor=BG_DARK,
        borderwidth=0,
        arrowsize=10
    )

    # Progressbar
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor=BG_SURFACE,
        background=CYAN,
        borderwidth=0
    )
