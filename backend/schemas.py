from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
import datetime

class HistoryEntry(BaseModel):
    timestamp: str
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    old_week: Optional[int] = None
    new_week: Optional[int] = None
    old_category: Optional[str] = None
    new_category: Optional[str] = None
    note: Optional[str] = None

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "new"
    week: Optional[int] = None
    category: str = "business"
    week_start: Optional[datetime.date] = None
    week_end: Optional[datetime.date] = None
    history: List[Dict[str, Any]] = []

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    week: Optional[int] = None
    category: Optional[str] = None

class TaskOut(TaskBase):
    id: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)
