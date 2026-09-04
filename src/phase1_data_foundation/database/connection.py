import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base

load_dotenv()

# Using SQLite by default for easy local testing
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///phase1_data.db")

# connect_args is needed for SQLite to handle multi-threading appropriately in some setups
connect_args = {"check_same_thread": False} if DATABASE_URI.startswith("sqlite") else {}

engine = create_engine(DATABASE_URI, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
