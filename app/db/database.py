from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import Config

if not Config.DATABASE_URL:
    raise ValueError("No DATABASE_URL provided. Set DATABASE_URL environment variable.")

engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()