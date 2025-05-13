from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your MySQL credentials
DATABASE_URL = "mysql+mysqlconnector://root:Sql%4021@localhost:3306/chatbot"


# Create database engine & session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
