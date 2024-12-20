from database import engine
import models

def init_db():
    """Initialize the database with the latest schema"""
    # Drop all tables
    models.Base.metadata.drop_all(bind=engine)
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 