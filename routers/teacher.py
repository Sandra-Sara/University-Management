from fastapi import APIRouter, HTTPException, status

from database.mongodb import get_collection
from models.user_factory import UserFactory

router = APIRouter()

teachers = get_collection("teachers")


@router.post("/teacher-register", status_code=status.HTTP_201_CREATED)
async def register_teacher(teacher: dict):
    try:
        config = UserFactory.get_config("teacher")
        required_fields = config["required_fields"]
        missing_fields = [field for field in required_fields if not teacher.get(field)]

        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please fill all fields",
            )

        email = teacher["email"].strip().lower()
        teacher_id = teacher["teacher_id"].strip()

        if teachers.find_one({"email": email}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        if teachers.find_one({"teacher_id": teacher_id}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher ID already registered",
            )

        teacher = UserFactory.create_user("teacher", teacher)

        result = teachers.insert_one(teacher)

        return {
            "message": "Teacher Account Created Successfully",
            "inserted_id": str(result.inserted_id),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/teacher-login")
async def login_teacher(credentials: dict):
    teacher_id = credentials.get("teacher_id", "").strip()
    password = credentials.get("password", "")

    if not teacher_id or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please fill all fields",
        )

    teacher = teachers.find_one({"teacher_id": teacher_id})

    if not teacher or not UserFactory.verify_password(password, teacher.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Teacher ID or Password",
        )

    return {
        "message": "Login Successful",
        "teacher": {
            "id": str(teacher["_id"]),
            "teacher_id": teacher.get("teacher_id"),
            "name": teacher.get("name"),
            "email": teacher.get("email"),
            "department": teacher.get("department"),
        },
    }
