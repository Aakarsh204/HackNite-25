<<<<<<< HEAD
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
=======
# HackNite’25

Problem Statement:

Education

Develop a personalized, Al-driven educational platform that dynamically adapts learning pathways and content delivery based on real-time student engagement, emotional state, and cognitive load, captured through multimodal data (e.g., eye-tracking, facial expression analysis, speech patterns, interaction logs). The challenge lies in creating a system that not only optimizes knowledge acquisition but also fosters intrinsic motivation and emotional well-being, while maintaining ethical considerations regarding student privacy and data usage.
 

# Goal/Work Division

## Creativity

- [ ]  use of personalized factors like (e.g., eye-tracking, facial expression analysis, speech patterns, interaction logs) for cognitive load (MAYUKH)
    
    [Mayukh’s page](https://www.notion.so/Mayukh-s-page-919a2cc3bce7472fbd0259bbb6d0adbc?pvs=21)
    
- [ ]  how to enhance learning using cognitive load (AAKARSH)
    
    [Aakarsh’s Page](https://www.notion.so/Aakarsh-s-Page-1c5cffea6725805aac13d1aa3e888c26?pvs=21)
    
- [ ]  Gen AI based interaction (summary,content gen)(ARUSH)
    
    [Gen AI ~Arush](https://www.notion.so/Gen-AI-Arush-1c5cffea672580629207ee6134958f4b?pvs=21)
    
- [ ]  Deep learning for generating learning pathways (DHRUV)
    
    [Dhruv Saxena](https://www.notion.so/Dhruv-Saxena-1c5cffea672580708909e83362273932?pvs=21)
    
- [ ]  Gamification- study streak, badges, leader boards

## Collaboration

## Problem Solving

- [ ]  Boredom through automated interaction through above features
- [ ]  Structured, personalized and creative learning

![Screenshot 2025-03-29 at 5.42.40 PM.png](attachment:845b2899-fb86-4c88-88f1-8edf046324d0:59ecdc4b-d94b-490b-a822-70bbb800bd42.png)
>>>>>>> d64d061c90c151e76c8e1dbaffc3040cbb912d2c
