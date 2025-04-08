from todo_app.db.models import Task
from todo_app.db.schema import TaskSchema
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


@task_router.post('/', response_model=TaskSchema)
async def task(task: TaskSchema, db: Session = Depends(get_db)):
    task_db = Task(**task.dict())
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


@task_router.get('/', response_model=List[TaskSchema])
async def task_list(user_id: int, db: Session = Depends(get_db)):
    tasks_db = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks_db


@task_router.get('/{task_id}/', response_model=TaskSchema)
async def task_detail(user_id: int, task_id: int, db: Session = Depends(get_db)):
    task_db = db.query(Task).filter(Task.id == task_id,
                                    Task.user_id == user_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail='Task not found')
    return task_db


@task_router.put('/{task_id}/', response_model=TaskSchema)
async def task_update(task_id: int, task: TaskSchema, db: Session = Depends(get_db)):
    task_db = db.query(Task).filter(Task.id == task_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail='Task not found')

    for task_key, task_value in task.dict().items():
        setattr(task_db, task_key, task_value)

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
