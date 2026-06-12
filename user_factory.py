import bcrypt


class UserFactory:
    user_configs = {
        "student": {
            "id_field": "student_id",
            "required_fields": ["student_id", "name", "email", "department", "password"],
        },
        "teacher": {
            "id_field": "teacher_id",
            "required_fields": ["teacher_id", "name", "email", "department", "password"],
        },
        "staff": {
            "id_field": "staff_id",
            "required_fields": ["staff_id", "name", "email", "position", "password"],
        },
    }

    @classmethod
    def create_user(cls, user_type: str, user_data: dict) -> dict:
        config = cls.get_config(user_type)
        user = user_data.copy()

        user["email"] = user["email"].strip().lower()
        user[config["id_field"]] = user[config["id_field"]].strip()
        user["password"] = cls.hash_password(user["password"])
        user["role"] = user_type

        return user

    @classmethod
    def get_config(cls, user_type: str) -> dict:
        if user_type not in cls.user_configs:
            raise ValueError("Invalid user type")

        return cls.user_configs[user_type]

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password: str, saved_password: str) -> bool:
        if saved_password.startswith("$2"):
            return bcrypt.checkpw(password.encode("utf-8"), saved_password.encode("utf-8"))

        # Supports accounts created before password hashing was added.
        return password == saved_password
