let currentMood = '';

async function getRecipe(mood) {
    currentMood = mood;
    try {
        // Show loading state
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('recipe-container').classList.add('hidden');

        const response = await fetch(`http://localhost:8000/recipes/${mood}`);
        if (!response.ok) {
            throw new Error('No recipe found');
        }
        const recipe = await response.json();
        displayRecipe(recipe);
    } catch (error) {
        console.error('Error:', error);
        alert('No recipe found for this mood. Try another mood!');
    } finally {
        // Hide loading state
        document.getElementById('loading').classList.add('hidden');
    }
}

function displayRecipe(recipe) {
    document.getElementById('recipe-container').classList.remove('hidden');
    document.getElementById('recipe-name').textContent = recipe.name;
    document.getElementById('ingredients').textContent = recipe.ingredients;
    document.getElementById('instructions').textContent = recipe.instructions;
    
    // Add new fields if they exist
    const additionalInfo = [];
    if (recipe.cooking_time) additionalInfo.push(`Cooking Time: ${recipe.cooking_time}`);
    if (recipe.difficulty_level) additionalInfo.push(`Difficulty: ${recipe.difficulty_level}`);
    if (recipe.cuisine_type) additionalInfo.push(`Cuisine: ${recipe.cuisine_type}`);
    
    // Display additional info if it exists
    const additionalInfoElement = document.getElementById('additional-info');
    if (additionalInfoElement) {
        additionalInfoElement.textContent = additionalInfo.join(' | ');
    }
    
    // Add image display with better error handling
    const imageContainer = document.getElementById('recipe-image');
    if (imageContainer) {
        const img = new Image();
        img.onload = function() {
            imageContainer.innerHTML = '';
            imageContainer.appendChild(img);
        };
        img.onerror = function() {
            console.error('Failed to load image:', img.src);
            // Use a default food image if loading fails
            img.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c';
        };
        img.src = recipe.image_url.startsWith('http') ? 
            recipe.image_url : 
            `http://localhost:8000${recipe.image_url}`;
        img.alt = recipe.name;
        img.style.width = '100%';
        img.style.borderRadius = '8px';
    }
}

function getNewRecipe() {
    getRecipe(currentMood);
} 