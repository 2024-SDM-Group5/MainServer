from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import Config

if not Config.DATABASE_URL:
    raise ValueError("No DATABASE_URL provided. Set DATABASE_URL environment variable.")

engine = create_engine(Config.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
