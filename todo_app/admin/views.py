from sqladmin import ModelView
from todo_app.db.models import UserProfile, Task


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.last_name, UserProfile.username]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.title, Task.description, Task.status]
