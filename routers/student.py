from fastapi import APIRouter, HTTPException, status

from database.mongodb import get_collection
from models.user_factory import UserFactory

router = APIRouter()

students = get_collection("students")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_student(student: dict):
    try:
        config = UserFactory.get_config("student")
        required_fields = config["required_fields"]
        missing_fields = [field for field in required_fields if not student.get(field)]

        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please fill all fields",
            )

        email = student["email"].strip().lower()
        student_id = student["student_id"].strip()

        if students.find_one({"email": email}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        if students.find_one({"student_id": student_id}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Student ID already registered",
            )

        student = UserFactory.create_user("student", student)

        result = students.insert_one(student)

        return {
            "message": "Account Created Successfully",
            "inserted_id": str(result.inserted_id)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/login")
async def login_student(credentials: dict):
    email = credentials.get("email", "").strip().lower()
    password = credentials.get("password", "")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please fill all fields",
        )

    student = students.find_one({"email": email})

    if not student or not UserFactory.verify_password(password, student.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password",
        )

    return {
        "message": "Login Successful",
        "student": {
            "id": str(student["_id"]),
            "student_id": student.get("student_id"),
            "name": student.get("name"),
            "email": student.get("email"),
            "department": student.get("department"),
        },
    }
