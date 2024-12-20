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