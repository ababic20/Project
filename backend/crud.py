from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import json
from passlib.context import CryptContext
from models import Task, User
from schemas import TaskCreate, TaskUpdate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- USER CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = User(username=user.username, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# --- TASKS CRUD ---
def get_week_range(week_number: int):
    year = datetime.now().year
    first_day = datetime(year, 1, 1)
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


def get_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if task:
        decode_history(task)
    return task


def get_tasks(db: Session, user_id: int, week: Optional[int] = None, category: Optional[str] = None):
    query = db.query(Task).filter(Task.owner_id == user_id)
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


def create_task(db: Session, payload: TaskCreate, user_id: int):
    week_start, week_end = get_week_range(payload.week)
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status or "new",
        week=payload.week,
        category=payload.category or "business",
        week_start=week_start,
        week_end=week_end,
        history="[]",
        owner_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return decode_history(task)


def update_task(db: Session, task: Task, payload: TaskUpdate):
    change = {"timestamp": datetime.utcnow().isoformat()}
    updated = False

    for field, value in payload.dict(exclude_unset=True).items():
        old = getattr(task, field)
        if value != old:
            change[f"old_{field}"] = old
            change[f"new_{field}"] = value
            setattr(task, field, value)
            updated = True

    if updated:
        _append_history(task, change)

    db.commit()
    db.refresh(task)
    return decode_history(task)


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
