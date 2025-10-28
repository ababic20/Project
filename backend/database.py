from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_PATH = "./data/tasks.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")


connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(DB_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()
