document.addEventListener('DOMContentLoaded', function() {
    const moodButtons = document.querySelectorAll('.mood-btn');
    const recipeContainer = document.getElementById('recipe-container');
    const loadingContainer = document.getElementById('loading-container');
    const DEFAULT_IMAGE_URL = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c';
    let currentMood = '';

    async function getRecipe(mood, isNewRecipe = false) {
        try {
            // Show loading
            loadingContainer.style.display = 'block';
            recipeContainer.style.display = 'none';

            // Get a fresh recipe from the LLM
            const timestamp = new Date().getTime();
            const response = await fetch(
                `http://localhost:8000/recipes/${mood}?t=${timestamp}`
            );
            
            if (!response.ok) {
                throw new Error('Failed to generate recipe');
            }

            const recipe = await response.json();
            
            // Update UI with the generated recipe
            const recipeImg = document.getElementById('recipe-img');
            // Use default image if no image_url is provided or if it's null
            recipeImg.src = recipe.image_url || DEFAULT_IMAGE_URL;
            recipeImg.onerror = function() {
                this.src = DEFAULT_IMAGE_URL;  // Fallback if image fails to load
            };

            document.getElementById('recipe-name').textContent = recipe.name;
            document.getElementById('cooking-time').textContent = recipe.cooking_time;
            document.getElementById('difficulty-level').textContent = recipe.difficulty_level;

            // Parse and display ingredients
            const ingredientsList = document.getElementById('ingredients-list');
            ingredientsList.innerHTML = '';
            recipe.ingredients.split('\n').forEach(ingredient => {
                if (ingredient.trim()) {
                    const li = document.createElement('li');
                    li.textContent = ingredient.replace('- ', '');
                    ingredientsList.appendChild(li);
                }
            });

            // Parse and display instructions
            const instructionsList = document.getElementById('instructions-list');
            instructionsList.innerHTML = '';
            recipe.instructions.split('\n').forEach(instruction => {
                if (instruction.trim()) {
                    const li = document.createElement('li');
                    li.textContent = instruction.replace(/^\d+\.\s*/, '');
                    instructionsList.appendChild(li);
                }
            });

            // Add "Get Another Recipe" button
            let newRecipeBtn = document.querySelector('.new-recipe-btn');
            if (!newRecipeBtn) {
                newRecipeBtn = document.createElement('button');
                newRecipeBtn.className = 'new-recipe-btn';
                newRecipeBtn.textContent = 'Get Another Recipe';
                recipeContainer.appendChild(newRecipeBtn);
            }
            
            // Update button click handler for new recipe generation
            newRecipeBtn.onclick = () => getRecipe(currentMood, true);

            // Show recipe and hide loading
            loadingContainer.style.display = 'none';
            recipeContainer.style.display = 'block';

            // Scroll to recipe if it's a new recipe request
            if (isNewRecipe) {
                recipeContainer.scrollIntoView({ behavior: 'smooth' });
            }

        } catch (error) {
            console.error('Error:', error);
            loadingContainer.style.display = 'none';
            alert('Failed to generate recipe. Please try again.');
        }
    }

    moodButtons.forEach(button => {
        button.addEventListener('click', function() {
            const mood = this.getAttribute('data-mood');
            
            // Always generate a new recipe when clicking mood buttons
            moodButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            currentMood = mood;
            getRecipe(mood);
        });
    });
}); 