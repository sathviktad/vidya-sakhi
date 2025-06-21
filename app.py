import streamlit as st
import base64
import os
import pygame
from chatbot import ChatBot
from quiz_data import QuizModule
from utils import get_avatar_svg, apply_theme, get_language_options
from study_materials import StudyMaterials

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_current' not in st.session_state:
    st.session_state.quiz_current = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'selected_class' not in st.session_state:
    st.session_state.selected_class = 5
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'

# Initialize modules
chatbot = ChatBot()
quiz_module = QuizModule()
study_materials = StudyMaterials()

def main():
    st.set_page_config(
        page_title="Vidya Sakhi - Your Learning Bestie",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply theme
    apply_theme(st.session_state.theme)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Settings")
        
        # Class selection
        st.session_state.selected_class = st.selectbox(
            "Select Class",
            options=list(range(3, 13)),
            index=st.session_state.selected_class - 3,
            key="class_selector"
        )
        
        # Language selection
        languages = get_language_options()
        st.session_state.selected_language = st.selectbox(
            "Select Language",
            options=list(languages.keys()),
            index=list(languages.keys()).index(st.session_state.selected_language),
            key="language_selector"
        )
        
        # Theme toggle
        theme_options = {"Light": "light", "Dark": "dark"}
        selected_theme = st.selectbox(
            "Theme",
            options=list(theme_options.keys()),
            index=0 if st.session_state.theme == 'light' else 1
        )
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()
        
        # Voice toggle
        st.session_state.voice_enabled = st.toggle(
            "🔊 Voice Output",
            value=st.session_state.voice_enabled
        )
        
        st.markdown("---")
        st.markdown("### 📚 Quick Access")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.quiz_started = False
        if st.button("🎯 New Quiz", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_current = 0
            st.session_state.quiz_answers = []
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #4CAF50; font-size: 3rem; margin-bottom: 0.5rem;">
            🌟 Vidya Sakhi 🌟
        </h1>
        <h3 style="color: #666; font-weight: 300;">
            Your Learning Bestie & AI Companion
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Avatar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(get_avatar_svg(), unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat with Sakhi", "🧠 Quiz Time", "📖 Study Materials"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        quiz_interface()
    
    with tab3:
        study_materials_interface()

def chat_interface():
    st.markdown("### 💬 Chat with Your AI Companion")
    
    # Chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message.get("translation"):
                    st.caption(f"*Translation: {message['translation']}*")
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask me anything about your studies!",
            key="chat_input",
            placeholder="Type your question here..."
        )
    
    with col2:
        ask_button = st.button("Ask Sakhi", type="primary", use_container_width=True)
    
    # Process input
    if user_input and (ask_button or st.session_state.get('chat_input_enter')):
        process_chat_input(user_input)
        st.rerun()

def process_chat_input(user_input):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get bot response
    response, translation = chatbot.get_response(
        user_input, 
        st.session_state.selected_language
    )
    
    # Add bot response
    bot_message = {
        "role": "assistant",
        "content": response
    }
    
    if translation and translation != response:
        bot_message["translation"] = translation
    
    st.session_state.messages.append(bot_message)
    
    # Voice output
    if st.session_state.voice_enabled:
        chatbot.speak_text(response, st.session_state.selected_language)

def quiz_interface():
    if not st.session_state.quiz_started:
        show_quiz_menu()
    else:
        show_quiz_questions()

def show_quiz_menu():
    st.markdown("### 🧠 Test Your Knowledge")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Select Subject")
        subjects = quiz_module.get_subjects_for_class(st.session_state.selected_class)
        selected_subject = st.selectbox("Choose a subject:", subjects)
    
    with col2:
        st.markdown("#### Quiz Settings")
        num_questions = st.slider("Number of questions:", 5, 20, 10)
    
    if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
        questions = quiz_module.generate_quiz(
            st.session_state.selected_class,
            selected_subject,
            num_questions,
            st.session_state.selected_language
        )
        
        if questions:
            st.session_state.quiz_questions = questions
            st.session_state.quiz_started = True
            st.session_state.quiz_current = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = []
            st.rerun()
        else:
            st.error("No questions available for this combination. Please try different settings.")

def show_quiz_questions():
    questions = st.session_state.quiz_questions
    current_idx = st.session_state.quiz_current
    
    if current_idx >= len(questions):
        show_quiz_results()
        return
    
    question = questions[current_idx]
    
    # Progress bar
    progress = (current_idx + 1) / len(questions)
    st.progress(progress)
    st.markdown(f"**Question {current_idx + 1} of {len(questions)}**")
    
    # Question
    st.markdown(f"### {question['question']}")
    
    # Options
    selected_option = st.radio(
        "Choose your answer:",
        question['options'],
        key=f"q_{current_idx}"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("Submit Answer", type="primary", use_container_width=True):
            # Check answer
            is_correct = selected_option == question['correct_answer']
            if is_correct:
                st.session_state.quiz_score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect! The correct answer is: {question['correct_answer']}")
            
            st.session_state.quiz_answers.append({
                'question': question['question'],
                'selected': selected_option,
                'correct': question['correct_answer'],
                'is_correct': is_correct
            })
            
            # Move to next question
            st.session_state.quiz_current += 1
            
            # Auto advance after showing result
            if st.session_state.quiz_current < len(questions):
                if st.button("Next Question", type="secondary"):
                    st.rerun()
            else:
                st.rerun()

def show_quiz_results():
    st.markdown("### 🎉 Quiz Completed!")
    
    score = st.session_state.quiz_score
    total = len(st.session_state.quiz_questions)
    percentage = (score / total) * 100
    
    # Score display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{score}/{total}")
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        if percentage >= 80:
            st.success("🌟 Excellent!")
        elif percentage >= 60:
            st.info("👍 Good job!")
        else:
            st.warning("📚 Keep studying!")
    
    # Detailed results
    with st.expander("📊 Detailed Results"):
        for i, answer in enumerate(st.session_state.quiz_answers):
            if answer['is_correct']:
                st.success(f"Q{i+1}: ✅ {answer['question'][:50]}...")
            else:
                st.error(f"Q{i+1}: ❌ {answer['question'][:50]}...")
                st.caption(f"Your answer: {answer['selected']}")
                st.caption(f"Correct answer: {answer['correct']}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_current = 0
            st.session_state.quiz_answers = []
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Menu", use_container_width=True):
            st.session_state.quiz_started = False
            st.rerun()

def study_materials_interface():
    st.markdown("### 📖 Study Materials")
    
    materials = study_materials.get_materials_for_class(st.session_state.selected_class)
    
    if not materials:
        st.info("Study materials for this class are being prepared. Please check back soon!")
        return
    
    for subject, content in materials.items():
        with st.expander(f"📚 {subject}"):
            st.markdown(content['description'])
            
            # Download buttons for sample materials
            if content.get('sample_pdf'):
                pdf_data = study_materials.generate_sample_pdf(subject, st.session_state.selected_class)
                st.download_button(
                    label=f"📄 Download {subject} Notes",
                    data=pdf_data,
                    file_name=f"{subject}_Class_{st.session_state.selected_class}_Notes.pdf",
                    mime="application/pdf"
                )
            
            # Additional resources
            if content.get('resources'):
                st.markdown("**Additional Resources:**")
                for resource in content['resources']:
                    st.markdown(f"• {resource}")

if __name__ == "__main__":
    main()
