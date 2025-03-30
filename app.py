#app py
import streamlit as st
import requests
import json
import sys
import os
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Personalized Learning Platform",
    page_icon="🧠",
    layout="wide"
)

# Define API URL (adjust if needed)
API_URL = "http://localhost:5001"  # Flask runs on port 5001

# Initialize session state for storing quiz data
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'show_reason' not in st.session_state:
    st.session_state.show_reason = False

# Navigation sidebar
st.sidebar.title("AI Learning Platform")
page = st.sidebar.radio(
    "Navigate", 
    ["Home", "Learning Roadmap", "Learning Resources", "Quiz"]
)

# Helper function for API calls
def api_call(endpoint, data):
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Home page
if page == "Home":
    st.title("Welcome to AI Personalized Learning Platform")
    st.write("This platform helps you create personalized learning paths, access relevant resources, and test your knowledge.")
    
    # Quick access cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### Create Roadmap\nGenerate a personalized learning path based on your interests and knowledge level.")
        if st.button("Create Learning Path", key="home_roadmap"):
            st.session_state.page = "Learning Roadmap"
            
    with col2:
        st.info("### Access Resources\nGet AI-generated learning resources for your specific needs.")
        if st.button("Explore Resources", key="home_resources"):
            st.session_state.page = "Learning Resources"
            
    with col3:
        st.info("### Test Knowledge\nTake quizzes to reinforce your learning and track progress.")
        if st.button("Take a Quiz", key="home_quiz"):
            st.session_state.page = "Quiz"

