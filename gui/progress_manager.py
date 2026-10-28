"""
DSA Simulator - Local Offline Progress Manager
Persists student achievements, quiz performance, and challenge milestones to progress.json.
"""

import json
import os
from typing import Dict, Any, List

PROGRESS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "progress.json")


def load_progress() -> Dict[str, Any]:
    default_state = {
        "lessons_completed": [],
        "operations_executed": 0,
        "quiz_best_score": 0,
        "quiz_total_taken": 0,
        "quiz_correct_count": 0,
        "challenges_solved": [],
        "structures_explored": ["singly"]
    }
    if not os.path.exists(PROGRESS_FILE):
        return default_state

    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Merge with defaults
            for k, v in default_state.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return default_state


def save_progress(data: Dict[str, Any]) -> None:
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving progress: {e}")


def record_operation() -> int:
    prog = load_progress()
    prog["operations_executed"] = prog.get("operations_executed", 0) + 1
    save_progress(prog)
    return prog["operations_executed"]


def record_lesson(lesson_id: str) -> bool:
    prog = load_progress()
    lessons = prog.get("lessons_completed", [])
    if lesson_id not in lessons:
        lessons.append(lesson_id)
        prog["lessons_completed"] = lessons
        save_progress(prog)
        return True
    return False


def record_challenge(challenge_id: str) -> bool:
    prog = load_progress()
    chals = prog.get("challenges_solved", [])
    if challenge_id not in chals:
        chals.append(challenge_id)
        prog["challenges_solved"] = chals
        save_progress(prog)
        return True
    return False


def record_quiz_score(score_pct: int) -> None:
    prog = load_progress()
    prog["quiz_best_score"] = max(prog.get("quiz_best_score", 0), score_pct)
    prog["quiz_total_taken"] = prog.get("quiz_total_taken", 0) + 1
    save_progress(prog)


def reset_all_progress() -> None:
    save_progress({
        "lessons_completed": [],
        "operations_executed": 0,
        "quiz_best_score": 0,
        "quiz_total_taken": 0,
        "quiz_correct_count": 0,
        "challenges_solved": [],
        "structures_explored": ["singly"]
    })
