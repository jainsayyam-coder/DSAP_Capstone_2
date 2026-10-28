"""
DSA Simulator - Multi-Language Code & Algorithm Viewer View
Reference implementations in Python, C, C++, Java, and Pseudocode
with syntax highlighting and clipboard export.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BG_INPUT, BORDER, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD, FONT_CODE_LG
)

CODE_LIBRARY = {
    ("singly", "insert_beginning"): {
        "Python": """class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def insert_beginning(self, val):
    new_node = Node(val)
    new_node.next = self.head  # 1. Wire new node to current head
    self.head = new_node       # 2. Advance head pointer to new node
    if self.tail is None:      # 3. Handle initially empty list
        self.tail = new_node
    self.length += 1
    # Time Complexity: O(1) Constant Time
    # Space Complexity: O(1) Auxiliary Space""",
        "C": """struct Node {
    int val;
    struct Node* next;
};

void insert_beginning(struct Node** head_ref, int val) {
    // 1. Allocate heap memory for new node
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    new_node->val = val;
    
    // 2. Wire new node to current head
    new_node->next = (*head_ref);
    
    // 3. Move head pointer to new node
    (*head_ref) = new_node;
    // Time: O(1), Space: O(1)
}""",
        "C++": """struct Node {
    int val;
    Node* next;
    Node(int v) : val(v), next(nullptr) {}
};

void insertBeginning(Node*& head, int val) {
    Node* newNode = new Node(val);
    newNode->next = head;
    head = newNode;
}""",
        "Java": """class Node {
    int val;
    Node next;
    Node(int val) { this.val = val; }
}

public void insertBeginning(int val) {
    Node newNode = new Node(val);
    newNode.next = head;
    head = newNode;
    if (tail == null) tail = newNode;
    length++;
}""",
        "Pseudocode": """ALGORITHM InsertBeginning(head, val):
    1. newNode ← allocate Node(val)
    2. newNode.next ← head
    3. head ← newNode
    4. if tail == NULL then tail ← newNode
    5. return head"""
    },
    ("singly", "delete_end"): {
        "Python": """def delete_end(self):
    if not self.head:
        return None  # Underflow
    if self.head == self.tail:
        val = self.head.val
        self.head = self.tail = None
        self.length = 0
        return val

    # THE PARADOX: Must walk entire chain from head to find second-to-last node!
    curr = self.head
    while curr.next != self.tail:
        curr = curr.next

    val = self.tail.val
    curr.next = None
    self.tail = curr
    self.length -= 1
    return val  # Time: O(n) Linear Time!""",
        "C": """int delete_end(struct Node** head_ref) {
    if (*head_ref == NULL) return -1;
    if ((*head_ref)->next == NULL) {
        int val = (*head_ref)->val;
        free(*head_ref);
        *head_ref = NULL;
        return val;
    }
    struct Node* curr = *head_ref;
    while (curr->next->next != NULL) {
        curr = curr->next;
    }
    int val = curr->next->val;
    free(curr->next);
    curr->next = NULL;
    return val;
}""",
        "C++": """int deleteEnd(Node*& head) {
    if (!head) return -1;
    if (!head->next) {
        int v = head->val;
        delete head;
        head = nullptr;
        return v;
    }
    Node* curr = head;
    while (curr->next->next) curr = curr->next;
    int v = curr->next->val;
    delete curr->next;
    curr->next = nullptr;
    return v;
}""",
        "Java": """public Integer deleteEnd() {
    if (head == null) return null;
    if (head == tail) {
        int v = head.val;
        head = tail = null;
        length = 0;
        return v;
    }
    Node curr = head;
    while (curr.next != tail) curr = curr.next;
    int v = tail.val;
    curr.next = null;
    tail = curr;
    length--;
    return v;
}""",
        "Pseudocode": """ALGORITHM DeleteEnd(head, tail):
    1. if head == NULL then return UNDERFLOW
    2. if head == tail then head ← tail ← NULL; return
    3. curr ← head
    4. while curr.next ≠ tail do:
    5.     curr ← curr.next
    6. val ← tail.val
    7. curr.next ← NULL
    8. tail ← curr
    9. return val (O(n) time)"""
    },
    ("singly", "reverse"): {
        "Python": """def reverse(self):
    prev = None
    curr = self.head
    self.tail = self.head
    while curr:
        next_temp = curr.next  # 1. Save forward address
        curr.next = prev       # 2. Invert link to point backward
        prev = curr            # 3. Advance prev
        curr = next_temp       # 4. Advance curr
    self.head = prev           # 5. Update head to old tail
    # Time: O(n) | Space: O(1) in-place!""",
        "C": """void reverse(struct Node** head_ref) {
    struct Node* prev = NULL;
    struct Node* curr = *head_ref;
    struct Node* next = NULL;
    while (curr != NULL) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    *head_ref = prev;
}""",
        "C++": """void reverse(Node*& head) {
    Node* prev = nullptr;
    Node* curr = head;
    while (curr) {
        Node* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    head = prev;
}""",
        "Java": """public void reverse() {
    Node prev = null;
    Node curr = head;
    tail = head;
    while (curr != null) {
        Node next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    head = prev;
}""",
        "Pseudocode": """ALGORITHM ReverseInPlace(head):
    1. prev ← NULL, curr ← head
    2. while curr ≠ NULL do:
    3.     nextTemp ← curr.next
    4.     curr.next ← prev
    5.     prev ← curr
    6.     curr ← nextTemp
    7. head ← prev
    8. return head"""
    },
    ("doubly", "delete_end"): {
        "Python": """def delete_end(self):
    if not self.tail:
        return None  # Underflow
    val = self.tail.val
    if self.head == self.tail:
        self.head = self.tail = None
    else:
        # THE ADVANTAGE: Direct O(1) access to predecessor!
        self.tail = self.tail.prev
        self.tail.next = None
    self.length -= 1
    return val  # Strictly O(1) Constant Time!""",
        "C": """int delete_end_doubly(struct DNode** head_ref, struct DNode** tail_ref) {
    if (*tail_ref == NULL) return -1;
    struct DNode* old_tail = *tail_ref;
    int val = old_tail->val;
    if (*head_ref == *tail_ref) {
        *head_ref = *tail_ref = NULL;
    } else {
        *tail_ref = (*tail_ref)->prev;
        (*tail_ref)->next = NULL;
    }
    free(old_tail);
    return val;
}""",
        "C++": """int deleteEnd(DNode*& head, DNode*& tail) {
    if (!tail) return -1;
    int v = tail->val;
    if (head == tail) {
        delete tail;
        head = tail = nullptr;
    } else {
        tail = tail->prev;
        delete tail->next;
        tail->next = nullptr;
    }
    return v;
}""",
        "Java": """public Integer deleteEnd() {
    if (tail == null) return null;
    int v = tail.val;
    if (head == tail) {
        head = tail = null;
    } else {
        tail = tail.prev;
        tail.next = null;
    }
    length--;
    return v;
}""",
        "Pseudocode": """ALGORITHM DoublyDeleteEnd(head, tail):
    1. if tail == NULL then return UNDERFLOW
    2. val ← tail.val
    3. if head == tail then head ← tail ← NULL
    4. else:
    5.     tail ← tail.prev
    6.     tail.next ← NULL
    7. return val (O(1) time)"""
    }
}


