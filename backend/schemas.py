from pydantic import BaseModel, ConfigDict, Field
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
    title: Optional[str]
    description: Optional[str] = None
    status: Optional[str] = None
    week: Optional[int] = None
    category: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "new"
    week: int
    category: str = "business"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    week: Optional[int] = None
    category: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    week: Optional[int]
    category: str
    week_start: Optional[datetime.date]
    week_end: Optional[datetime.date]
    history: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    model_config = ConfigDict(from_attributes=True)
