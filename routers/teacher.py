from fastapi import APIRouter, HTTPException, status

from database.mongodb import mongodb
from models.user_factory import UserFactory

router = APIRouter()

teachers = mongodb.get_collection("teachers")


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
