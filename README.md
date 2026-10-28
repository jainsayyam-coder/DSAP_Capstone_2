# DSA Simulator — Interactive Data Structures Laboratory
### Capstone Project Edition • 100% Python • Zero Dependencies • Offline Desktop Engine

An interactive, dark-navy educational desktop software suite dedicated to mastering **Linked Lists**, **Binary Search Trees (BST)**, **Stacks**, and **Queues**. Built entirely in **pure Python** using the native standard library and vector Tkinter rendering engine, this application runs **100% locally and completely offline** on any system with zero pip dependencies or browser requirements.

---

## 🚀 Key Modules & Capstone Features

### 1. 4 Core Linked List Implementations
- **Singly Linked List (SLL):** Unidirectional node chain with `[DATA | NEXT]` cells terminating at `NULL`. Demonstrates $O(1)$ prepends and the $O(n)$ tail deletion paradox.
- **Doubly Linked List (DLL):** Bidirectional node chain with `[PREV | DATA | NEXT]` cells, enabling true $O(1)$ tail deletions and reverse traversals via `tail.prev`.
- **Circular Singly Linked List (CSLL):** Continuous closed ring where `tail.next == HEAD`. Traversals are protected by cycle-safety guards.
- **Circular Doubly Linked List (CDLL):** Seamless dual-direction circular loop with `tail.next == HEAD` and `HEAD.prev == TAIL` for instant round-trip traversal.

### 2. Interactive High-DPI Vector Canvas Visualizer
- **Crisp Custom Vector Rendering:** Renders node cards, address headers, and compartmentalized pointer fields (`DATA`, `NEXT`, `PREV`).
- **Dynamic Connection Arrows:** Directional forward arrows, bidirectional parallel arrows for DLL, and smooth curved loopback arcs for circular topologies.
- **Live Pointer Badges:** Visual indicator pills for `HEAD`, `TAIL`, `NULL`, `CURR`, and `NEW (Heap)`.
- **Interactive Node Click Inspector:** Click any node on the canvas to open a detailed memory inspector displaying simulated 64-bit heap addresses (`0x7ffe10...`), stored values, pointer dereferences, and 64-bit architecture memory breakdowns.

### 3. Binary Search Tree (BST) Laboratory
- **Dynamic 2D Coordinates Computation:** Tree layout algorithm automatically spaces nodes horizontally and vertically without branch overlaps.
- **Full Operational Suite:** Insert, Delete (handling leaf, single child, and dual-child in-order successor cases), Search, Find Min, and Find Max.
- **4 Animated Traversals:** 
  1. *In-Order Traversal (`Left → Root → Right`):* Produces monotonically ascending sorted sequence.
  2. *Pre-Order Traversal (`Root → Left → Right`):* Essential for tree cloning and serialization.
  3. *Post-Order Traversal (`Left → Right → Root`):* Bottom-up traversal used in node deletion and expression trees.
  4. *Level-Order Traversal (`Breadth-First Search / BFS`):* Level-by-level exploration using a FIFO queue.

### 4. Stack & Queue Visualizer Laboratories
- **Stack (LIFO):** Vertical memory cylinder with bounded capacity, slot indexing, and dynamic `TOP ->` pointer arrow indicator. Full overflow and underflow guards.
- **Queue (FIFO):** Horizontal conveyor structure with dedicated `FRONT ->` and `<- REAR` pointer tracking for enqueues and dequeues.

### 5. Step-by-Step Study Mode with Pseudocode Tracking
- Step through operations (Insert, Delete, Search, Reverse) with discrete snapshot states.
- Stepper controls: `⏮ First Step`, `◀ Previous Step`, `▶ Play / ⏸ Pause`, `Next Step ▶`, `⏭ Last Step`, `↺ Reset`.
- **Synchronized Pseudocode:** Highlights the active line of code in real time as the animation steps forward.
- **Pedagogical Explanation Cards:** "What is happening" and "⚠️ Why pointer order matters" safety cards highlighting memory leaks and orphaned node hazards.
- Configurable animation speed slider (`300ms` to `2200ms`).

### 6. Polyglot Algorithm & Multi-Language Code Viewer
- Clean implementations in **Python**, **C**, **C++**, **Java**, and language-independent **Pseudocode**.
- Highlights algorithmic invariants and memory management differences.
- One-click `📋 Copy Code` button to copy snippets directly to your clipboard.

### 7. Time & Space Complexity Comparison Matrix
- Comprehensive comparison table contrasting Dynamic Arrays, Singly Lists, Doubly Lists, Circular Singly, Circular Doubly, and BST.
- Color-coded complexity badges: Emerald for $O(1)$, Cyan for $O(\log n)$, Amber for $O(k)$ walks, and Rose for $O(n)$ shifts.
- Detailed theoretical analysis of the **"Delete Tail Paradox"** and pointer memory overhead (16 bytes/node on 64-bit systems).

