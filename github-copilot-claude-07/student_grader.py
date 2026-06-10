"""Student grader utility.

Usage:
  - Import functions: `grade_student`, `grade_students`.
  - Run as script for a small demo: `python student_grader.py`.
"""

from typing import Dict, List, Tuple


def calculate_total(marks: Dict[str, float]) -> float:
    """Return the sum of the provided marks."""
    return sum(float(v) for v in marks.values())


def percentage(total: float, max_total: float) -> float:
    """Return percentage given a total and max_total.

    Raises ValueError if `max_total` is not positive.
    """
    if max_total <= 0:
        raise ValueError("max_total must be > 0")
    return (total / max_total) * 100.0


def grade_from_percentage(pct: float) -> Tuple[str, str]:
    """Map percentage to a grade and a short remark."""
    if pct >= 90:
        return "A+", "Excellent"
    if pct >= 80:
        return "A", "Very Good"
    if pct >= 70:
        return "B", "Good"
    if pct >= 60:
        return "C", "Average"
    if pct >= 50:
        return "D", "Below Average"
    return "F", "Fail"


def grade_student(marks: Dict[str, float], max_per_subject: float = 100.0) -> Dict[str, object]:
    """Calculate total, percentage and grade for a single student.

    Args:
        marks: mapping subject -> mark
        max_per_subject: maximum marks for each subject (defaults to 100)

    Returns:
        A dict containing total, max_total, percentage, grade and remark.
    """
    if not marks:
        raise ValueError("marks must be a non-empty dict")

    total = calculate_total(marks)
    max_total = len(marks) * float(max_per_subject)
    pct = percentage(total, max_total)
    grade, remark = grade_from_percentage(pct)
    return {
        "total": round(total, 2),
        "max_total": round(max_total, 2),
        "percentage": round(pct, 2),
        "grade": grade,
        "remark": remark,
    }


def grade_students(students: List[Dict], max_per_subject: float = 100.0) -> List[Dict]:
    """Grade multiple students.

    Each student dict should contain:
      - `name`: student name
      - `marks`: dict of subject -> mark

    Returns a list of dicts with name + grading results.
    """
    results: List[Dict] = []
    for s in students:
        name = s.get("name", "<unknown>")
        marks = s.get("marks")
        try:
            graded = grade_student(marks, max_per_subject)
        except Exception as e:
            graded = {"error": str(e)}
        out = {"name": name}
        out.update(graded)
        results.append(out)
    return results


if __name__ == "__main__":
    # Quick demo
    demo_students = [
        {"name": "Alice", "marks": {"Math": 95, "Physics": 88, "Chemistry": 92}},
        {"name": "Bob", "marks": {"Math": 72, "Physics": 68, "Chemistry": 70}},
        {"name": "Charlie", "marks": {"Math": 45, "Physics": 52, "Chemistry": 48}},
    ]
    results = grade_students(demo_students)
    for r in results:
        print(
            f"{r['name']}: Total {r.get('total')}/{r.get('max_total')} - {r.get('percentage')}% - Grade {r.get('grade')} ({r.get('remark')})"
        )
