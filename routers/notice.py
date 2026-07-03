from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from database.mongodb import get_collection
from models.notice_observer import ClassroomNoticeBoard, StudentNotificationObserver

router = APIRouter()

notices = get_collection("notices")
notifications = get_collection("notifications")

notice_board = ClassroomNoticeBoard()
notice_board.attach(StudentNotificationObserver())


@router.post("/notices", status_code=status.HTTP_201_CREATED)
async def create_notice(notice: dict):
    required_fields = ["title", "message", "department"]
    missing_fields = [field for field in required_fields if not notice.get(field)]

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide title, message, and department",
        )

    notice_doc = {
        "title": notice["title"].strip(),
        "message": notice["message"].strip(),
        "department": notice["department"].strip(),
        "created_by": notice.get("created_by", "").strip(),
        "created_at": datetime.now(timezone.utc),
    }

    result = notices.insert_one(notice_doc)
    notice_doc["notice_id"] = str(result.inserted_id)

    notification_ids = notice_board.notify(notice_doc)

    return {
        "message": "Notice Published Successfully",
        "notice_id": str(result.inserted_id),
        "notified_students": len(notification_ids),
        "notification_ids": notification_ids,
    }


@router.get("/student-notifications/{student_id}")
async def get_student_notifications(student_id: str):
    student_notifications = list(
        notifications.find(
            {"student_id": student_id},
            {"_id": 0},
        ).sort("created_at", -1)
    )

    return {
        "student_id": student_id,
        "notifications": student_notifications,
    }