### 8. Interactive Quiz & Assessment System
- Curated question bank across **Beginner**, **Intermediate**, and **Advanced** tiers.
- Formats: Pointer tracing, time complexity analysis, algorithm mechanics, and bug finding.
- Instant feedback with educational explanations for both correct and incorrect choices.
- Scores saved automatically to local offline storage.

### 9. Practice Challenge Mode with Automated Verification
- 8 hands-on interactive algorithmic challenges:
  1. *Insert at Position 3*
  2. *Delete a Specified Target Value*
  3. *Reverse a Singly Linked List (In-Place)*
  4. *Find the Middle Node (Tortoise & Hare two-pointer)*
  5. *Verify Circular Linkage*
  6. *Doubly Linked List Two-Way Deletion*
  7. *Detect a Cycle (Floyd's Algorithm)*
  8. *Merge Two Sorted Lists*
- Multi-tier hint drawer (up to 3 hints per challenge).
- Automated solution verification checking the student's live list against strict unit invariants.

### 10. Student Learning Portfolio & Offline Progress
- Tracks completed lessons, executed operations, quiz accuracy, and solved challenges.
- Persisted locally in `progress.json` with zero network telemetry or tracking.
- Visual completion percentage bar with reset option.

### 11. Automated Unit Test Runner
- Graphical test runner integrated directly into the desktop application with green/red status badges.
- 21 automated unit tests verifying correctness, invariants, edge cases, and bounds across all data structures.

---

## 📁 Pure Python Project Structure

```
DASP-PROJECT-gROUP-NO.4-main/
├── main.py                     # Primary GUI application launcher
├── simulator.py                # Standalone entry point alias
├── test_suite.py               # Complete automated unit test suite (21 unit tests)
├── progress.json               # Offline local progress & quiz persistence
├── run.bat                     # Windows one-click desktop launcher
├── README.md                   # Complete documentation
│
├── backend/                    # Core Algorithmic & Data Structure Engine
│   ├── __init__.py             # Exports all data structure models
│   ├── linked_list.py          # SLL, DLL, CSLL, CDLL implementations
│   ├── bst.py                  # Binary Search Tree with automated 2D coordinates
│   ├── stack.py                # Bounded LIFO Stack implementation
│   ├── queue.py                # Bounded FIFO Queue implementation
│   └── algorithm_tracer.py     # Step-by-step frame generator for Study Mode
│
└── gui/                        # Native Tkinter Desktop UI Engine
    ├── __init__.py
    ├── theme.py                # Modern dark-navy palette, typography, ttk styles
    ├── visualizer_canvas.py    # Vector canvas renderer (nodes, arrows, loops, trees, inspector)
    ├── view_home.py            # Dashboard overview & structure cards
    ├── view_simulator.py       # Operations lab with interactive node inspection
    ├── view_study.py           # Step-by-step study mode with pseudocode sync
    ├── view_tree.py            # BST visualizer with 4 animated traversals
    ├── view_stack_queue.py     # Stack & Queue visualizer
    ├── view_code.py            # Multi-language code viewer (Python, C, C++, Java, Pseudo)
    ├── view_complexity.py      # Asymptotic time and space matrix
    ├── view_quiz.py            # Interactive assessment system with difficulty tiers
    ├── view_challenges.py      # 8 practice challenges with automated verification
    ├── view_progress.py        # Student learning portfolio & progress dashboard
    ├── view_tests.py           # Graphical unit test runner
    └── app.py                  # Main window layout and sidebar navigation orchestrator
```

---

## 💻 How to Run Locally Offline

### Prerequisites
- **Python 3.8+** (Uses only Python's built-in standard library and Tkinter).
- **No external pip packages required** (Zero installation overhead).

### Quick Launch on Windows
Double-click `run.bat` in the project root folder.

### Launch via Terminal / PowerShell
```bash
python main.py
```
*(Alternatively: `python simulator.py`)*

### Run Automated Unit Tests via Terminal
```bash
python test_suite.py
```
*(or `python -m unittest test_suite.py`)*

---

## 🎓 Academic & Capstone Presentation Highlights

1. **100% Python Native Application:** Eliminated all external web dependencies (`.html`, `.css`, `.js`), creating a unified, robust, and offline Python desktop software.
2. **Pedagogical Pointer Visualizer:** Directly addresses student difficulty with pointers by making memory addresses (`0x7ffe10`), dereferences, and link order visually intuitive.
3. **The "Delete Tail Paradox":** Demonstrates both visually and analytically why Singly Linked Lists suffer from $O(n)$ tail deletions while Doubly Linked Lists achieve constant $O(1)$ time.
4. **Self-Contained Assessment Engine:** Includes 14 tier-filtered quiz questions and 8 challenge verification algorithms with persistent score tracking.
