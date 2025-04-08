from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from todo_app.api import profile, task, auth, social_auth

todo = FastAPI(title='To Do')
todo.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

todo.include_router(auth.auth_router)
todo.include_router(profile.user_router)
todo.include_router(task.task_router)
todo.include_router(social_auth.social_router)

if __name__ == '__main__':
    uvicorn.run(todo, host='127.0.0.1', port=8000)
