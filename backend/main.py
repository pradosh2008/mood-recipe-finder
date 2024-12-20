from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import random
import models
import database
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample recipes data - you can expand this
SAMPLE_RECIPES = [
    # Happy Mood Recipes
    {"name": "Chocolate Cake", 
     "ingredients": "2 cups flour, 2 cups sugar, 3/4 cup cocoa powder, 2 eggs, 1 cup milk, 1/2 cup vegetable oil, 2 tsp vanilla extract", 
     "instructions": "1. Preheat oven to 350°F\n2. Mix dry ingredients\n3. Add wet ingredients\n4. Bake for 30-35 minutes", 
     "mood": "happy",
     "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&auto=format"},
    
    {"name": "Rainbow Fruit Salad", 
     "ingredients": "strawberries, oranges, pineapple, kiwi, blueberries, grapes, honey, mint leaves", 
     "instructions": "1. Wash and cut all fruits\n2. Mix in a large bowl\n3. Drizzle with honey\n4. Garnish with mint", 
     "mood": "happy",
     "image_url": "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=500&auto=format"},
    
    {"name": "Pizza from Scratch", 
     "ingredients": "pizza dough, tomato sauce, mozzarella, favorite toppings, olive oil, Italian herbs", 
     "instructions": "1. Roll out dough\n2. Spread sauce\n3. Add toppings\n4. Bake at 450°F for 15-20 minutes", 
     "mood": "happy",
     "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format"},

    # Sad Mood Recipes
    {"name": "Homemade Chicken Soup", 
     "ingredients": "chicken, carrots, celery, onion, chicken broth, noodles, garlic, herbs", 
     "instructions": "1. Simmer chicken in broth\n2. Add vegetables\n3. Cook noodles\n4. Season to taste", 
     "mood": "sad",
     "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500&auto=format"},
    
    {"name": "Creamy Mac and Cheese", 
     "ingredients": "macaroni, cheddar cheese, milk, butter, flour, breadcrumbs, salt, pepper", 
     "instructions": "1. Cook pasta\n2. Make cheese sauce\n3. Combine and top with breadcrumbs\n4. Bake until golden", 
     "mood": "sad",
     "image_url": "https://images.unsplash.com/photo-1612152328957-01c943051601?w=500&auto=format"},
    
    {"name": "Hot Chocolate", 
     "ingredients": "milk, dark chocolate, cocoa powder, sugar, vanilla extract, marshmallows", 
     "instructions": "1. Heat milk\n2. Add chocolate and cocoa\n3. Stir until smooth\n4. Top with marshmallows", 
     "mood": "sad",
     "image_url": "https://images.unsplash.com/photo-1517578239113-b03992dcdd25?w=500&auto=format"},

    # Excited Mood Recipes
    {"name": "Spicy Tacos", 
     "ingredients": "tortillas, ground beef, taco seasoning, lettuce, tomatoes, cheese, hot sauce", 
     "instructions": "1. Cook seasoned meat\n2. Warm tortillas\n3. Assemble with toppings\n4. Add hot sauce to taste", 
     "mood": "excited",
     "image_url": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=500&auto=format"},
    
    {"name": "Sushi Rolls", 
     "ingredients": "sushi rice, nori sheets, fish/vegetables, wasabi, soy sauce, pickled ginger", 
     "instructions": "1. Prepare rice\n2. Layer ingredients\n3. Roll tightly\n4. Slice and serve", 
     "mood": "excited",
     "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&auto=format"},
    
    {"name": "Buffalo Wings", 
     "ingredients": "chicken wings, buffalo sauce, butter, celery, carrots, blue cheese dressing", 
     "instructions": "1. Bake wings until crispy\n2. Toss in sauce\n3. Serve with vegetables\n4. Dip and enjoy", 
     "mood": "excited",
     "image_url": "https://images.unsplash.com/photo-1608039858788-667850f129d3?w=500&auto=format"},

    # Energetic Mood Recipes
    {"name": "Green Power Smoothie", 
     "ingredients": "spinach, banana, apple, yogurt, chia seeds, honey, almond milk", 
     "instructions": "1. Add all ingredients to blender\n2. Blend until smooth\n3. Add ice if desired\n4. Serve immediately", 
     "mood": "energetic",
     "image_url": "https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=500&auto=format"},
    
    {"name": "Quinoa Buddha Bowl", 
     "ingredients": "quinoa, chickpeas, kale, sweet potato, avocado, tahini dressing", 
     "instructions": "1. Cook quinoa\n2. Roast vegetables\n3. Arrange in bowl\n4. Top with dressing", 
     "mood": "energetic",
     "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&auto=format"},
    
    {"name": "Protein-Packed Breakfast Burrito", 
     "ingredients": "eggs, black beans, sweet potatoes, spinach, cheese, salsa, whole wheat tortilla", 
     "instructions": "1. Scramble eggs\n2. Warm beans and potatoes\n3. Assemble burrito\n4. Wrap and serve", 
     "mood": "energetic",
     "image_url": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=500&auto=format"}
]

@app.on_event("startup")
async def startup_event():
    db = next(database.get_db())
    # Add sample recipes if database is empty
    if not db.query(models.Recipe).first():
        for recipe in SAMPLE_RECIPES:
            db_recipe = models.Recipe(**recipe)
            db.add(db_recipe)
        db.commit()

@app.get("/recipes/{mood}")
def get_recipe_by_mood(mood: str, db: Session = Depends(database.get_db)):
    recipes = db.query(models.Recipe).filter(models.Recipe.mood == mood.lower()).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found for this mood")
    return random.choice(recipes) 