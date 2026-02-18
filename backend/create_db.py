from sqlalchemy import create_engine
from models import Base   # import from models.py

engine = create_engine("sqlite:///airline.db")

Base.metadata.create_all(engine)

print("Database created successfully!")