# Learning Roadmap page
elif page == "Learning Roadmap":
    st.title("Create Your Learning Roadmap")
    
    with st.form("roadmap_form"):
        topic = st.text_input("What would you like to learn?", placeholder="e.g., Machine Learning, Web Development")
        
        col1, col2 = st.columns(2)
        with col1:
            time_options = ["2 weeks", "4 weeks", "8 weeks", "12 weeks"]
            time = st.selectbox("How much time do you have?", time_options)
        
        with col2:
            knowledge_levels = ["Absolute Beginner", "Beginner", "Intermediate", "Advanced"]
            knowledge_level = st.selectbox("Your current knowledge level:", knowledge_levels)
        
        submit_button = st.form_submit_button("Generate Roadmap")
    
    if submit_button:
        with st.spinner("Generating your personalized learning roadmap..."):
            roadmap_data = api_call("/api/roadmap", {
                "topic": topic,
                "time": time,
                "knowledge_level": knowledge_level
            })
            
            if roadmap_data:
                st.success(f"Your personalized roadmap for learning {topic} is ready!")
                
                # Display the roadmap
                for week, week_data in roadmap_data.items():
                    with st.expander(f"{week.title()}: {week_data.get('topic', '')}"):
                        for i, subtopic in enumerate(week_data.get("subtopics", [])):
                            st.subheader(f"{i+1}. {subtopic.get('subtopic', '')}")
                            st.caption(f"⏱️ Estimated time: {subtopic.get('time', 'Not specified')}")
                            st.write(subtopic.get('description', ''))
                
                # Save roadmap option
                if st.download_button(
                    "Download Roadmap",
                    data=json.dumps(roadmap_data, indent=4),
                    file_name=f"{topic.replace(' ', '_')}_roadmap_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                ):
                    st.success("Roadmap downloaded successfully!")

# Learning Resources page
elif page == "Learning Resources":
    st.title("Get Personalized Learning Resources")
    
    with st.form("resources_form"):
        course = st.text_input("Course/Subject", placeholder="e.g., Python Programming, Data Science")
        
        col1, col2 = st.columns(2)
        with col1:
            knowledge_levels = ["Absolute Beginner", "Beginner", "Intermediate", "Advanced"]
            knowledge_level = st.selectbox("Your knowledge level:", knowledge_levels)
        
        with col2:
            time_options = ["1 hour", "1 day", "1 week", "1 month"]
            time = st.selectbox("Learning timeframe:", time_options)
        
        description = st.text_area("What specifically do you want to learn?", 
                                  placeholder="e.g., I want to learn how to build a web application with Flask")
        
        submit_button = st.form_submit_button("Generate Resources")
    
    if submit_button:
        with st.spinner("Generating personalized learning resources..."):
            resources_data = api_call("/api/generate-resource", {
                "course": course,
                "knowledge_level": knowledge_level,
                "description": description,
                "time": time
            })
            
            if resources_data and "content" in resources_data:
                st.success(f"Here are your personalized resources for {course}:")
                st.markdown(resources_data["content"])
                
                # Download option
                if st.download_button(
                    "Download Resources",
                    data=resources_data["content"],
                    file_name=f"{course.replace(' ', '_')}_resources_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                ):
                    st.success("Resources downloaded successfully!")
            else:
                st.error("Failed to generate resources. Please try again.")

# Quiz page
elif page == "Quiz":
    st.title("Test Your Knowledge")
    
    # Quiz form or quiz display based on state
    if st.session_state.current_quiz is None:
        with st.form("quiz_form"):
            course = st.text_input("Course", placeholder="e.g., Computer Science")
            topic = st.text_input("Topic", placeholder="e.g., Data Structures")
            subtopic = st.text_input("Subtopic", placeholder="e.g., Binary Trees")
            description = st.text_area("Description", placeholder="e.g., Understanding tree traversal algorithms including in-order, pre-order, and post-order traversal")
            
            submit_button = st.form_submit_button("Generate Quiz")
        
        if submit_button:
            with st.spinner("Generating quiz questions..."):
                quiz_data = api_call("/api/quiz", {
                    "course": course,
                    "topic": topic,
                    "subtopic": subtopic,
                    "description": description
                })
                
                if quiz_data and "questions" in quiz_data:
                    st.session_state.current_quiz = quiz_data["questions"]
                    st.session_state.current_question_idx = 0
                    st.session_state.score = 0
                    st.session_state.quiz_completed = False
                    st.session_state.selected_answer = None
                    st.session_state.show_reason = False
                    st.rerun()
    
    # Display current quiz question
    else:
        # If quiz is completed, show results
        if st.session_state.quiz_completed:
            st.success(f"Quiz completed! Your score: {st.session_state.score}/{len(st.session_state.current_quiz)}")
            
            # Show summary of questions and answers
            for i, q in enumerate(st.session_state.current_quiz):
                with st.expander(f"Question {i+1}: {q['question']}"):
                    st.write(f"**Correct Answer:** {q['options'][int(q['answerIndex'])]}")
                    st.write(f"**Explanation:** {q.get('reason', 'No explanation provided')}")
            
            if st.button("Take Another Quiz"):
                st.session_state.current_quiz = None
                st.rerun()
        
        # Display the current question
        else:
            questions = st.session_state.current_quiz
            idx = st.session_state.current_question_idx
            
            if idx < len(questions):
                current_q = questions[idx]
                
                # Progress bar
                st.progress((idx) / len(questions))
                st.write(f"Question {idx+1} of {len(questions)}")
                
                # Question and options
                st.subheader(current_q["question"])
                
                # If answer already selected, disable the radio buttons
                if st.session_state.selected_answer is not None:
                    selected_option = st.radio(
                        "Select your answer:",
                        current_q["options"],
                        index=st.session_state.selected_answer,
                        disabled=True
                    )
                    
                    # Show if answer is correct
                    if st.session_state.selected_answer == int(current_q["answerIndex"]):
                        st.success("Correct! ✅")
                    else:
                        st.error(f"Incorrect. The correct answer is: {current_q['options'][int(current_q['answerIndex'])]} ❌")
                    
                    # Show explanation
                    if st.session_state.show_reason:
                        st.info(f"**Explanation:** {current_q.get('reason', 'No explanation provided')}")
                    
                    # Buttons for navigation
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        if st.button("Show Explanation"):
                            st.session_state.show_reason = True
                            st.rerun()
                    
                    with col3:
                        if idx < len(questions) - 1:
                            if st.button("Next Question"):
                                st.session_state.current_question_idx += 1
                                st.session_state.selected_answer = None
                                st.session_state.show_reason = False
                                st.rerun()
                        else:
                            if st.button("Finish Quiz"):
                                st.session_state.quiz_completed = True
                                st.rerun()
                
                # If no answer selected yet, enable the radio buttons
                else:
                    selected_option = st.radio(
                        "Select your answer:",
                        current_q["options"]
                    )
                    
                    if st.button("Submit Answer"):
                        selected_idx = current_q["options"].index(selected_option)
                        st.session_state.selected_answer = selected_idx
                        
                        # Update score if correct
                        if selected_idx == int(current_q["answerIndex"]):
                            st.session_state.score += 1
                        
                        st.rerun()