"""
DSA Simulator - Interactive Visualizer Canvas
High-DPI vector rendering on Tkinter Canvas for Linked Lists, Trees, Stacks, and Queues.
Supports node click inspection, dynamic curved arrows, loopback arcs, and pointer badges.
"""

import tkinter as tk
from typing import List, Dict, Any, Optional, Callable
import math
from gui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BORDER, BORDER_LIGHT, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    CYAN, BLUE, PURPLE, EMERALD, AMBER, ROSE, GOLD,
    NODE_BG, NODE_BORDER, NODE_DATA_BG, NODE_HIGHLIGHT, NODE_FOUND,
    ARROW_FORWARD, ARROW_BACKWARD, ARROW_CIRCULAR,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_CODE, FONT_CODE_BOLD
)


class VisualizerCanvas(tk.Frame):
    """Interactive visual canvas that renders data structures with animated highlights and click inspection."""

    def __init__(self, parent, on_node_click: Optional[Callable[[Dict[str, Any]], None]] = None, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)
        self.on_node_click = on_node_click

        # Canvas with scrollbars
        self.canvas = tk.Canvas(
            self,
            bg=BG_DARK,
            highlightthickness=0,
            cursor="crosshair"
        )
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.hbar.grid(row=1, column=0, sticky="ew")
        self.vbar.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Pan and Zoom state
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.zoom_scale = 1.0

        # Clickable node regions
        self.node_hotspots: List[Dict[str, Any]] = []

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.canvas.bind("<Motion>", self._on_mouse_hover)

        # Drag tracking
        self._is_dragging = False
        self._press_x = 0
        self._press_y = 0

    # =========================================================================
    # Mouse Interaction (Pan & Click Inspection)
    # =========================================================================
    def _on_mouse_down(self, event):
        self._press_x = event.x
        self._press_y = event.y
        self._is_dragging = False
        self.canvas.scan_mark(event.x, event.y)

    def _on_mouse_drag(self, event):
        if abs(event.x - self._press_x) > 4 or abs(event.y - self._press_y) > 4:
            self._is_dragging = True
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mouse_up(self, event):
        if not self._is_dragging:
            # Check if clicked on a node hotspot
            canvas_x = self.canvas.canvasx(event.x)
            canvas_y = self.canvas.canvasy(event.y)
            for spot in self.node_hotspots:
                if spot["x1"] <= canvas_x <= spot["x2"] and spot["y1"] <= canvas_y <= spot["y2"]:
                    if self.on_node_click:
                        self.on_node_click(spot["data"])
                    break

    def _on_mouse_hover(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        hovered = False
        for spot in self.node_hotspots:
            if spot["x1"] <= canvas_x <= spot["x2"] and spot["y1"] <= canvas_y <= spot["y2"]:
                hovered = True
                break
        self.canvas.config(cursor="hand2" if hovered else "arrow")

    def reset_view(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    # =========================================================================
    # 1. LINKED LIST RENDERING
    # =========================================================================
    def render_linked_list(
        self,
        items: List[Any],
        list_type: str = "singly",
        highlight_index: int = -1,
        found_index: int = -1,
        active_pointers: Optional[Dict[str, int]] = None,
        floating_node: Optional[Any] = None,
        addresses: Optional[List[str]] = None
    ) -> None:
        """Render Singly, Doubly, Circular Singly, or Circular Doubly linked list."""
        self.canvas.delete("all")
        self.node_hotspots.clear()

        is_doubly = "doubly" in list_type.lower()
        is_circular = "circular" in list_type.lower()
        n = len(items)

        if n == 0 and floating_node is None:
            self.canvas.create_text(
                350, 150,
                text="Empty List\nHEAD = NULL | TAIL = NULL",
                fill=TEXT_MUTED,
                font=FONT_SUBHEADING,
                justify=tk.CENTER
            )
            self.canvas.config(scrollregion=(0, 0, 700, 300))
            return

        # Layout parameters
        node_w = 140 if is_doubly else 120
        node_h = 75
        spacing = 65
        start_x = 70
        start_y = 120

        # Generate deterministic addresses if not provided
        if not addresses or len(addresses) != n:
            addresses = [f"0x{0x7ffe10 + (i * 0x20):06x}" for i in range(n)]

        # Draw each node
        for i, val in enumerate(items):
            x = start_x + i * (node_w + spacing)
            y = start_y

            is_hl = (i == highlight_index)
            is_found = (i == found_index)
            border_col = NODE_FOUND if is_found else (NODE_HIGHLIGHT if is_hl else NODE_BORDER)
            bg_col = "#2d1a04" if is_hl else ("#062e1e" if is_found else NODE_BG)

            # Node card
            self._draw_round_rect(x, y, x + node_w, y + node_h, radius=10, fill=bg_col, outline=border_col, width=2)

            # Header: Address tag
            self.canvas.create_rectangle(x + 1, y + 1, x + node_w - 1, y + 22, fill=BG_CARD, outline="")
            self.canvas.create_text(x + node_w / 2, y + 11, text=addresses[i], fill=CYAN, font=FONT_SMALL)

            # Cell partitions
            content_y = y + 22
            content_h = node_h - 22

            if is_doubly:
                # [ PREV | DATA | NEXT ]
                col_w = node_w / 3.0
                # Dividers
                self.canvas.create_line(x + col_w, content_y, x + col_w, y + node_h, fill=BORDER)
                self.canvas.create_line(x + 2 * col_w, content_y, x + 2 * col_w, y + node_h, fill=BORDER)

                # PREV
                prev_text = addresses[i - 1][-4:] if i > 0 else (addresses[-1][-4:] if is_circular else "NULL")
                self.canvas.create_text(x + col_w / 2, content_y + 12, text="PREV", fill=PURPLE, font=FONT_SMALL)
                self.canvas.create_text(x + col_w / 2, content_y + 30, text=prev_text, fill=TEXT_MUTED, font=FONT_SMALL)

                # DATA
                self.canvas.create_text(x + 1.5 * col_w, content_y + content_h / 2, text=str(val), fill=TEXT_MAIN, font=FONT_HEADING)

                # NEXT
                next_text = addresses[i + 1][-4:] if i < n - 1 else (addresses[0][-4:] if is_circular else "NULL")
                self.canvas.create_text(x + 2.5 * col_w, content_y + 12, text="NEXT", fill=CYAN, font=FONT_SMALL)
                self.canvas.create_text(x + 2.5 * col_w, content_y + 30, text=next_text, fill=TEXT_MUTED, font=FONT_SMALL)
            else:
                # [ DATA | NEXT ]
                col_w = node_w * 0.6
                self.canvas.create_line(x + col_w, content_y, x + col_w, y + node_h, fill=BORDER)

                # DATA
                self.canvas.create_text(x + col_w / 2, content_y + content_h / 2, text=str(val), fill=TEXT_MAIN, font=FONT_HEADING)

                # NEXT
                next_text = addresses[i + 1][-4:] if i < n - 1 else (addresses[0][-4:] if is_circular else "NULL")
                self.canvas.create_text(x + col_w + (node_w - col_w) / 2, content_y + 14, text="NEXT", fill=CYAN, font=FONT_SMALL)
                self.canvas.create_text(x + col_w + (node_w - col_w) / 2, content_y + 32, text=next_text, fill=TEXT_MUTED, font=FONT_SMALL)

            # Node Hotspot for click inspection
            self.node_hotspots.append({
                "x1": x, "y1": y, "x2": x + node_w, "y2": y + node_h,
                "data": {
                    "index": i,
                    "value": val,
                    "address": addresses[i],
                    "next_addr": addresses[i + 1] if i < n - 1 else (addresses[0] if is_circular else "0x000000 (NULL)"),
                    "prev_addr": (addresses[i - 1] if i > 0 else (addresses[-1] if is_circular else "0x000000 (NULL)")) if is_doubly else None,
                    "list_type": list_type
                }
            })

            # Badges: HEAD, TAIL, Index
            if i == 0:
                self._draw_badge(x + 35, y - 22, "HEAD", CYAN)
            if i == n - 1:
                self._draw_badge(x + node_w - 35, y - 22, "TAIL", AMBER)

            self.canvas.create_text(x + node_w / 2, y + node_h + 16, text=f"Index {i}", fill=TEXT_DIM, font=FONT_SMALL)

            # Connecting Arrows between adjacent nodes
            if i < n - 1:
                next_x = start_x + (i + 1) * (node_w + spacing)
                if is_doubly:
                    # Forward arrow (top half)
                    self._draw_arrow(x + node_w, y + content_y - y + 14, next_x, y + content_y - y + 14, ARROW_FORWARD)
                    # Backward arrow (bottom half)
                    self._draw_arrow(next_x, y + content_y - y + 36, x + node_w, y + content_y - y + 36, ARROW_BACKWARD)
                else:
                    # Single forward arrow
                    self._draw_arrow(x + node_w, y + node_h / 2, next_x, y + node_h / 2, ARROW_FORWARD)

        # NULL pointer box for non-circular lists
        if not is_circular and n > 0:
            null_x = start_x + n * (node_w + spacing)
            null_y = start_y + (node_h - 36) / 2
            self._draw_arrow(start_x + (n - 1) * (node_w + spacing) + node_w, start_y + node_h / 2, null_x, start_y + node_h / 2, ARROW_FORWARD)
            self._draw_round_rect(null_x, null_y, null_x + 55, null_y + 36, radius=6, fill=BG_CARD, outline=BORDER)
            self.canvas.create_text(null_x + 27, null_y + 18, text="NULL", fill=ROSE, font=FONT_CODE_BOLD)

        # Circular Loopback Arc
        if is_circular and n > 0:
            tail_x = start_x + (n - 1) * (node_w + spacing) + node_w
            head_x = start_x
            arc_y = start_y + node_h + 45

            # TAIL -> HEAD loopback arc
            self.canvas.create_line(
                tail_x, start_y + node_h / 2,
                tail_x + 25, start_y + node_h / 2,
                tail_x + 25, arc_y,
                head_x - 25, arc_y,
                head_x - 25, start_y + node_h / 2,
                head_x, start_y + node_h / 2,
                fill=ARROW_CIRCULAR,
                width=2,
                arrow=tk.LAST,
                arrowshape=(10, 12, 5),
                smooth=True
            )
            self.canvas.create_text(
                (head_x + tail_x) / 2, arc_y + 14,
                text="↶ TAIL.next → HEAD (Circular Loop)",
                fill=ARROW_CIRCULAR,
                font=FONT_SMALL
            )

            # CDLL backward loopback (HEAD.prev -> TAIL)
            if is_doubly:
                top_arc_y = start_y - 45
                self.canvas.create_line(
                    head_x, start_y + node_h / 2 - 12,
                    head_x - 30, start_y + node_h / 2 - 12,
                    head_x - 30, top_arc_y,
                    tail_x + 30, top_arc_y,
                    tail_x + 30, start_y + node_h / 2 - 12,
                    tail_x, start_y + node_h / 2 - 12,
                    fill=PURPLE,
                    width=2,
                    arrow=tk.LAST,
                    arrowshape=(10, 12, 5),
                    smooth=True
                )
                self.canvas.create_text(
                    (head_x + tail_x) / 2, top_arc_y - 12,
                    text="HEAD.prev → TAIL ↷ (Backward Loop)",
                    fill=PURPLE,
                    font=FONT_SMALL
                )

        # Floating newNode for step-by-step animations
        if floating_node is not None:
            float_x = start_x + 100
            float_y = start_y - 80
            self._draw_round_rect(float_x, float_y, float_x + 110, float_y + 55, radius=8, fill="#1c2538", outline=CYAN, width=2)
            self.canvas.create_text(float_x + 55, float_y + 12, text="NEW NODE (Heap)", fill=CYAN, font=FONT_SMALL)
            self.canvas.create_text(float_x + 55, float_y + 35, text=str(floating_node), fill=TEXT_MAIN, font=FONT_HEADING)
            self.canvas.create_line(float_x + 55, float_y + 55, float_x + 55, start_y, fill=CYAN, width=1.5, dash=(4, 4), arrow=tk.LAST)

        # Update scrollregion
        total_w = max(start_x + (n + 1) * (node_w + spacing) + 100, 850)
        total_h = max(start_y + node_h + 120, 360)
        self.canvas.config(scrollregion=(0, 0, total_w, total_h))

    # =========================================================================
    # 2. BINARY SEARCH TREE RENDERING
    # =========================================================================
    def render_bst(
        self,
        bst_model,
        visited_nodes: Optional[List[int]] = None,
        current_node_val: Optional[int] = None
    ) -> None:
        """Render complete Binary Search Tree with connected branches and node coordinates."""
        self.canvas.delete("all")
        self.node_hotspots.clear()

        if not bst_model.root:
            self.canvas.create_text(
                400, 150,
                text="Empty Binary Search Tree\nRoot = NULL\nInsert numbers to grow the tree.",
                fill=TEXT_MUTED,
                font=FONT_SUBHEADING,
                justify=tk.CENTER
            )
            self.canvas.config(scrollregion=(0, 0, 800, 400))
            return

        # Ensure coordinates are fresh
        c_width = max(self.winfo_width(), 800)
        bst_model.compute_coordinates(canvas_width=c_width, top_y=60.0, level_height=70.0)

        visited_set = set(visited_nodes or [])

        # 1. Draw all connecting edges first
        def _draw_edges(node):
            if not node:
                return
            if node.left:
                self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill=BORDER_LIGHT, width=2)
                _draw_edges(node.left)
            if node.right:
                self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill=BORDER_LIGHT, width=2)
                _draw_edges(node.right)

        _draw_edges(bst_model.root)

        # 2. Draw nodes on top of edges
        r = 24  # node radius
        def _draw_nodes(node):
            if not node:
                return

            is_curr = (current_node_val is not None and node.value == current_node_val)
            is_vis = node.value in visited_set

            outline_col = GOLD if is_curr else (EMERALD if is_vis else CYAN)
            fill_col = "#382305" if is_curr else ("#062e1e" if is_vis else BG_CARD)

            self.canvas.create_oval(node.x - r, node.y - r, node.x + r, node.y + r, fill=fill_col, outline=outline_col, width=2.5 if is_curr else 1.5)
            self.canvas.create_text(node.x, node.y - 4, text=str(node.value), fill=TEXT_MAIN, font=FONT_HEADING)
            self.canvas.create_text(node.x, node.y + 11, text=node.address[-4:], fill=CYAN, font=FONT_SMALL)

            # Hotspot
            self.node_hotspots.append({
                "x1": node.x - r, "y1": node.y - r, "x2": node.x + r, "y2": node.y + r,
                "data": {
                    "value": node.value,
                    "address": node.address,
                    "left": node.left.value if node.left else "NULL",
                    "right": node.right.value if node.right else "NULL",
                    "level": node.level,
                    "structure": "Binary Search Tree Node"
                }
            })

            _draw_nodes(node.left)
            _draw_nodes(node.right)

        _draw_nodes(bst_model.root)

        # Scroll region
        max_y = max(bst_model.get_height() * 75 + 100, 400)
        self.canvas.config(scrollregion=(0, 0, max(c_width, 850), max_y))

    # =========================================================================
    # 3. STACK RENDERING
    # =========================================================================
    def render_stack(self, stack_items: List[Any], capacity: int = 7, top_index: int = -1) -> None:
        """Render vertical LIFO stack with slot chambers and TOP indicator."""
        self.canvas.delete("all")
        self.node_hotspots.clear()

        slot_w = 180
        slot_h = 36
        base_x = 300
        base_y = 320

        # Draw outer chamber
        total_h = capacity * slot_h
        chamber_top = base_y - total_h

        # Left, bottom, right walls
        self.canvas.create_line(base_x, chamber_top, base_x, base_y, fill=BORDER_LIGHT, width=3)
        self.canvas.create_line(base_x, base_y, base_x + slot_w, base_y, fill=BORDER_LIGHT, width=4)
        self.canvas.create_line(base_x + slot_w, chamber_top, base_x + slot_w, base_y, fill=BORDER_LIGHT, width=3)

        # Draw slots from bottom up
        for i in range(capacity):
            slot_y = base_y - (i + 1) * slot_h
            # Divider
            self.canvas.create_line(base_x, slot_y, base_x + slot_w, slot_y, fill=BORDER, dash=(2, 2))
            # Index label
            self.canvas.create_text(base_x - 30, slot_y + slot_h / 2, text=f"[{i}]", fill=TEXT_MUTED, font=FONT_SMALL)

            if i < len(stack_items):
                val = stack_items[i]
                is_top = (i == len(stack_items) - 1)
                bg_col = "#14304f" if is_top else BG_SURFACE
                outline_col = CYAN if is_top else BORDER

                self._draw_round_rect(base_x + 4, slot_y + 4, base_x + slot_w - 4, slot_y + slot_h - 4, radius=6, fill=bg_col, outline=outline_col)
                self.canvas.create_text(base_x + slot_w / 2, slot_y + slot_h / 2, text=str(val), fill=TEXT_MAIN, font=FONT_BODY_BOLD)

                if is_top:
                    # TOP arrow indicator
                    self._draw_arrow(base_x + slot_w + 50, slot_y + slot_h / 2, base_x + slot_w + 6, slot_y + slot_h / 2, CYAN)
                    self.canvas.create_text(base_x + slot_w + 80, slot_y + slot_h / 2, text="TOP", fill=CYAN, font=FONT_CODE_BOLD)

        # Empty slot indicator
        if not stack_items:
            self.canvas.create_text(base_x + slot_w / 2, base_y - total_h / 2, text="Stack Empty\n(TOP = -1)", fill=TEXT_MUTED, font=FONT_SUBHEADING, justify=tk.CENTER)

        self.canvas.config(scrollregion=(0, 0, 750, 400))

    # =========================================================================
    # 4. QUEUE RENDERING
    # =========================================================================
    def render_queue(self, queue_items: List[Any], capacity: int = 7) -> None:
        """Render horizontal FIFO queue with FRONT and REAR indicators."""
        self.canvas.delete("all")
        self.node_hotspots.clear()

        slot_w = 65
        slot_h = 60
        start_x = 120
        y = 140

        # Draw conveyor top and bottom rails
        total_w = capacity * slot_w
        self.canvas.create_line(start_x, y, start_x + total_w, y, fill=BORDER_LIGHT, width=3)
        self.canvas.create_line(start_x, y + slot_h, start_x + total_w, y + slot_h, fill=BORDER_LIGHT, width=3)

        for i in range(capacity):
            x = start_x + i * slot_w
            self.canvas.create_line(x, y, x, y + slot_h, fill=BORDER, dash=(2, 2))
            self.canvas.create_text(x + slot_w / 2, y + slot_h + 16, text=f"[{i}]", fill=TEXT_MUTED, font=FONT_SMALL)

            if i < len(queue_items):
                val = queue_items[i]
                is_front = (i == 0)
                is_rear = (i == len(queue_items) - 1)

                bg_col = "#0c2c38" if is_front else ("#281b3d" if is_rear else BG_SURFACE)
                outline_col = CYAN if is_front else (PURPLE if is_rear else BORDER)

                self._draw_round_rect(x + 3, y + 4, x + slot_w - 3, y + slot_h - 4, radius=6, fill=bg_col, outline=outline_col)
                self.canvas.create_text(x + slot_w / 2, y + slot_h / 2, text=str(val), fill=TEXT_MAIN, font=FONT_BODY_BOLD)

                if is_front:
                    self._draw_arrow(x + slot_w / 2, y - 35, x + slot_w / 2, y - 4, CYAN)
                    self.canvas.create_text(x + slot_w / 2, y - 44, text="FRONT", fill=CYAN, font=FONT_CODE_BOLD)
                if is_rear:
                    self._draw_arrow(x + slot_w / 2, y + slot_h + 50, x + slot_w / 2, y + slot_h + 26, PURPLE)
                    self.canvas.create_text(x + slot_w / 2, y + slot_h + 60, text="REAR", fill=PURPLE, font=FONT_CODE_BOLD)

        if not queue_items:
            self.canvas.create_text(start_x + total_w / 2, y + slot_h / 2, text="Queue Empty", fill=TEXT_MUTED, font=FONT_SUBHEADING)

        self.canvas.config(scrollregion=(0, 0, start_x + total_w + 120, 320))

    # =========================================================================
    # Drawing Utilities
    # =========================================================================
    def _draw_round_rect(self, x1, y1, x2, y2, radius=8, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def _draw_arrow(self, x1, y1, x2, y2, color):
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=2,
            arrow=tk.LAST,
            arrowshape=(8, 10, 4)
        )

    def _draw_badge(self, x, y, text, color):
        w = len(text) * 8 + 14
        h = 18
        self._draw_round_rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, radius=5, fill=color, outline="")
        self.canvas.create_text(x, y, text=text, fill="#000000", font=FONT_CODE_BOLD)
