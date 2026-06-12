from fastapi import APIRouter, HTTPException, status

from database.mongodb import mongodb
from models.user_factory import UserFactory

router = APIRouter()

staffs = mongodb.get_collection("staffs")


@router.post("/staff-register", status_code=status.HTTP_201_CREATED)
async def register_staff(staff: dict):
    try:
        config = UserFactory.get_config("staff")
        required_fields = config["required_fields"]
        missing_fields = [field for field in required_fields if not staff.get(field)]

        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please fill all fields",
            )

        email = staff["email"].strip().lower()
        staff_id = staff["staff_id"].strip()

        if staffs.find_one({"email": email}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        if staffs.find_one({"staff_id": staff_id}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Staff ID already registered",
            )

        staff = UserFactory.create_user("staff", staff)

        result = staffs.insert_one(staff)

        return {
            "message": "Staff Account Created Successfully",
            "inserted_id": str(result.inserted_id),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
