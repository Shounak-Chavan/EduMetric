from app.core.constants import SECTION_MARKS


def grade_submission(submission) -> dict:
    """
    Rule-based grading (sync, deterministic)

    Returns:
        {
            "marks_obtained": float,
            "feedback": str
        }
    """
    total_marks: float = 0.0
    feedback_lines: list[str] = []

    for section, max_marks in SECTION_MARKS.items():
        field_name = f"{section}_ans"
        student_answer = getattr(submission, field_name, None)

        if student_answer and student_answer.strip():
            total_marks += max_marks
            feedback_lines.append(
                f"{section.capitalize()}: Present (+{max_marks})"
            )
        else:
            feedback_lines.append(
                f"{section.capitalize()}: Missing (+0)"
            )

    return {
        "marks_obtained": total_marks,
        "feedback": "\n".join(feedback_lines)
    }
