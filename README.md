# AI Personalized Learning Platform

An AI-powered learning platform that provides personalized learning experiences through dynamic content generation, interactive quizzes, and adaptive learning paths.

## Features

- **Personalized Learning Roadmaps**: Generate customized learning paths based on your interests and knowledge level
- **AI-Generated Learning Resources**: Get tailored learning materials for your specific needs
- **Interactive Quizzes**: Test your knowledge with AI-generated quizzes
- **Progress Tracking**: Monitor your learning progress and achievements

## Tech Stack

- Frontend: Streamlit
- Backend: Flask
- AI: Google Gemini AI
- Database: JSON (for storing quiz data)

## Prerequisites

- Python 3.8+
- Google Gemini API Key
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aakarsh204/HackNite-25.git
cd HackNite-25/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Flask backend:
```bash
python base.py
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app.py
```

3. Open your browser and navigate to:
```
http://localhost:8501
```

## Project Structure

```
backend/
├── app.py              # Streamlit frontend
├── base.py            # Flask backend
├── generativeResources.py  # AI resource generation
├── quiz.py            # Quiz generation logic
├── roadmap.py         # Learning roadmap generation
├── requirements.txt   # Project dependencies
└── .env              # Environment variables
```

## API Endpoints

- `/api/roadmap`: Generate personalized learning roadmap
- `/api/quiz`: Generate quiz questions
- `/api/generate-resource`: Generate learning resources

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Streamlit for the frontend framework
- Flask for the backend framework 