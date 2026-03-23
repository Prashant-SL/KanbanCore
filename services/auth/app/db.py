# After configuration(config.py), connect to DB here.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    
    # important for Neon
    pool_pre_ping=True,

    # max permanent connections
    pool_size=5,

    # extra temporary connections
    max_overflow=2,

    # recycle connections before Neon closes them
    pool_recycle=1800,

    # seconds to wait before failing
    pool_timeout=30
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()