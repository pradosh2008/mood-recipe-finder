# Mood-Based Recipe Generator

An AI-powered application that generates personalized recipes based on your mood. The application uses state-of-the-art language models to create unique recipes and generates matching food images using AI.

## Features

- 🎯 Mood-based recipe generation
- 🖼️ AI-generated food images
- 🌎 Cuisine type specification
- 📝 Detailed ingredients and instructions
- 🕒 Cooking time and difficulty estimates
- 💡 Multiple recipe suggestions

## Technology Stack

- **Backend:**
  - FastAPI (Python web framework)
  - Hugging Face's Zephyr-7b-beta for recipe generation
  - Stability AI for food image generation
  
- **Frontend:**
  - HTML/CSS/JavaScript
  - Responsive design
  - Real-time API integration

## Prerequisites

- Python 3.8 or higher
- API keys for:
  - Hugging Face (for recipe generation)
  - Stability AI (for image generation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mood-recipe-finder.git
   cd mood-recipe-finder
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```env
   HUGGINGFACE_API_KEY=your_huggingface_key
   STABILITY_API_KEY=your_stability_key
   ```

## Running the Application

1. Start the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. Open `frontend/index.html` in your web browser

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /recipes/{mood}
Generate a recipe based on mood.
- Parameters:
  - `mood` (path): User's mood (e.g., happy, sad, excited)
  - `cuisine_type` (query, optional): Preferred cuisine type

### GET /recipes/{mood}/suggestions
Get multiple recipe suggestions.
- Parameters:
  - `mood` (path): User's mood
  - `count` (query, optional): Number of recipes to generate (default: 3)

## Project Structure
```
mood-recipe-finder/
├── backend/
│   ├── main.py           # FastAPI application and endpoints
│   └── llm_service.py    # LLM and image generation logic
├── frontend/
│   ├── index.html        # Main application page
│   ├── styles.css        # Application styling
│   └── script.js         # Frontend logic
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── .gitignore
└── README.md
```

## Environment Variables

- `HUGGINGFACE_API_KEY`: Your Hugging Face API key for accessing the LLM
- `STABILITY_API_KEY`: Your Stability AI API key for image generation

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for providing the LLM API
- Stability AI for the image generation API
- FastAPI team for the excellent web framework