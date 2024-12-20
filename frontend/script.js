let currentMood = '';

async function getRecipe(mood) {
    currentMood = mood;
    try {
        const response = await fetch(`http://localhost:8000/recipes/${mood}`);
        if (!response.ok) {
            throw new Error('No recipe found');
        }
        const recipe = await response.json();
        displayRecipe(recipe);
    } catch (error) {
        alert('No recipe found for this mood. Try another mood!');
    }
}

function displayRecipe(recipe) {
    document.getElementById('recipe-container').classList.remove('hidden');
    document.getElementById('recipe-name').textContent = recipe.name;
    document.getElementById('ingredients').textContent = recipe.ingredients;
    document.getElementById('instructions').textContent = recipe.instructions;
    
    // Add image display
    const imageContainer = document.getElementById('recipe-image');
    if (imageContainer) {
        imageContainer.innerHTML = `<img src="${recipe.image_url}" alt="${recipe.name}" style="width: 100%; border-radius: 8px;">`;
    }
}

function getNewRecipe() {
    getRecipe(currentMood);
} 