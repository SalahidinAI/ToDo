from todo_app.db.models import Task
from todo_app.db.schema import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from todo_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

task_router = APIRouter(prefix='/task', tags=['Tasks'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@task_router.post('/', response_model=TaskCreateSchema)
async def task(task: TaskCreateSchema, db: Session = Depends(get_db)):
    task_db = Task(**task.dict())
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


@task_router.get('/', response_model=List[TaskSchema])
async def task_list(user_id: int, db: Session = Depends(get_db),
                    skip: int = 0, limit: int = 10):
    tasks_db = db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()
    return tasks_db


@task_router.get('/{task_id}/', response_model=TaskSchema)
async def task_detail(user_id: int, task_id: int, db: Session = Depends(get_db)):
    task_db = db.query(Task).filter(Task.id == task_id,
                                    Task.user_id == user_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail='Task not found')
    return task_db


@task_router.put('/{task_id}/', response_model=TaskSchema)
async def task_update(task_id: int, task: TaskUpdateSchema, db: Session = Depends(get_db)):
    task_db = db.query(Task).filter(Task.id == task_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail='Task not found')

    task_db.status = task.status

    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


@task_router.delete('/{task_id}/')
async def task_delete(task_id: int, db: Session = Depends(get_db)):
    task_db = db.query(Task).filter(Task.id == task_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail='Task not found')

    db.delete(task_db)
    db.commit()
    return {'message': 'Task is deleted'}
