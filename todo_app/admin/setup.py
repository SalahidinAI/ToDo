from sqladmin import Admin
from fastapi import FastAPI
from .views import UserProfileAdmin, TaskAdmin
from todo_app.db.database import engine

def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(TaskAdmin)

