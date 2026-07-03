from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import get_mongodb
from routers.academic import router as academic_router
from routers.notice import router as notice_router
from routers.student import router as student_router
from routers.staff import router as staff_router
from routers.teacher import router as teacher_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router)
app.include_router(staff_router)
app.include_router(teacher_router)
app.include_router(notice_router)
app.include_router(academic_router)


@app.on_event("shutdown")
def shutdown_db_client():
    get_mongodb().close()

@app.get("/")
def role_select_page():
    return FileResponse("templates/role_select.html")


@app.get("/student")
def student_login_page():
    return FileResponse("templates/student_login.html")


@app.get("/teacher")
def teacher_login_page():
    return FileResponse("templates/teacher_login.html")


@app.get("/teacher-dashboard")
def teacher_dashboard_page():
    return FileResponse("templates/teacher_dashboard.html")


@app.get("/staff")
def staff_login_page():
    return FileResponse("templates/staff_login.html")


@app.get("/register")
def register_page():
    return FileResponse("templates/student_createaccount.html")


@app.get("/teacher-register")
def teacher_register_page():
    return FileResponse("templates/teacher_createaccount.html")


@app.get("/staff-register")
def staff_register_page():
    return FileResponse("templates/staff_createaccount.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/student_dashboard.html")