class CodeView(tk.Frame):
    """Polyglot Algorithm and Code Viewer with multi-language tabs and copy functionality."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.app = app
        self.selected_lang = "Python"
        self._build_ui()
        self.render_code()

    def _build_ui(self):
        # 1. Top Filters Bar
        ctrl_bar = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=10)
        ctrl_bar.pack(fill=tk.X, padx=14, pady=(12, 10))

        tk.Label(ctrl_bar, text="Structure:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 4))
        self.combo_type = ttk.Combobox(
            ctrl_bar,
            values=["Singly Linked List", "Doubly Linked List"],
            state="readonly",
            width=18
        )
        self.combo_type.current(0)
        self.combo_type.pack(side=tk.LEFT, padx=(0, 12))
        self.combo_type.bind("<<ComboboxSelected>>", lambda e: self.render_code())

        tk.Label(ctrl_bar, text="Operation:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 4))
        self.combo_op = ttk.Combobox(
            ctrl_bar,
            values=["Insert at Beginning", "Delete from End (Paradox)", "Reverse In-Place"],
            state="readonly",
            width=26
        )
        self.combo_op.current(0)
        self.combo_op.pack(side=tk.LEFT, padx=(0, 12))
        self.combo_op.bind("<<ComboboxSelected>>", lambda e: self.render_code())

        # Copy button
        tk.Button(
            ctrl_bar,
            text="📋 Copy Code",
            bg=BLUE,
            fg="#ffffff",
            font=FONT_BODY_BOLD,
            relief=tk.FLAT,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.copy_to_clipboard
        ).pack(side=tk.RIGHT)

        # 2. Language Selection Tabs Bar
        lang_bar = tk.Frame(self, bg=BG_DARK)
        lang_bar.pack(fill=tk.X, padx=14, pady=(0, 6))

        self.lang_buttons = {}
        langs = ["Python", "C", "C++", "Java", "Pseudocode"]
        for lang in langs:
            btn = tk.Button(
                lang_bar,
                text=lang,
                bg=BG_SURFACE if lang != self.selected_lang else BLUE,
                fg=TEXT_MAIN if lang != self.selected_lang else "#ffffff",
                font=FONT_BODY_BOLD,
                relief=tk.FLAT,
                padx=14,
                pady=4,
                cursor="hand2",
                command=lambda l=lang: self.select_language(l)
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.lang_buttons[lang] = btn

        # 3. Main Code Display Box
        code_container = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12)
        code_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        self.txt_code = tk.Text(
            code_container,
            bg=BG_INPUT,
            fg=TEXT_MAIN,
            font=FONT_CODE_LG,
            relief=tk.FLAT,
            padx=14,
            pady=14,
            wrap=tk.NONE
        )
        v_scroll = ttk.Scrollbar(code_container, orient=tk.VERTICAL, command=self.txt_code.yview)
        h_scroll = ttk.Scrollbar(code_container, orient=tk.HORIZONTAL, command=self.txt_code.xview)
        self.txt_code.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        self.txt_code.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        code_container.rowconfigure(0, weight=1)
        code_container.columnconfigure(0, weight=1)

        # Syntax tags
        self.txt_code.tag_configure("comment", foreground=TEXT_DIM)
        self.txt_code.tag_configure("keyword", foreground=PURPLE)
        self.txt_code.tag_configure("highlight", foreground=CYAN)

    def select_language(self, lang: str):
        self.selected_lang = lang
        for name, btn in self.lang_buttons.items():
            if name == lang:
                btn.config(bg=BLUE, fg="#ffffff")
            else:
                btn.config(bg=BG_SURFACE, fg=TEXT_MAIN)
        self.render_code()

    def render_code(self):
        st_text = self.combo_type.get()
        op_text = self.combo_op.get()

        st_key = "doubly" if "Doubly" in st_text else "singly"
        if "Delete" in op_text:
            op_key = "delete_end"
        elif "Reverse" in op_text:
            op_key = "reverse"
        else:
            op_key = "insert_beginning"

        entry = CODE_LIBRARY.get((st_key, op_key))
        if not entry or self.selected_lang not in entry:
            # Fallback
            entry = CODE_LIBRARY.get(("singly", "insert_beginning"))

        code = entry.get(self.selected_lang, "// Code not available for this combination.")

        self.txt_code.config(state=tk.NORMAL)
        self.txt_code.delete("1.0", tk.END)
        self.txt_code.insert(tk.END, code)

        # Apply simple syntax colorings
        for line_num, line in enumerate(code.split("\n"), start=1):
            if line.strip().startswith(("#", "//")):
                self.txt_code.tag_add("comment", f"{line_num}.0", f"{line_num}.end")

        self.txt_code.config(state=tk.DISABLED)

    def copy_to_clipboard(self):
        code = self.txt_code.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(code)
        messagebox.showinfo("Copied", f"Copied {self.selected_lang} implementation to clipboard!")
