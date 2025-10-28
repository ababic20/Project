from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine, Base
from models import Task
from schemas import TaskOut, TaskCreate, TaskUpdate
import crud

# Kreiraj tablice ako ne postoje
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager (Kanban + Week View)", version="1.0.0")

# CORS: dopusti lokalni frontend (prilagodi po potrebi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://127.0.0.1:5173",
        "https://project-kj3g.onrender.com",  
        "https://frontend-myxf.onrender.com",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency za DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- ROUTES -----------------

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskOut], tags=["tasks"])
def list_tasks(
    week: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_tasks(db, week=week, category=category)


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, payload)

@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return crud.update_task(db, task, payload)

@app.post("/tasks/{task_id}/move", response_model=TaskOut, tags=["tasks"])
def move_task(task_id: int, new_week: Optional[int] = None, new_status: Optional[str] = None, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return crud.move_task(db, task, new_week=new_week, new_status=new_status)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    crud.delete_task(db, task)
    return None
