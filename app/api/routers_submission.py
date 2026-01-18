from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.submission import Submission
from app.models.assignment import Assignment
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

@router.get(
    "/{submission_id}",
    status_code=status.HTTP_200_OK
)
async def get_submission_detail(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1 Fetch submission
    stmt = select(Submission).where(Submission.id == submission_id)
    result = await db.execute(stmt)
    submission = result.scalar_one_or_none()

    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )

    # 2 STUDENT ACCESS RULE
    if current_user.role == "student":
        if submission.student_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view this submission"
            )

    # 3 TEACHER ACCESS RULE
    elif current_user.role == "teacher":
        assignment_stmt = select(Assignment).where(
            Assignment.id == submission.assignment_id,
            Assignment.teacher_id == current_user.id
        )
        assignment_result = await db.execute(assignment_stmt)
        assignment = assignment_result.scalar_one_or_none()

        if not assignment:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view this submission"
            )

    else:
        raise HTTPException(
            status_code=403,
            detail="Invalid role"
        )

    # 4 Response shaping (important)
    response = {
        "submission_id": submission.id,
        "assignment_id": submission.assignment_id,
        "student_id": submission.student_id,
        "aim_ans": submission.aim_ans,
        "objectives_ans": submission.objectives_ans,
        "code_ans": submission.code_ans,
        "conclusion_ans": submission.conclusion_ans,
        "status": submission.status,
        "submitted_at": submission.submitted_at,
    }

    # Show marks ONLY if evaluated
    if submission.status == "EVALUATED":
        response["marks_obtained"] = submission.marks_obtained
        response["feedback"] = submission.feedback
    else:
        response["marks_obtained"] = None
        response["feedback"] = None

    return response
