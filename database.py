from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_uri="postgresql://postgres:06122004@localhost:5432/products"
engine=create_engine(db_uri)
session=sessionmaker(autoflush=False,bind=engine)