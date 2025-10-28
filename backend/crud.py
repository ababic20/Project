from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import json

from backend.models import Task
from backend.schemas import TaskCreate, TaskUpdate


def get_week_range(week_number: int):
    year = datetime.now().year
    first_day = datetime(year, 1, 1)

    # First Monday of the year
    first_monday = first_day - timedelta(days=first_day.weekday())

    start = first_monday + timedelta(weeks=week_number - 1)
    end = start + timedelta(days=6)

    return start.date(), end.date()


def decode_history(task: Task):
    try:
        task.history = json.loads(task.history) if isinstance(task.history, str) else task.history
    except:
        task.history = []
    return task


def get_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        decode_history(task)
    return task


def get_tasks(db: Session, week: Optional[int] = None, category: Optional[str] = None):
    query = db.query(Task)
    if week is not None:
        query = query.filter(Task.week == week)
    if category:
        query = query.filter(Task.category == category)

    tasks = query.all()
    return [decode_history(t) for t in tasks]


def _append_history(task: Task, change: dict):
    try:
        history_list = json.loads(task.history) if isinstance(task.history, str) else task.history
    except:
        history_list = []
    history_list.append(change)
    task.history = json.dumps(history_list)


def create_task(db: Session, payload: TaskCreate):
    week_start, week_end = get_week_range(payload.week)

    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        week=payload.week,
        category=payload.category,
        week_start=week_start,
        week_end=week_end,
        history="[]"
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return decode_history(task)


def update_task(db: Session, task: Task, payload: TaskUpdate):
    change = {"timestamp": datetime.utcnow().isoformat()}
    updated = False

    if payload.title is not None and payload.title != task.title:
        change["old_title"] = task.title
        change["new_title"] = payload.title
        task.title = payload.title
        updated = True

    if payload.description is not None and payload.description != task.description:
        change["old_description"] = task.description
        change["new_description"] = payload.description
        task.description = payload.description
        updated = True

    if payload.status is not None and payload.status != task.status:
        change["old_status"] = task.status
        change["new_status"] = payload.status
        task.status = payload.status
        updated = True

    if payload.week is not None and payload.week != task.week:
        change["old_week"] = task.week
        change["new_week"] = payload.week
        task.week = payload.week
        task.week_start, task.week_end = get_week_range(payload.week)
        updated = True

    if payload.category is not None and payload.category != task.category:
        change["old_category"] = task.category
        change["new_category"] = payload.category
        task.category = payload.category
        updated = True

    if updated:
        _append_history(task, change)

    db.commit()
    db.refresh(task)
    return decode_history(task)


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
