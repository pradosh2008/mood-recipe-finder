import httpx
from typing import Dict, Optional
import json
import os
import logging
from dotenv import load_dotenv
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found in .env file")

API_URL = "https://api-inference.huggingface.co/models/"
IMAGE_MODEL = "CompVis/stable-diffusion-v1-4"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Mood-based recipe templates
RECIPES = {
    "happy": [
        {
            "name": "Colorful Buddha Bowl",
            "ingredients": "- 1 cup quinoa\n- 1 sweet potato, cubed\n- 1 avocado\n- Mixed fresh vegetables\n- Tahini dressing",
            "instructions": "1. Cook quinoa\n2. Roast sweet potato\n3. Arrange bowl with fresh veggies\n4. Top with avocado and dressing",
            "cooking_time": "25 minutes",
            "difficulty_level": "easy",
            "image_prompt": "colorful buddha bowl with quinoa, roasted vegetables, and avocado, overhead shot, food photography"
        },
        {
            "name": "Rainbow Fruit Smoothie",
            "ingredients": "- Mixed berries\n- Banana\n- Greek yogurt\n- Honey\n- Granola topping",
            "instructions": "1. Blend fruits and yogurt\n2. Pour into glass\n3. Top with granola\n4. Drizzle honey",
            "cooking_time": "10 minutes",
            "difficulty_level": "easy",
            "image_prompt": "vibrant fruit smoothie with berries and granola topping, bright food photography"
        }
    ],
    "sad": [
        {
            "name": "Creamy Mac and Cheese",
            "ingredients": "- 2 cups macaroni\n- 2 cups cheddar cheese\n- 1 cup milk\n- Butter and flour\n- Salt and pepper",
            "instructions": "1. Cook pasta\n2. Make cheese sauce\n3. Combine and bake\n4. Serve hot",
            "cooking_time": "30 minutes",
            "difficulty_level": "easy",
            "image_prompt": "creamy baked mac and cheese, melted cheese, comfort food photography"
        },
        {
            "name": "Chocolate Chip Cookies",
            "ingredients": "- 2 cups flour\n- 1 cup butter\n- Brown sugar\n- Chocolate chips\n- Vanilla extract",
            "instructions": "1. Mix ingredients\n2. Form cookies\n3. Bake until golden\n4. Enjoy warm",
            "cooking_time": "20 minutes",
            "difficulty_level": "easy",
            "image_prompt": "freshly baked chocolate chip cookies, warm and gooey, comfort food photography"
        }
    ],
    "excited": [
        {
            "name": "Party Pizza",
            "ingredients": "- Pizza dough\n- Tomato sauce\n- Mozzarella\n- Favorite toppings\n- Fresh basil",
            "instructions": "1. Roll out dough\n2. Add toppings\n3. Bake until bubbly\n4. Slice and serve",
            "cooking_time": "25 minutes",
            "difficulty_level": "medium",
            "image_prompt": "homemade pizza with melted cheese and fresh toppings, rustic food photography"
        }
    ],
    "energetic": [
        {
            "name": "Power Protein Bowl",
            "ingredients": "- Grilled chicken\n- Quinoa\n- Mixed vegetables\n- Avocado\n- Lemon dressing",
            "instructions": "1. Cook quinoa\n2. Grill chicken\n3. Assemble bowl\n4. Add dressing",
            "cooking_time": "30 minutes",
            "difficulty_level": "medium",
            "image_prompt": "healthy protein bowl with grilled chicken and quinoa, bright food photography"
        }
    ]
}

async def generate_recipe(mood: str, cuisine_type: Optional[str] = None) -> Dict:
    """Get a random recipe for the given mood"""
    mood = mood.lower()
    recipes = RECIPES.get(mood, RECIPES["happy"])
    recipe = random.choice(recipes)
    return recipe

async def generate_recipe_image(recipe_name: str) -> str:
    """Generate an image for the recipe"""
    try:
        # Get the recipe's image prompt
        recipe_prompt = None
        for mood_recipes in RECIPES.values():
            for recipe in mood_recipes:
                if recipe["name"] == recipe_name:
                    recipe_prompt = recipe.get("image_prompt")
                    break
            if recipe_prompt:
                break

        prompt = recipe_prompt or f"professional food photography of {recipe_name}, styled food, natural lighting"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}{IMAGE_MODEL}",
                headers=headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "negative_prompt": "text, watermark, blurry, cartoon",
                        "num_inference_steps": 25,
                        "guidance_scale": 7.5
                    }
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                # Create a unique filename
                image_filename = f"food_{recipe_name.lower().replace(' ', '_')}_{os.urandom(4).hex()}.png"
                
                # Use absolute path
                image_dir = os.path.join(os.path.dirname(__file__), "static", "images")
                image_path = os.path.join(image_dir, image_filename)
                
                # Ensure directory exists
                os.makedirs(image_dir, exist_ok=True)
                
                # Save the image
                with open(image_path, "wb") as f:
                    f.write(response.content)
                
                logger.info(f"Image saved to: {image_path}")
                return f"/static/images/{image_filename}"
            else:
                logger.error(f"Image generation failed: {response.status_code} - {response.text}")
                return get_fallback_image_url(recipe_name)

    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return get_fallback_image_url(recipe_name)

def get_fallback_image_url(recipe_name: str) -> str:
    """Get a fallback image URL based on recipe type"""
    recipe_type_images = {
        "bowl": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38",
        "smoothie": "https://images.unsplash.com/photo-1505252585461-04db1eb84625",
        "pasta": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8",
        "cookie": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e",
        "pizza": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"
    }
    
    # Find matching image based on recipe name
    for key, url in recipe_type_images.items():
        if key.lower() in recipe_name.lower():
            return url
    
    # Default food image
    return "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"