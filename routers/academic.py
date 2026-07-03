from fastapi import APIRouter, HTTPException, status

from database.mongodb import get_collection

router = APIRouter()

courses = get_collection("courses")
grades = get_collection("grades")
attendance = get_collection("attendance")


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(course: dict):
    required_fields = ["student_id", "course_code", "course_name"]
    missing_fields = [field for field in required_fields if not course.get(field)]

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide student ID, course code, and course name",
        )

    course_doc = {
        "student_id": course["student_id"].strip(),
        "course_code": course["course_code"].strip(),
        "course_name": course["course_name"].strip(),
        "teacher": course.get("teacher", "").strip(),
        "semester": course.get("semester", "").strip(),
    }

    result = courses.insert_one(course_doc)

    return {
        "message": "Course Added Successfully",
        "inserted_id": str(result.inserted_id),
    }


@router.post("/grades", status_code=status.HTTP_201_CREATED)
async def create_grade(grade: dict):
    required_fields = ["student_id", "course_code", "marks", "grade"]
    missing_fields = [field for field in required_fields if not grade.get(field)]

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide student ID, course code, marks, and grade",
        )

    grade_doc = {
        "student_id": grade["student_id"].strip(),
        "course_code": grade["course_code"].strip(),
        "marks": grade["marks"],
        "grade": grade["grade"].strip(),
        "semester": grade.get("semester", "").strip(),
    }

    result = grades.insert_one(grade_doc)

    return {
        "message": "Grade Added Successfully",
        "inserted_id": str(result.inserted_id),
    }


@router.post("/attendance", status_code=status.HTTP_201_CREATED)
async def create_attendance(attendance_record: dict):
    required_fields = ["student_id", "course_code", "date", "status"]
    missing_fields = [field for field in required_fields if not attendance_record.get(field)]

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide student ID, course code, date, and status",
        )

    attendance_doc = {
        "student_id": attendance_record["student_id"].strip(),
        "course_code": attendance_record["course_code"].strip(),
        "date": attendance_record["date"].strip(),
        "status": attendance_record["status"].strip(),
    }

    result = attendance.insert_one(attendance_doc)

    return {
        "message": "Attendance Added Successfully",
        "inserted_id": str(result.inserted_id),
    }


@router.get("/student-courses/{student_id}")
async def get_student_courses(student_id: str):
    student_courses = list(
        courses.find(
            {"student_id": student_id},
            {"_id": 0},
        )
    )

    return {
        "student_id": student_id,
        "courses": student_courses,
    }


@router.get("/student-grades/{student_id}")
async def get_student_grades(student_id: str):
    student_grades = list(
        grades.find(
            {"student_id": student_id},
            {"_id": 0},
        )
    )

    return {
        "student_id": student_id,
        "grades": student_grades,
    }


@router.get("/student-attendance/{student_id}")
async def get_student_attendance(student_id: str):
    student_attendance = list(
        attendance.find(
            {"student_id": student_id},
            {"_id": 0},
        )
    )

    return {
        "student_id": student_id,
        "attendance": student_attendance,
    }
