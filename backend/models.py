from sqlalchemy import Column, Integer, String, DateTime, Date, func
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="new")
    week = Column(Integer, nullable=True)
    category = Column(String, nullable=False)

    week_start = Column(Date, nullable=True)
    week_end = Column(Date, nullable=True)

    history = Column(String, nullable=False, default="[]")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
