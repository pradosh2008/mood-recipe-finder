from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import database
from database import engine
from llm_service import generate_recipe, generate_recipe_image  # Import the singleton instance
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(os.path.join(STATIC_DIR, "images"), exist_ok=True)

# Initialize database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files directory with proper configuration
app.mount("/static", StaticFiles(directory=STATIC_DIR, check_dir=True), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    """Root endpoint that redirects to frontend"""
    return {"message": "API is running. Please access the frontend application."}

@app.get("/recipes/{mood}")
async def get_recipe_by_mood(
    mood: str, 
    cuisine_type: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    try:
        logger.info(f"Generating recipe for mood: {mood}, cuisine: {cuisine_type}")
        
        # Generate recipe using LLM
        recipe_data = await generate_recipe(mood, cuisine_type)
        
        # Generate image for the recipe
        image_url = await generate_recipe_image(recipe_data["name"])
        
        # Create new recipe object
        db_recipe = models.Recipe(
            name=recipe_data["name"],
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            mood=mood.lower(),
            image_url=image_url,
            cuisine_type=cuisine_type if cuisine_type else "",
            cooking_time=recipe_data.get("cooking_time", "30 minutes"),
            difficulty_level=recipe_data.get("difficulty_level", "medium")
        )
        
        try:
            db.add(db_recipe)
            db.commit()
            db.refresh(db_recipe)
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
        
        return db_recipe
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        ) 

@app.get("/test-image")
async def test_image():
    """Test endpoint to verify static file serving"""
    return FileResponse(os.path.join(STATIC_DIR, "images", "default_food.png"))