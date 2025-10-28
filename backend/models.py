import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def _normalize_db_url(url: str) -> str:
    # Render često daje "postgres://", a SQLAlchemy treba "postgresql+psycopg2://"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    return url

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
DB_URL = _normalize_db_url(DB_URL)

# Ako je Postgres na Renderu, osiguraj SSL
if DB_URL.startswith("postgresql"):
    if "sslmode=" not in DB_URL:
        DB_URL += ("&" if "?" in DB_URL else "?") + "sslmode=require"

# connect_args samo za sqlite
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(
    DB_URL,
    future=True,
    echo=False,
    pool_pre_ping=True,   # automatski obnavlja "mrtve" konekcije
    connect_args=connect_args,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
