#!/usr/bin/env python3
"""
================================================================================
   DSA Simulator — Capstone Interactive Data Structures Laboratory
   100% Python • Zero External Dependencies • Native Vector GUI & Offline
================================================================================
Run with:
    python main.py
"""

import sys
import os

# Ensure current directory is in python search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from gui.app import DSASimulatorApp


def main():
    print("==================================================================")
    print("  DSA Simulator — Capstone Interactive Data Structures Lab")
    print("  Initializing Native Python GUI (Tkinter Desktop Engine)...")
    print("  Running 100% locally and completely offline.")
    print("==================================================================")
    app = DSASimulatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
