from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print("=" * 50)
            print("PostgreSQL Connection: SUCCESS")
            print(f"Version: {version}")
            print("=" * 50)
            return True
    except Exception as e:
        print("=" * 50)
        print("PostgreSQL Connection: FAILED")
        print(f"Error: {e}")
        print("=" * 50)
        return False


if __name__ == "__main__":
    test_connection()