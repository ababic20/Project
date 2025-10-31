from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
import datetime

# ----- USER -----
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

# ----- TASK -----
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
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    week: Optional[int] = None
    category: Optional[str] = None

class TaskCreate(TaskBase):
    title: str
    week: int

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

# ----- TOKEN -----
class Token(BaseModel):
    access_token: str
    token_type: str
