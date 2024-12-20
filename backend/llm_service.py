"""
Recipe generation service using LLM for recipes and Stable Diffusion for images.
"""

import httpx
from typing import Dict, Optional, List
import logging
import os
from dotenv import load_dotenv
import json
import base64
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# API endpoints
LLM_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

async def generate_recipe(mood: str, cuisine_type: Optional[str] = None) -> Dict:
    """
    Generate a recipe using LLM and create matching image using Stable Diffusion.
    """
    try:
        cuisine_prompt = f" and {cuisine_type} cuisine" if cuisine_type else ""
        
        # Get the appropriate mood guideline
        mood_guidelines = {
            "happy": "Light, colorful, fresh dishes with vibrant ingredients",
            "sad": "Warm, comforting, indulgent dishes that feel like a hug",
            "excited": "Fun, party-friendly, shareable dishes that bring joy",
            "energetic": "Nutritious, protein-rich, energizing meals for vitality"
        }
        mood_guideline = mood_guidelines.get(mood.lower(), "Balanced, flavorful dishes")
        
        prompt = f"""<|system|>
You are a professional chef creating unique recipes based on people's moods.
Always respond with a valid JSON object. Format ingredients and instructions as proper lists.

<|user|>
Create a unique recipe for someone feeling {mood}{cuisine_prompt}.

Mood Guideline: {mood_guideline}

Return ONLY a JSON object in this exact format:
{{
    "name": "Unique and descriptive food recipe name",
    "ingredients": "- ingredient 1 with amount\\n- ingredient 2 with amount",
    "instructions": "1. First step\\n2. Second step",
    "cooking_time": "XX minutes",
    "difficulty_level": "easy/medium/hard",
    "cuisine_type": "specific cuisine type",
    "category": "main/appetizer/dessert/etc"
}}

<|assistant|>"""

        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                LLM_API_URL,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 1000,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "do_sample": True,
                        "return_full_text": False
                    }
                },
                headers=headers
            )
            response.raise_for_status()
            
            recipe_text = response.json()[0]["generated_text"]
            logger.info(f"Raw LLM response: {recipe_text}")
            
            # Clean and parse JSON
            recipe_text = recipe_text.strip()
            if not recipe_text.startswith('{'):
                recipe_text = recipe_text[recipe_text.find('{'):]
            if not recipe_text.endswith('}'):
                recipe_text = recipe_text[:recipe_text.rfind('}')+1]
            
            recipe_data = json.loads(recipe_text)
            
            # Generate matching image
            image_url = await generate_food_image(recipe_data)
            recipe_data["image_url"] = image_url
            recipe_data["moods"] = mood.lower()

            logger.info(f"Generated recipe: {recipe_data['name']} for mood: {mood}")
            return recipe_data

    except Exception as e:
        logger.error(f"Error generating recipe: {str(e)}")
        logger.error(f"Full error details: {e.__class__.__name__}")
        raise

async def generate_food_image(recipe_data: Dict) -> str:
    """
    Generate a food image using Stable Diffusion based on recipe details.
    """
    try:
        # Create a detailed prompt for the image
        ingredients_list = recipe_data['ingredients'].split('\n')[:3]
        ingredients_text = ', '.join([ing.strip('- ').split(',')[0] for ing in ingredients_list])
        
        prompt = f"""Professional food photography of {recipe_data['name']}.
        A beautiful {recipe_data['cuisine_type']} {recipe_data['category']} dish.
        Made with {ingredients_text}.
        Food photography, professional lighting, high-end restaurant presentation,
        centered composition, shallow depth of field, soft natural lighting,
        garnished, styled food photography, 4k, high resolution, hyperrealistic"""

        # Configure image generation
        payload = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1
                },
                {
                    "text": "blurry, text, watermark, logo, pixelated, low quality, cartoon, drawing, anime, illustration, painting, rendered, artificial",
                    "weight": -1
                }
            ],
            "cfg_scale": 8,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 40,
            "style_preset": "photographic"
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                STABILITY_API_URL,
                json=payload,
                headers=headers
            )
            
            if response.status_code != 200:
                logger.error(f"Stability API Error: {response.status_code}")
                logger.error(f"Response content: {response.content}")
                return None
                
            # Get the generated image
            result = response.json()
            logger.info(f"Stability API Response: {result}")
            
            if "artifacts" in result and len(result["artifacts"]) > 0:
                image_data = result["artifacts"][0]["base64"]
                return f"data:image/png;base64,{image_data}"
            else:
                logger.error("No image generated in response")
                logger.error(f"Full response: {result}")
                return None

    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Response content: {e.response.content}")
        return None

async def get_recipe_suggestions(mood: str, count: int = 3) -> List[Dict]:
    """
    Get multiple recipe suggestions for a given mood.
    """
    recipes = []
    for _ in range(count):
        recipe = await generate_recipe(mood)
        recipes.append(recipe)
    return recipes