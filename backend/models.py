from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(Text)
    instructions = Column(Text)
    mood = Column(String, index=True)
    image_url = Column(String)
    cuisine_type = Column(String, index=True)
    cooking_time = Column(String)
    difficulty_level = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 