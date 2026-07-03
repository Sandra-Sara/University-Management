from datetime import datetime, timezone
import re

from database.mongodb import get_collection


class NoticeObserver:
    def update(self, notice: dict):
        raise NotImplementedError


class StudentNotificationObserver(NoticeObserver):
    def __init__(self):
        self.students = get_collection("students")
        self.notifications = get_collection("notifications")

    def update(self, notice: dict):
        department = notice.get("department")

        if not department:
            return []

        enrolled_students = list(
            self.students.find(
                {"department": {"$regex": f"^{re.escape(department)}$", "$options": "i"}},
                {"student_id": 1, "name": 1, "email": 1, "department": 1},
            )
        )

        if not enrolled_students:
            return []

        notification_docs = [
            {
                "student_id": student.get("student_id"),
                "student_name": student.get("name"),
                "student_email": student.get("email"),
                "department": student.get("department"),
                "notice_id": notice.get("notice_id"),
                "title": notice.get("title"),
                "message": notice.get("message"),
                "is_read": False,
                "created_at": datetime.now(timezone.utc),
            }
            for student in enrolled_students
        ]

        result = self.notifications.insert_many(notification_docs)
        return [str(inserted_id) for inserted_id in result.inserted_ids]


class ClassroomNoticeBoard:
    def __init__(self):
        self._observers = []

    def attach(self, observer: NoticeObserver):
        self._observers.append(observer)

    def detach(self, observer: NoticeObserver):
        self._observers.remove(observer)

    def notify(self, notice: dict):
        notification_ids = []

        for observer in self._observers:
            notification_ids.extend(observer.update(notice))

        return notification_ids
