"""
DSA Simulator - Algorithm Tracer & Study Mode Step Engine
Generates detailed step-by-step frames with pseudocode line numbers,
active pointers, explanations, and safety warnings for every operation.
"""

from typing import List, Dict, Any, Optional
import copy


def get_operation_steps(
    structure_type: str,
    operation: str,
    initial_items: List[Any],
    val: Any = 42,
    pos: int = 1
) -> Dict[str, Any]:
    """
    Generate step-by-step playback frames for Study Mode.
    Returns:
    {
        "title": str,
        "complexity_time": str,
        "complexity_space": str,
        "pseudocode": List[str],
        "steps": [
            {
                "step_number": int,
                "pseudo_line": int,
                "title": str,
                "description": str,
                "why_it_matters": str,
                "items": List[Any],
                "active_indices": List[int],
                "pointers": Dict[str, int], # e.g. {"HEAD": 0, "CURR": 2, "NEW": -1}
                "new_node_value": Any,
                "status_badge": str
            }
        ]
    }
    """
    st = structure_type.lower().replace("-", "_").replace(" ", "_")
    op = operation.lower().replace("-", "_").replace(" ", "_")
    items = list(initial_items)
    n = len(items)

    # =========================================================================
    # 1. SINGLY LINKED LIST (SLL)
    # =========================================================================
    if "singly" in st and "circular" not in st:
        if op in ("insert_beginning", "insertbeg"):
            pseudo = [
                "1. newNode ← allocate Node(val)",
                "2. newNode.next ← HEAD",
                "3. HEAD ← newNode",
                "4. if TAIL == NULL then TAIL ← newNode",
                "5. length ← length + 1"
            ]
            steps = [
                {
                    "step_number": 1,
                    "pseudo_line": 0,
                    "title": "Allocate New Node",
                    "description": f"Allocate dynamic heap memory for new node with value {val}. newNode.next is initialized to NULL.",
                    "why_it_matters": "Heap nodes must be instantiated and populated with data before any pointer wiring begins.",
                    "items": list(items),
                    "active_indices": [],
                    "pointers": {"HEAD": 0 if n else -1, "NEW": -99},
                    "new_node_value": val,
                    "status_badge": "O(1) Allocation"
                },
                {
                    "step_number": 2,
                    "pseudo_line": 1,
                    "title": "Wire newNode.next to Current HEAD",
                    "description": f"Set newNode.next = HEAD ({items[0] if n else 'NULL'}).",
                    "why_it_matters": "CRITICAL ORDER: You MUST connect newNode.next to HEAD before moving HEAD itself! Otherwise, the rest of the list becomes orphaned and causes a memory leak.",
                    "items": list(items),
                    "active_indices": [0] if n else [],
                    "pointers": {"HEAD": 0 if n else -1, "NEW": -99},
                    "new_node_value": val,
                    "status_badge": "Pointer Relink"
                },
                {
                    "step_number": 3,
                    "pseudo_line": 2,
                    "title": "Advance HEAD Pointer",
                    "description": f"Update HEAD to reference the newNode ({val}).",
                    "why_it_matters": "HEAD now officially designates the new node as the primary entry point to the list.",
                    "items": [val] + list(items),
                    "active_indices": [0],
                    "pointers": {"HEAD": 0, "TAIL": len(items)},
                    "new_node_value": None,
                    "status_badge": "HEAD Relinked"
                },
                {
                    "step_number": 4,
                    "pseudo_line": 4,
                    "title": "Operation Complete",
                    "description": f"List successfully updated. New length is {len(items) + 1}.",
                    "why_it_matters": "Because no nodes needed to be shifted or traversed, prepending is strictly O(1) constant time.",
                    "items": [val] + list(items),
                    "active_indices": [0],
                    "pointers": {"HEAD": 0, "TAIL": len(items)},
                    "new_node_value": None,
                    "status_badge": "Finished (O(1))"
                }
            ]
            return {
                "title": "Singly Linked List: Insert at Beginning",
                "complexity_time": "O(1) Constant Time",
                "complexity_space": "O(1) Auxiliary Space",
                "pseudocode": pseudo,
                "steps": steps
            }

        elif op in ("insert_end", "append"):
            pseudo = [
                "1. newNode ← allocate Node(val)",
                "2. if HEAD == NULL then HEAD ← TAIL ← newNode; return",
                "3. TAIL.next ← newNode",
                "4. TAIL ← newNode",
                "5. length ← length + 1"
            ]
            steps = [
                {
                    "step_number": 1,
                    "pseudo_line": 0,
                    "title": "Allocate New Node",
                    "description": f"Instantiate node with value {val}. Its next pointer defaults to NULL.",
                    "why_it_matters": "Every new element requires an independent node allocation on the heap.",
                    "items": list(items),
                    "active_indices": [],
                    "pointers": {"HEAD": 0, "TAIL": n - 1, "NEW": -99},
                    "new_node_value": val,
                    "status_badge": "Allocation"
                },
                {
                    "step_number": 2,
                    "pseudo_line": 2,
                    "title": "Connect TAIL.next to newNode",
                    "description": f"Update existing tail node ({items[-1] if n else 'NULL'}).next to point to {val}.",
                    "why_it_matters": "Maintained tail pointer allows instant O(1) connection without having to walk the entire chain from HEAD.",
                    "items": list(items),
                    "active_indices": [n - 1] if n else [],
                    "pointers": {"HEAD": 0, "TAIL": n - 1, "NEW": -99},
                    "new_node_value": val,
                    "status_badge": "Tail Linked"
                },
                {
                    "step_number": 3,
                    "pseudo_line": 3,
                    "title": "Advance TAIL Pointer",
                    "description": f"Move TAIL pointer to the new node ({val}). TAIL.next is NULL.",
                    "why_it_matters": "The list invariants are restored: TAIL points to the last valid node, and its next is NULL.",
                    "items": list(items) + [val],
                    "active_indices": [len(items)],
                    "pointers": {"HEAD": 0, "TAIL": len(items)},
                    "new_node_value": None,
                    "status_badge": "Complete (O(1))"
                }
            ]
            return {
                "title": "Singly Linked List: Insert at End",
                "complexity_time": "O(1) Constant Time (with Tail pointer)",
                "complexity_space": "O(1) Auxiliary Space",
                "pseudocode": pseudo,
                "steps": steps
            }

        elif op in ("insert_at", "insert_pos"):
            idx = max(0, min(pos, n))
            pseudo = [
                "1. validate index in [0, length]",
                "2. if index == 0 then insertBeginning(val); return",
                "3. prev ← HEAD; walk index - 1 steps",
                "4. newNode ← allocate Node(val)",
                "5. newNode.next ← prev.next",
                "6. prev.next ← newNode"
            ]
            walk_idx = max(0, idx - 1)
            steps = [
                {
                    "step_number": 1,
                    "pseudo_line": 2,
                    "title": "Traverse to Predecessor Node",
                    "description": f"Walk from HEAD to index {walk_idx} (node containing {items[walk_idx] if walk_idx < n else 'N/A'}).",
                    "why_it_matters": "In a singly linked list, we cannot splice a node without reaching its immediate predecessor.",
                    "items": list(items),
                    "active_indices": [walk_idx],
                    "pointers": {"HEAD": 0, "PREV": walk_idx},
                    "new_node_value": None,
                    "status_badge": f"Walking O(k)"
                },
                {
                    "step_number": 2,
                    "pseudo_line": 3,
                    "title": "Allocate New Node",
                    "description": f"Create newNode({val}) to be spliced between index {walk_idx} and index {idx}.",
                    "why_it_matters": "Node is created before altering existing neighbor references.",
                    "items": list(items),
                    "active_indices": [walk_idx],
                    "pointers": {"HEAD": 0, "PREV": walk_idx, "NEW": -99},
                    "new_node_value": val,
                    "status_badge": "Allocated"
                },
                {
                    "step_number": 3,
                    "pseudo_line": 4,
                    "title": "Point newNode.next to Successor",
                    "description": f"Set newNode.next = prev.next ({items[idx] if idx < n else 'NULL'}).",
                    "why_it_matters": "CRITICAL ORDER: newNode must capture the successor address BEFORE prev.next is overwritten, otherwise the remaining subchain is lost permanently.",
                    "items": list(items),
                    "active_indices": [walk_idx],
                    "pointers": {"HEAD": 0, "PREV": walk_idx, "NEW": -99},
                    "new_node_value": val,
                    "status_badge": "Successor Linked"
                },
                {
                    "step_number": 4,
                    "pseudo_line": 5,
                    "title": "Point prev.next to newNode",
                    "description": f"Splice complete: prev.next now points to {val}.",
                    "why_it_matters": "The splice is complete. The chain now flows continuously through the newly inserted node.",
                    "items": items[:idx] + [val] + items[idx:],
                    "active_indices": [idx],
                    "pointers": {"HEAD": 0, "CURR": idx, "TAIL": len(items)},
                    "new_node_value": None,
                    "status_badge": "Complete (O(k))"
                }
            ]
            return {
                "title": f"Singly Linked List: Insert at Index {idx}",
                "complexity_time": "O(k) Traversal Time",
                "complexity_space": "O(1) Auxiliary Space",
                "pseudocode": pseudo,
                "steps": steps
            }

        elif op in ("delete_beginning", "deletebeg"):
            pseudo = [
                "1. if HEAD == NULL then return NULL (underflow)",
                "2. targetNode ← HEAD",
                "3. HEAD ← HEAD.next",
                "4. targetNode.next ← NULL; free(targetNode)",
                "5. length ← length - 1"
            ]
            new_items = items[1:] if n > 1 else []
            steps = [
                {
                    "step_number": 1,
                    "pseudo_line": 1,
                    "title": "Mark Target Node",
                    "description": f"Identify current HEAD node ({items[0] if n else 'NULL'}) for removal.",
                    "why_it_matters": "Keep a temporary pointer so we can reclaim memory or return the deleted value.",
                    "items": list(items),
                    "active_indices": [0] if n else [],
                    "pointers": {"HEAD": 0, "TARGET": 0},
                    "new_node_value": None,
                    "status_badge": "Target Identified"
                },
                {
                    "step_number": 2,
                    "pseudo_line": 2,
                    "title": "Advance HEAD to Successor",
                    "description": f"Move HEAD pointer forward to HEAD.next ({items[1] if n > 1 else 'NULL'}).",
                    "why_it_matters": "The first node is immediately detached from the chain in O(1) time.",
                    "items": new_items,
                    "active_indices": [0] if new_items else [],
                    "pointers": {"HEAD": 0 if new_items else -1, "TAIL": len(new_items) - 1 if new_items else -1},
                    "new_node_value": None,
                    "status_badge": "HEAD Advanced"
                },
                {
                    "step_number": 3,
                    "pseudo_line": 3,
                    "title": "Memory Reclamation",
                    "description": f"Old head node with value {items[0] if n else ''} is released.",
                    "why_it_matters": "Properly zeroing out pointers prevents dangling pointer bugs.",
                    "items": new_items,
                    "active_indices": [],
                    "pointers": {"HEAD": 0 if new_items else -1, "TAIL": len(new_items) - 1 if new_items else -1},
                    "new_node_value": None,
                    "status_badge": "Finished (O(1))"
                }
            ]
            return {
                "title": "Singly Linked List: Delete from Beginning",
                "complexity_time": "O(1) Constant Time",
                "complexity_space": "O(1) Auxiliary Space",
                "pseudocode": pseudo,
                "steps": steps
            }

        elif op in ("reverse", "reversal"):
            pseudo = [
                "1. prev ← NULL, curr ← HEAD",
                "2. while curr ≠ NULL do:",
                "3.     nextTemp ← curr.next",
                "4.     curr.next ← prev",
                "5.     prev ← curr",
                "6.     curr ← nextTemp",
                "7. HEAD ← prev"
            ]
            steps = []
            rev_items = list(items)
            steps.append({
                "step_number": 1,
                "pseudo_line": 0,
                "title": "Initialize Three Pointers",
                "description": "Setup prev = NULL, curr = HEAD, nextTemp = NULL. We will reverse one link at a time.",
                "why_it_matters": "In-place reversal requires 3 simultaneous pointer references to avoid losing the rest of the chain.",
                "items": list(items),
                "active_indices": [0] if n else [],
                "pointers": {"HEAD": 0, "CURR": 0, "PREV": -1},
                "new_node_value": None,
                "status_badge": "Setup"
            })
            for i in range(min(n, 4)):
                steps.append({
                    "step_number": len(steps) + 1,
                    "pseudo_line": 3,
                    "title": f"Invert Link at Node {items[i]}",
                    "description": f"Store curr.next, invert pointer to point backward to prev ({items[i-1] if i > 0 else 'NULL'}), advance prev and curr.",
                    "why_it_matters": f"Node {items[i]} now points left instead of right.",
                    "items": list(items),
                    "active_indices": [i],
                    "pointers": {"CURR": i, "PREV": i - 1 if i > 0 else -1},
                    "new_node_value": None,
                    "status_badge": f"Relink Step {i+1}"
                })
            steps.append({
                "step_number": len(steps) + 1,
                "pseudo_line": 6,
                "title": "Reversal Complete",
                "description": f"HEAD is now updated to the former TAIL ({items[-1] if n else 'NULL'}).",
                "why_it_matters": "All pointer directions are completely inverted in-place in O(n) time and O(1) extra space.",
                "items": list(reversed(items)),
                "active_indices": [0],
                "pointers": {"HEAD": 0, "TAIL": len(items) - 1},
                "new_node_value": None,
                "status_badge": "Reversed (O(n))"
            })
            return {
                "title": "Singly Linked List: In-Place Reversal",
                "complexity_time": "O(n) Linear Time",
                "complexity_space": "O(1) Auxiliary Space",
                "pseudocode": pseudo,
                "steps": steps
            }

    # =========================================================================
    # 2. DOUBLY LINKED LIST (DLL)
    # =========================================================================
    elif "doubly" in st and "circular" not in st:
        if op in ("delete_end", "deleteend", "pop"):
            pseudo = [
                "1. if TAIL == NULL then return NULL (empty)",
                "2. val ← TAIL.value",
                "3. if HEAD == TAIL then HEAD ← TAIL ← NULL",
                "4. else:",
                "5.     TAIL ← TAIL.prev",
                "6.     TAIL.next ← NULL",
                "7. return val"
            ]
            del_val = items[-1] if n else None
            new_items = items[:-1]
            steps = [
                {
                    "step_number": 1,
                    "pseudo_line": 0,
                    "title": "Inspect TAIL and TAIL.prev",
                    "description": f"Because this is a Doubly Linked List, TAIL ({del_val}) contains a direct .prev reference to {items[-2] if n > 1 else 'NULL'}.",
                    "why_it_matters": "THE PARADOX SOLVED: In SLL, deleting tail is O(n) because you must walk from head. In DLL, tail.prev is immediately available in O(1)!",
                    "items": list(items),
                    "active_indices": [n - 1] if n else [],
                    "pointers": {"HEAD": 0, "TAIL": n - 1, "PREV": n - 2 if n > 1 else -1},
                    "new_node_value": None,
                    "status_badge": "O(1) Direct Access"
                },
                {
                    "step_number": 2,
                    "pseudo_line": 4,
                    "title": "Retract TAIL to TAIL.prev",
                    "description": f"Move TAIL pointer to the predecessor node ({items[-2] if n > 1 else 'NULL'}).",
                    "why_it_matters": "No traversal required! Constant time O(1) pointer adjustment.",
                    "items": new_items,
                    "active_indices": [len(new_items) - 1] if new_items else [],
                    "pointers": {"HEAD": 0 if new_items else -1, "TAIL": len(new_items) - 1 if new_items else -1},
                    "new_node_value": None,
                    "status_badge": "TAIL Retracted"
                },
                {
                    "step_number": 3,
                    "pseudo_line": 5,
                    "title": "Sever Forward Link (TAIL.next = NULL)",
                    "description": "Set the new TAIL's next pointer to NULL, severing all connections to the discarded node.",
                    "why_it_matters": "Maintains DLL invariant: TAIL.next must always equal NULL in a non-circular list.",
                    "items": new_items,
                    "active_indices": [len(new_items) - 1] if new_items else [],
                    "pointers": {"HEAD": 0 if new_items else -1, "TAIL": len(new_items) - 1 if new_items else -1},
                    "new_node_value": None,
                    "status_badge": "Complete (O(1))"
                }
            ]
            return {
                "title": "Doubly Linked List: Delete from End",
                "complexity_time": "O(1) Constant Time (via tail.prev)",
                "complexity_space": "O(1) Auxiliary Space",
                "pseudocode": pseudo,
                "steps": steps
            }

    # =========================================================================
    # 3. CIRCULAR LINKED LISTS (CSLL / CDLL)
    # =========================================================================
    elif "circular" in st:
        pseudo = [
            "1. newNode ← allocate Node(val)",
            "2. if HEAD == NULL then",
            "3.     HEAD ← TAIL ← newNode",
            "4.     newNode.next ← newNode (self-loop)",
            "5. else:",
            "6.     newNode.next ← HEAD",
            "7.     TAIL.next ← newNode",
            "8.     HEAD ← newNode (or TAIL ← newNode for append)"
        ]
        steps = [
            {
                "step_number": 1,
                "pseudo_line": 0,
                "title": "Allocate Circular Node",
                "description": f"Create node with value {val}.",
                "why_it_matters": "Circular lists require uninterrupted closed loops.",
                "items": list(items),
                "active_indices": [],
                "pointers": {"HEAD": 0, "TAIL": n - 1, "NEW": -99},
                "new_node_value": val,
                "status_badge": "Allocated"
            },
            {
                "step_number": 2,
                "pseudo_line": 5,
                "title": "Connect newNode.next to HEAD",
                "description": f"Link newNode.next to current HEAD ({items[0] if n else 'NULL'}).",
                "why_it_matters": "The new node points into the existing circular loop.",
                "items": list(items),
                "active_indices": [0],
                "pointers": {"HEAD": 0, "TAIL": n - 1, "NEW": -99},
                "new_node_value": val,
                "status_badge": "Loop Linked"
            },
            {
                "step_number": 3,
                "pseudo_line": 6,
                "title": "Close the Loop (TAIL.next = newNode)",
                "description": "Re-wire TAIL.next from the old head to the new node.",
                "why_it_matters": "Ensures there is NO NULL pointer anywhere in the list. The tail seamlessly loops back to start.",
                "items": [val] + list(items),
                "active_indices": [0],
                "pointers": {"HEAD": 0, "TAIL": len(items)},
                "new_node_value": None,
                "status_badge": "Closed Loop (O(1))"
            }
        ]
        return {
            "title": "Circular List: Insert Operation",
            "complexity_time": "O(1) Constant Time",
            "complexity_space": "O(1) Auxiliary Space",
            "pseudocode": pseudo,
            "steps": steps
        }

    # Default fallback steps
    pseudo = [
        "1. validate structure and input",
        "2. locate target nodes",
        "3. update forward and backward links",
        "4. restore head, tail, and boundary invariants"
    ]
    return {
        "title": f"{structure_type.title()}: {operation.replace('_', ' ').title()}",
        "complexity_time": "O(1) to O(n)",
        "complexity_space": "O(1) Auxiliary Space",
        "pseudocode": pseudo,
        "steps": [
            {
                "step_number": 1,
                "pseudo_line": 0,
                "title": "Initialize Operation",
                "description": f"Preparing {operation} on {structure_type}.",
                "why_it_matters": "Validate inputs and current pointers.",
                "items": list(items),
                "active_indices": [0] if n else [],
                "pointers": {"HEAD": 0 if n else -1, "TAIL": n - 1 if n else -1},
                "new_node_value": None,
                "status_badge": "Ready"
            },
            {
                "step_number": 2,
                "pseudo_line": 2,
                "title": "Execute Pointer Changes",
                "description": "Perform dynamic pointer adjustments.",
                "why_it_matters": "Keep link ordering consistent.",
                "items": list(items),
                "active_indices": [min(1, n - 1)] if n else [],
                "pointers": {"HEAD": 0 if n else -1, "CURR": min(1, n - 1) if n else -1},
                "new_node_value": None,
                "status_badge": "Updated"
            }
        ]
    }
