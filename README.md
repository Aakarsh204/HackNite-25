# HackNite’25

## Problem Statement:

Education

Develop a personalized, Al-driven educational platform that dynamically adapts learning pathways and content delivery based on real-time student engagement, emotional state, and cognitive load, captured through multimodal data (e.g., eye-tracking, facial expression analysis, speech patterns, interaction logs). The challenge lies in creating a system that not only optimizes knowledge acquisition but also fosters intrinsic motivation and emotional well-being, while maintaining ethical considerations regarding student privacy and data usage.

## Solution:

An AI-powered learning platform that provides personalized learning experiences through dynamic content generation, interactive quizzes, and adaptive learning paths.

Solution Link: [HackNite'25](https://youtu.be/y5tPg5xu3kY)

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

- Python 3.10+
- Google Gemini API Key
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aakarsh204/HackNite-25.git
cd HackNite-25
```

2. Create and activate a virtual environment:
```bash
python -m venv hacknite
source hacknite/bin/activate  # On Windows use: hacknite\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with your Google Gemini API key:
```
echo GEMINI_API_KEY=your_api_key > .env
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
