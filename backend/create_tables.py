"""
Run this once to create all tables in PostgreSQL.
Safe to run multiple times — will not drop existing data.
"""
from backend.database import engine, Base
from backend.models.models import User, Session, Event, Feedback, Subscription

def create_all_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    create_all_tables()