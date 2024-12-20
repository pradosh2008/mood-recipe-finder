from sqlalchemy import Column, Integer, String
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(String)
    instructions = Column(String)
    mood = Column(String, index=True)
    image_url = Column(String) 