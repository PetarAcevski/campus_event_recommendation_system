from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Student
from backend.schemas.student import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    statement = (
        select(Student)
        .where(Student.deleted_at.is_(None))
        .order_by(Student.id)
    )
    return db.scalars(statement).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)

    if not student or student.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Student not found.")

    return student


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.scalar(
        select(Student).where(Student.email == student_data.email)
    )

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists.",
        )

    student = Student(**student_data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)

    return student