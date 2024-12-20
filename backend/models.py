from sqlalchemy import Column, Integer, String, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(Text)
    instructions = Column(Text)
    cooking_time = Column(String)
    difficulty_level = Column(String)
    cuisine_type = Column(String, index=True)
    image_url = Column(String)
    image_data = Column(LargeBinary, nullable=True)
    image_content_type = Column(String, nullable=True)
    moods = Column(String, index=True)  # Comma-separated moods
    category = Column(String, index=True)

class RecipeImage(Base):
    __tablename__ = "recipe_images"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    image_data = Column(LargeBinary)
    content_type = Column(String)
    alt_text = Column(String)
    recipe = relationship("Recipe", backref="images")