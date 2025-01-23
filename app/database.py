from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL="sqlite:///notifications.db"

# Create the engine using the database URL (SQLite)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
