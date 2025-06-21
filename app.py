import streamlit as st
import base64
import os
import pygame
from streamlit_lottie import st_lottie
import requests
from chatbot import ChatBot
from quiz_data import QuizModule
from utils import get_avatar_svg, apply_theme, get_language_options, get_lottie_url
from study_materials import StudyMaterials
from auth import show_login, show_admin_panel, logout, AuthSystem

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
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "chat"
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'student_progress' not in st.session_state:
    st.session_state.student_progress = {}

# Initialize modules
chatbot = ChatBot()
quiz_module = QuizModule()
study_materials = StudyMaterials()

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def main():
    st.set_page_config(
        page_title="Vidya Sakhi - Your Learning Bestie",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply theme
    apply_theme(st.session_state.theme)
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_login()
        return
    
    # Show appropriate interface based on user role
    if st.session_state.user_role == "admin":
        show_admin_interface()
    elif st.session_state.user_role == "teacher":
        show_teacher_interface()
    else:  # student
        show_student_interface()

def show_student_interface():
    """Main student interface"""
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
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
        if st.button("🎯 New Quiz", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_current = 0
            st.session_state.quiz_answers = []
            st.session_state.active_tab = "quiz"
        if st.button("💬 Chat with Sakhi", use_container_width=True):
            st.session_state.active_tab = "chat"
        if st.button("📖 Study Materials", use_container_width=True):
            st.session_state.active_tab = "study"
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.active_tab = "analytics"
        if st.button("ℹ️ About Us", use_container_width=True):
            st.session_state.active_tab = "about"
        if st.button("📞 Contact", use_container_width=True):
            st.session_state.active_tab = "contact"
    
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
    
    # Avatar with Lottie animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lottie_animation = load_lottie_url(get_lottie_url())
        if lottie_animation:
            st_lottie(lottie_animation, height=200, key="avatar")
        else:
            st.markdown(get_avatar_svg(), unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💬 Chat with Sakhi", "🧠 Quiz Time", "📖 Study Materials", "📊 Analytics", "ℹ️ About Us", "📞 Contact"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        quiz_interface()
    
    with tab3:
        study_materials_interface()
    
    with tab4:
        analytics_interface()
    
    with tab5:
        about_us_interface()
    
    with tab6:
        contact_interface()

def show_teacher_interface():
    """Teacher interface with additional functionality"""
    with st.sidebar:
        st.markdown(f"### 👩‍🏫 Welcome {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.markdown("### 🎯 Settings")
        
        # Same settings as student
        st.session_state.selected_class = st.selectbox(
            "Select Class",
            options=list(range(3, 13)),
            index=st.session_state.selected_class - 3,
            key="class_selector"
        )
        
        languages = get_language_options()
        st.session_state.selected_language = st.selectbox(
            "Select Language",
            options=list(languages.keys()),
            index=list(languages.keys()).index(st.session_state.selected_language),
            key="language_selector"
        )
        
        theme_options = {"Light": "light", "Dark": "dark"}
        selected_theme = st.selectbox(
            "Theme",
            options=list(theme_options.keys()),
            index=0 if st.session_state.theme == 'light' else 1
        )
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()
        
        st.session_state.voice_enabled = st.toggle(
            "🔊 Voice Output",
            value=st.session_state.voice_enabled
        )
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #4CAF50; font-size: 3rem; margin-bottom: 0.5rem;">
            🌟 Vidya Sakhi - Teacher Portal 🌟
        </h1>
        <h3 style="color: #666; font-weight: 300;">
            Manage Study Materials & Monitor Progress
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Teacher tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Manage Study Materials", "💬 Chat with Sakhi", "🧠 Quiz Time", "📊 Student Progress"])
    
    with tab1:
        teacher_study_materials()
        st.markdown("---")
        teacher_quiz_management()
    
    with tab2:
        chat_interface()
    
    with tab3:
        quiz_interface()
    
    with tab4:
        teacher_analytics_dashboard()

def show_admin_interface():
    """Admin interface"""
    with st.sidebar:
        st.markdown(f"### 👑 Welcome {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #4CAF50; font-size: 3rem; margin-bottom: 0.5rem;">
            🌟 Vidya Sakhi - Admin Portal 🌟
        </h1>
        <h3 style="color: #666; font-weight: 300;">
            System Administration & User Management
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    show_admin_panel()

def teacher_study_materials():
    """Teacher interface for managing study materials"""
    st.markdown("### 📚 Manage Study Materials")
    
    # Class and subject selection
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("Select Class", list(range(3, 13)))
    with col2:
        subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "Hindi", "Telugu", "History", "Geography", "Civics"]
        selected_subject = st.selectbox("Select Subject", subjects)
    
    st.markdown("---")
    
    # Upload new study material
    st.markdown("#### Upload New Study Material")
    uploaded_file = st.file_uploader(
        f"Upload {selected_subject} material for Class {selected_class}",
        type=['pdf', 'doc', 'docx', 'txt']
    )
    
    if uploaded_file:
        description = st.text_area("Material Description")
        if st.button("Save Material"):
            # Save the uploaded file (implementation needed)
            st.success(f"Study material for {selected_subject} - Class {selected_class} uploaded successfully!")
    
    st.markdown("---")
    
    # View existing materials
    st.markdown("#### Existing Materials")
    study_materials = StudyMaterials()
    materials = study_materials.get_materials_for_class(selected_class)
    
    if selected_subject in materials:
        material = materials[selected_subject]
        st.write(f"**Description:** {material['description']}")
        st.write("**Resources:**")
        for resource in material.get('resources', []):
            st.write(f"• {resource}")
        
        if st.button(f"Replace {selected_subject} Material"):
            st.info("Upload new material above to replace existing content")
    else:
        st.info(f"No materials found for {selected_subject} - Class {selected_class}")
        st.write("Upload new material above to add content for this subject.")

def teacher_quiz_management():
    """Teacher interface for adding quiz questions"""
    st.markdown("### ➕ Add Quiz Questions")
    
    col1, col2 = st.columns(2)
    with col1:
        add_class = st.selectbox("Select Class for Question", list(range(3, 13)), key="add_q_class")
    with col2:
        subjects = quiz_module.get_subjects_for_class(add_class)
        add_subject = st.selectbox("Select Subject for Question", subjects, key="add_q_subject")
    
    with st.form("add_question_form"):
        question_text = st.text_area("Question", placeholder="Enter your question here...")
        
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.text_input("Option A")
            option2 = st.text_input("Option B")
        with col2:
            option3 = st.text_input("Option C")
            option4 = st.text_input("Option D")
        
        correct_answer = st.selectbox("Correct Answer", ["Option A", "Option B", "Option C", "Option D"])
        
        if st.form_submit_button("Add Question"):
            if question_text and option1 and option2 and option3 and option4:
                options = [option1, option2, option3, option4]
                correct_idx = ["Option A", "Option B", "Option C", "Option D"].index(correct_answer)
                
                question_data = {
                    'question': question_text,
                    'options': options,
                    'correct_answer': options[correct_idx]
                }
                
                if quiz_module.add_question(add_class, add_subject, question_data):
                    st.success(f"Question added successfully to {add_subject} - Class {add_class}!")
                else:
                    st.error("Failed to add question")
            else:
                st.error("Please fill all fields")

def analytics_interface():
    """Student analytics and progress dashboard"""
    st.markdown("### 📊 Your Learning Analytics")
    
    if not st.session_state.quiz_history:
        st.info("No quiz history available. Take some quizzes to see your progress!")
        return
    
    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total_quizzes = len(st.session_state.quiz_history)
    completed_quizzes = len([q for q in st.session_state.quiz_history if q['status'] == 'Completed'])
    avg_score = sum(q['score'] for q in st.session_state.quiz_history) / total_quizzes if total_quizzes > 0 else 0
    
    with col1:
        st.metric("Total Quizzes", total_quizzes)
    with col2:
        st.metric("Completed", completed_quizzes)
    with col3:
        st.metric("Average Score", f"{avg_score:.1f}%")
    with col4:
        highest_score = max((q['score'] for q in st.session_state.quiz_history), default=0)
        st.metric("Best Score", f"{highest_score:.1f}%")
    
    st.markdown("---")
    
    # Recent quiz history
    st.markdown("### 📈 Recent Quiz History")
    if st.session_state.quiz_history:
        import pandas as pd
        df = pd.DataFrame(st.session_state.quiz_history)
        st.dataframe(df, use_container_width=True)
    
    # Subject-wise performance
    st.markdown("### 📚 Subject Performance")
    subject_scores = {}
    for quiz in st.session_state.quiz_history:
        subject = quiz['subject']
        if subject not in subject_scores:
            subject_scores[subject] = []
        subject_scores[subject].append(quiz['score'])
    
    if subject_scores:
        for subject, scores in subject_scores.items():
            avg_score = sum(scores) / len(scores)
            st.write(f"**{subject}:** {avg_score:.1f}% average ({len(scores)} quizzes)")
            st.progress(avg_score / 100)

def teacher_analytics_dashboard():
    """Teacher analytics dashboard"""
    st.markdown("### 📊 Student Progress Dashboard")
    
    # This would typically connect to a database to show all students' progress
    st.info("""
    **Teacher Analytics Dashboard**
    
    This section will show:
    - Overall class performance
    - Individual student progress
    - Subject-wise statistics
    - Quiz completion rates
    - Performance trends
    
    Currently showing demo data. In a full implementation, this would connect to a student database.
    """)
    
    # Demo metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", "45")
    with col2:
        st.metric("Active This Week", "38")
    with col3:
        st.metric("Average Score", "78.5%")
    with col4:
        st.metric("Quizzes Completed", "156")

def about_us_interface():
    """About Us section"""
    st.markdown("### ℹ️ About Vidya Sakhi")
    
    st.markdown("""
    ## 🌟 Your AI Learning Companion
    
    **Vidya Sakhi** is an innovative educational platform designed specifically for Indian school students from Classes 3-12. Our mission is to make learning engaging, accessible, and fun for every student.
    
    ### 🎯 What We Offer
    
    **For Students:**
    - 🤖 AI-powered chat assistance for all subjects
    - 🧠 Interactive quizzes with instant feedback
    - 📚 Comprehensive study materials
    - 🗣️ Multi-language support including Hindi, Telugu, and regional languages
    - 🔊 Voice assistance for better learning
    - 📊 Personal progress tracking and analytics
    
    **For Teachers:**
    - 📝 Easy quiz question management
    - 📋 Student progress monitoring
    - 📁 Study material upload and organization
    - 📊 Class performance analytics
    
    **For Administrators:**
    - 👥 User management system
    - 📈 System-wide analytics
    - 🔧 Platform administration tools
    
    ### 🌍 Our Vision
    
    To democratize quality education by providing every Indian student with a personalized AI tutor that understands their language, culture, and learning needs.
    
    ### 🏆 Key Features
    
    - **Multi-lingual Support:** Learn in your preferred language
    - **AI-Powered:** Intelligent responses powered by advanced AI
    - **Comprehensive Content:** Covers all major subjects and classes
    - **Voice Enabled:** Audio support for better accessibility
    - **Progress Tracking:** Monitor your learning journey
    - **Secure & Safe:** Protected user data and safe learning environment
    
    ### 🙏 Acknowledgments
    
    Vidya Sakhi is built with love for Indian students, incorporating the best of modern technology with traditional educational values.
    """)

def contact_interface():
    """Contact section"""
    st.markdown("### 📞 Contact Us")
    
    st.markdown("""
    ## Get in Touch
    
    We'd love to hear from you! Whether you have questions, suggestions, or need support, our team is here to help.
    
    ### 📧 Contact Information
    
    **Email:** [Contact email to be added]
    **Phone:** [Contact phone to be added]
    **Address:** [Office address to be added]
    
    ### 🕒 Support Hours
    
    - **Monday - Friday:** 9:00 AM - 6:00 PM
    - **Saturday:** 10:00 AM - 4:00 PM
    - **Sunday:** Closed
    
    ### 💬 Quick Contact Form
    """)
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*")
            email = st.text_input("Email Address*")
        with col2:
            phone = st.text_input("Phone Number")
            subject = st.selectbox("Subject", ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"])
        
        message = st.text_area("Message*", placeholder="Please describe your query or feedback...")
        
        if st.form_submit_button("Send Message"):
            if name and email and message:
                st.success("Thank you for your message! We'll get back to you soon.")
                st.info("Note: This is a demo form. In production, this would send an actual email.")
            else:
                st.error("Please fill in all required fields marked with *")
    
    st.markdown("""
    ### 🤝 Connect With Us
    
    - **GitHub:** [Repository link to be added]
    - **LinkedIn:** [LinkedIn profile to be added]
    - **Twitter:** [Twitter handle to be added]
    
    ### 📚 Resources
    
    - **User Guide:** [Link to user documentation]
    - **FAQs:** [Link to frequently asked questions]
    - **Video Tutorials:** [Link to tutorial videos]
    
    ### 🆘 Emergency Support
    
    For urgent technical issues during school hours, please contact our emergency support line:
    **Emergency Phone:** [Emergency contact to be added]
    """)

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
    
    # Chat input with Enter key support
    user_input = st.chat_input("Ask me anything about your studies!")
    
    if user_input:
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
        try:
            chatbot.speak_text(response, st.session_state.selected_language)
        except Exception as e:
            pass  # Silently handle voice errors

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
        st.session_state.quiz_subject = selected_subject  # Store for analytics
    
    with col2:
        st.markdown("#### Quiz Settings")
        num_questions = st.slider("Number of questions:", 1, 10, 5)
    
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
    
    # Voice output for question
    if st.session_state.voice_enabled and st.button("🔊 Read Question", key=f"read_q_{current_idx}"):
        try:
            chatbot.speak_text(question['question'], st.session_state.selected_language)
        except:
            pass
    
    # Options
    selected_option = st.radio(
        "Choose your answer:",
        question['options'],
        key=f"q_{current_idx}"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
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
            
            # Voice output for quiz feedback
            if st.session_state.voice_enabled:
                feedback_text = "Correct! Well done!" if is_correct else f"Incorrect. The correct answer is {question['correct_answer']}"
                try:
                    chatbot.speak_text(feedback_text, st.session_state.selected_language)
                except:
                    pass
            
            # Move to next question
            st.session_state.quiz_current += 1
            
            # Auto advance after showing result
            if st.session_state.quiz_current < len(questions):
                if st.button("Next Question", type="secondary"):
                    st.rerun()
            else:
                st.rerun()
    
    with col2:
        if st.button("🚪 Exit Quiz", type="secondary", use_container_width=True):
            from datetime import datetime
            # Calculate current score
            correct_answers = sum(1 for ans in st.session_state.quiz_answers if ans['is_correct'])
            current_score = correct_answers / len(st.session_state.quiz_answers) * 100 if st.session_state.quiz_answers else 0
            
            # Save to quiz history
            quiz_record = {
                'date': str(datetime.now().date()),
                'subject': st.session_state.get('quiz_subject', 'Unknown'),
                'class': st.session_state.selected_class,
                'questions_attempted': len(st.session_state.quiz_answers),
                'score': current_score,
                'status': 'Incomplete'
            }
            st.session_state.quiz_history.append(quiz_record)
            
            # Reset quiz state
            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_current = 0
            st.session_state.quiz_answers = []
            
            st.warning(f"Quiz exited! Your score: {current_score:.1f}% ({correct_answers}/{len(st.session_state.quiz_answers)} questions)")
            st.rerun()

def show_quiz_results():
    st.markdown("### 🎉 Quiz Completed!")
    
    from datetime import datetime
    score = st.session_state.quiz_score
    total = len(st.session_state.quiz_questions)
    percentage = (score / total) * 100
    
    # Save to quiz history
    quiz_record = {
        'date': str(datetime.now().date()),
        'subject': st.session_state.get('quiz_subject', 'Unknown'),
        'class': st.session_state.selected_class,
        'questions_attempted': total,
        'score': percentage,
        'status': 'Completed'
    }
    st.session_state.quiz_history.append(quiz_record)
    
    # Update student progress
    subject = st.session_state.get('quiz_subject', 'Unknown')
    if subject not in st.session_state.student_progress:
        st.session_state.student_progress[subject] = []
    st.session_state.student_progress[subject].append({
        'date': str(datetime.now().date()),
        'score': percentage,
        'questions': total
    })
    
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
                try:
                    pdf_data = study_materials.generate_sample_pdf(subject, st.session_state.selected_class)
                    st.download_button(
                        label=f"📄 Download {subject} Notes",
                        data=pdf_data,
                        file_name=f"{subject}_Class_{st.session_state.selected_class}_Notes.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.warning(f"PDF generation temporarily unavailable for {subject}. Please try again later.")
            
            # Additional resources
            if content.get('resources'):
                st.markdown("**Additional Resources:**")
                for resource in content['resources']:
                    st.markdown(f"• {resource}")

if __name__ == "__main__":
    main()
