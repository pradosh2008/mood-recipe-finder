# Mood Recipe Finder

A web application that suggests recipes based on your current mood. Whether you're happy, sad, excited, or energetic, this app will recommend the perfect recipe to match your emotional state.

## Features

- Mood-based recipe recommendations
- Interactive UI with emoji mood selectors
- Recipe display with images, ingredients, and instructions
- Option to get alternative recipes for the same mood
- Responsive design that works on both desktop and mobile devices

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite (Database)

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

## Installation

### Backend Setup

1. Clone the repository:

2. Create and activate a virtual environment:

3. Install dependencies:

4. Start the backend server:

The backend will be running at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:


2. Open `index.html` in your web browser or serve it using a local server:

The frontend will be accessible at `http://localhost:8080`

## Usage

1. Ensure both backend and frontend servers are running
2. Open your web browser and navigate to `http://localhost:8080`
3. Click on an emoji that matches your current mood
4. View the recommended recipe with ingredients and instructions
5. Click "Get Another Recipe" for more suggestions matching your mood

## API Endpoints

- `GET /recipes/{mood}`: Get a random recipe for the specified mood
  - Available moods: happy, sad, excited, energetic
  - Returns: Recipe object with name, ingredients, instructions, and image URL

## Project Structure

mood-recipe-finder/
├── backend/
│ ├── main.py # FastAPI application and routes
│ ├── models.py # SQLAlchemy models
│ └── database.py # Database configuration
├── frontend/
│ ├── index.html # Main HTML file
│ ├── styles.css # Styling
│ └── script.js # Frontend JavaScript
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── LICENSE # MIT license


## Development

To add new recipes or modify existing ones, edit the `SAMPLE_RECIPES` list in `backend/main.py`. Each recipe should include:
- name
- ingredients
- instructions
- mood
- image_url

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Pradosh Kumar Jena

## Acknowledgments

- Recipe images from Unsplash
- Emoji support for mood selection
- FastAPI for the efficient backend
- SQLAlchemy for database management


How can you push the project to github

1. First, you need to create a new repository on GitHub:
Go to GitHub
Click the "+" icon in the top right corner
Select "New repository"
Name it "mood-recipe-finder"
Don't initialize it with any files (no README, no .gitignore)
Click "Create repository"

Then, if this is a new local repository, run these commands in your project directory:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/pradosh2008/mood-recipe-finder.git
git push -u origin main

Make sure that:
1. You're logged into GitHub in your terminal/Git client
The repository name matches exactly (case-sensitive)
Your GitHub username is correct in the URL
You have the necessary permissions for the repository
If you're using HTTPS, you might need to enter your GitHub credentials when pushing. If you're using SSH, ensure your SSH keys are properly set up with GitHub.

To check remote
git remote -v
origin  https://github.com/pradosh2008/mood-recipe-finder.git (fetch)
origin  https://github.com/pradosh2008/mood-recipe-finder.git (push)
1. (fetch): The URL used when pulling/fetching data FROM GitHub
(push): The URL used when pushing data TO GitHub

(fetch) is your "download" URL
(push) is your "upload" URL

## Environment Setup

1. Get a free API key from Hugging Face:
   - Go to https://huggingface.co/
   - Create an account
   - Go to Settings -> Access Tokens
   - Create a new token with read access

2. Create a `.env` file in the project root:   ```
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here   ```

## New Features in v2
- Dynamic recipe generation using AI
- AI-generated food images
- Extended recipe details (cooking time, difficulty level, cuisine type)
- Persistent storage of generated recipes
- More detailed recipe information

[Rest of the README remains the same...]