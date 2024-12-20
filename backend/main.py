"""
FastAPI backend for the Mood-Based Recipe Generator.
This service provides endpoints to generate recipes based on user's mood using LLMs
and creates matching food images using Stability AI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging
from llm_service import generate_recipe, get_recipe_suggestions

# Configure logging to track API requests and errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mood Recipe Generator",
    description="An API that generates recipes based on your mood using AI",
    version="1.0.0"
)

# Enable CORS to allow frontend application access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    """Health check endpoint to verify API status"""
    return {"message": "API is running. Please access the frontend application."}

@app.get("/recipes/{mood}")
async def get_recipe_by_mood(
    mood: str, 
    cuisine_type: Optional[str] = None
):
    """
    Generate a recipe based on the user's mood.
    
    Args:
        mood (str): The user's current mood (e.g., happy, sad, excited)
        cuisine_type (Optional[str]): Specific cuisine preference (e.g., Italian, Japanese)
    
    Returns:
        dict: Recipe data including name, ingredients, instructions, and AI-generated image
    
    Raises:
        HTTPException: If recipe generation fails or encounters an error
    """
    try:
        logger.info(f"Generating recipe for mood: {mood}")
        
        # Generate recipe using LLM in real-time
        recipe = await generate_recipe(mood, cuisine_type)
        
        if not recipe:
            raise HTTPException(
                status_code=404, 
                detail="Failed to generate recipe"
            )
        
        return recipe
        
    except Exception as e:
        logger.error(f"Error generating recipe: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/recipes/{mood}/suggestions")
async def get_suggestions(
    mood: str,
    count: int = 3
):
    """
    Get multiple recipe suggestions for a given mood.
    
    Args:
        mood (str): The user's current mood
        count (int): Number of recipes to generate (default: 3)
    
    Returns:
        list: List of recipe dictionaries
    
    Raises:
        HTTPException: If suggestion generation fails
    """
    try:
        logger.info(f"Generating {count} recipe suggestions for mood: {mood}")
        recipes = await get_recipe_suggestions(mood, count)
        return recipes
    except Exception as e:
        logger.error(f"Error generating suggestions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )