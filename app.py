import streamlit as st
import base64
import os
import pygame
from streamlit_lottie import st_lottie
import requests
from chatbot import ChatBot
from quiz_data import QuizModule
from utils import get_avatar_svg, apply_theme, get_language_options, get_lottie_url, load_quiz_history, append_quiz_history, reset_quiz_history, t, TRANSLATIONS, get_language_code
from study_materials import StudyMaterials
from auth import show_login, show_admin_panel, logout, AuthSystem
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import rcParams
import matplotlib
matplotlib.rcParams['font.family'] = ['Noto Sans', 'Noto Sans Telugu', 'Noto Sans Devanagari', 'Noto Sans Tamil', 'sans-serif']
rcParams.update({'font.size': 10})  # Set default font size smaller for pie chart labels

st.set_page_config(
    page_title="Vidya Sakhi - Your Learning Bestie",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.session_state.active_tab = 0
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'student_progress' not in st.session_state:
    st.session_state.student_progress = {}
if 'quick_access' not in st.session_state:
    st.session_state.quick_access = None

# Initialize modules
chatbot = ChatBot()
quiz_module = QuizModule()
study_materials = StudyMaterials()

# Add Lottie URLs for each section
QUIZ_LOTTIE_URL = "https://lottie.host/6e2e2b6d-quiz-education.json"  # Replace with a real quiz Lottie URL
STUDY_LOTTIE_URL = "https://lottie.host/7a3b1c2d-study-materials.json"  # Replace with a real study Lottie URL
ANALYTICS_LOTTIE_URL = "https://lottie.host/8b4c3d4e-analytics.json"  # Replace with a real analytics Lottie URL
HELP_LOTTIE_URL = get_lottie_url()  # Already used for Help/FAQ

# After imports, add:
def safe_translate(line):
    # Don't translate markdown links
    if line.strip().startswith("[") and "](" in line:
        return line
    return t(line)

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def translate_status(val, lang=None):
    if lang is None:
        lang = st.session_state.get('selected_language', 'en')
    # Always show Telugu only if Telugu is selected
    if lang.lower().startswith('telugu') or lang.lower() in ['te', 'telugu']:
        if str(val).strip().lower() in ['completed', t('completed', 'en').lower(), t('completed', 'te').lower(), t('completed', 'hi').lower()]:
            return t('completed', 'te')
        if str(val).strip().lower() in ['incomplete', t('incomplete', 'en').lower(), t('incomplete', 'te').lower(), t('incomplete', 'hi').lower()]:
            return t('incomplete', 'te')
    else:
        if str(val).strip().lower() in ['completed', t('completed', 'en').lower(), t('completed', 'te').lower(), t('completed', 'hi').lower()]:
            return t('completed', lang)
        if str(val).strip().lower() in ['incomplete', t('incomplete', 'en').lower(), t('incomplete', 'te').lower(), t('incomplete', 'hi').lower()]:
            return t('incomplete', lang)
    return str(val)

def main():
    # Only inject monospace font if dyslexia-friendly toggle is on
    if st.session_state.get('dyslexia_font', False):
        st.markdown(
            """
            <style>
            html, body, .stApp, .css-1v0mbdj, .css-1v3fvcr, .css-1c7y2kd, .css-1offfwp, .css-1lcbmhc, body * {
                font-family: monospace !important;
            }
            </style>
            """,
            unsafe_allow_html=True
    )
    # Ensure default theme is always light on login
    if 'theme' not in st.session_state or st.session_state.theme not in ['theme1', 'theme2']:
        st.session_state.theme = 'theme1'
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
    section_labels = [
        (t('chat_with_sakhi'), "chat"),
        (t('quiz_time'), "quiz"),
        (t('study_materials'), "study"),
        (t('analytics'), "analytics"),
        (t('about_us'), "about"),
        (t('contact'), "contact"),
        (t('help_faq'), "help")
    ]
    section_keys = [k for _, k in section_labels]
    section_display = {k: l for l, k in section_labels}
    if 'main_section' not in st.session_state:
        st.session_state.main_section = 'chat'
    with st.sidebar:
        st.markdown(f"### 👋 {t('welcome')} {st.session_state.user_name}")
        st.markdown(f"**{t('role')}: {st.session_state.user_role.title()}")
        if st.button(f"🚪 {t('logout')}", use_container_width=True):
            logout()
        st.markdown("---")
        st.markdown(f"### 🎯 {t('settings')}")
        st.session_state.selected_class = st.selectbox(
            t('select_class'),
            options=list(range(3, 13)),
            index=st.session_state.selected_class - 3,
            key="class_selector"
        )
        languages = get_language_options()
        st.session_state.selected_language = st.selectbox(
            t('language'),
            options=list(languages.keys()),
            index=list(languages.keys()).index(st.session_state.selected_language),
            key="language_selector"
        )
        theme_options = {"Light": "theme1", "Dark": "theme2"}
        selected_theme = st.selectbox(
            t('theme'),
            options=list(theme_options.keys()),
            index=0 if st.session_state.theme == 'theme1' else 1
        )
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()
        st.session_state.voice_enabled = st.toggle(
            f"🔊 {t('voice_output')}",
            value=st.session_state.voice_enabled
        )
        # Accessibility toggles
        st.markdown("---")
        st.markdown(f"### ♿ {t('accessibility')}")
        large_font = st.toggle(t('large_font'), key="large_font")
        dyslexia_font = st.toggle(t('dyslexia_font'), key="dyslexia_font")
        if large_font:
            st.markdown("""
            <style>
            html, body, .stApp, .css-1v0mbdj, .css-1v3fvcr, .css-1c7y2kd, .css-1offfwp, .css-1lcbmhc {
                font-size: 20px !important;
            }
            </style>
            """, unsafe_allow_html=True)
        if dyslexia_font:
            st.markdown("""
            <style>
            html, body, .stApp, .css-1v0mbdj, .css-1v3fvcr, .css-1c7y2kd, .css-1offfwp, .css-1lcbmhc {
                font-family: monospace !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.info("Dyslexia-Friendly Font (for testing): Monospace. This is not a real dyslexia-friendly font, but you should see a dramatic change when toggled on.")
        st.markdown("---")
        st.markdown(f"### 📚 {t('quick_access')}")
        if st.button(f"💬 {t('chat_with_sakhi')}", use_container_width=True):
            st.session_state.jump_to_section = 'chat'
            st.rerun()
        if st.button(f"🎯 {t('new_quiz')}", use_container_width=True):
            st.session_state.jump_to_section = 'quiz'
            st.rerun()
        if st.button(f"📖 {t('study_materials')}", use_container_width=True):
            st.session_state.jump_to_section = 'study'
            st.rerun()
        st.markdown("---")
        st.markdown(f"### {t('main_menu')}", unsafe_allow_html=True)
        default_section = st.session_state.get('main_section', 'chat')
        if 'jump_to_section' in st.session_state:
            default_section = st.session_state.jump_to_section
            del st.session_state.jump_to_section
        if default_section not in section_keys:
            default_section = 'chat'
        selected_section = st.radio(
            "",
            [l for l, _ in section_labels],
            index=section_keys.index(default_section),
            key="main_section_radio"
        )
        for l, k in section_labels:
            if selected_section == l:
                st.session_state.main_section = k
                break
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #4CAF50; font-size: 3rem; margin-bottom: 0.5rem;">
            🌟 {t('vidya_sakhi')} 🌟
        </h1>
        <h3 style="color: #666; font-weight: 300;">
            {t('learning_bestie')}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lottie_animation = load_lottie_url(get_lottie_url())
        if lottie_animation:
            st_lottie(lottie_animation, height=200, key="avatar")
        else:
            st.markdown(get_avatar_svg(), unsafe_allow_html=True)
    section = st.session_state.main_section
    if section == 'chat':
        chat_interface()
    elif section == 'quiz':
        quiz_interface()
    elif section == 'study':
        study_materials_interface()
    elif section == 'analytics':
        analytics_interface()
    elif section == 'about':
        about_us_interface()
    elif section == 'contact':
        contact_interface()
    elif section == 'help':
        help_faq_interface()
    st.markdown('<div style="text-align:center; color:gray; font-size:0.9rem; margin-top:2rem;">© 2024 Vidya Sakhi. All rights reserved.</div>', unsafe_allow_html=True)

    # Notification banner for new study materials/quizzes
    materials = study_materials.get_materials_for_class(st.session_state.selected_class)
    num_materials = len(materials) if materials else 0
    num_quizzes = len(quiz_module.get_subjects_for_class(st.session_state.selected_class))
    if 'last_seen_materials' not in st.session_state:
        st.session_state.last_seen_materials = num_materials
    if 'last_seen_quizzes' not in st.session_state:
        st.session_state.last_seen_quizzes = num_quizzes
    new_materials = num_materials > st.session_state.last_seen_materials
    new_quizzes = num_quizzes > st.session_state.last_seen_quizzes
    if new_materials or new_quizzes:
        msg = []
        if new_materials:
            msg.append('New study materials have been added for your class!')
        if new_quizzes:
            msg.append('New quizzes are available for your class!')
        st.info(' '.join(msg))
        st.session_state.last_seen_materials = num_materials
        st.session_state.last_seen_quizzes = num_quizzes

def show_teacher_interface():
    # Robust navigation fix for study materials
    if st.session_state.get('goto_study'):
        st.session_state.main_section = 'study'
        st.session_state['main_section_radio_teacher'] = '📚 Manage Study Materials'
        del st.session_state['goto_study']
        st.rerun()
        return
    """Teacher interface with additional functionality"""
    section_labels = [
        ("📚 Manage Study Materials", "study"),
        ("💬 Chat with Sakhi", "chat"),
        ("🧠 Quiz Time", "quiz"),
        ("📊 Student Progress", "progress"),
        ("❓ Help & FAQ", "help")
    ]
    section_keys = [k for _, k in section_labels]
    section_display = {k: l for l, k in section_labels}
    if 'main_section' not in st.session_state:
        st.session_state.main_section = 'study'
    with st.sidebar:
        st.markdown(f"### 👩‍🏫 Welcome {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        st.markdown("---")
        st.markdown("### 🎯 Settings")
        st.session_state.selected_class = st.selectbox(
            "Select Class",
            options=list(range(3, 13)),
            index=st.session_state.selected_class - 3,
            key="class_selector"
        )
        languages = get_language_options()
        st.session_state.selected_language = st.selectbox(
            t('language'),
            options=list(languages.keys()),
            index=list(languages.keys()).index(st.session_state.selected_language),
            key="language_selector"
        )
        theme_options = {"Light": "theme1", "Dark": "theme2"}
        selected_theme = st.selectbox(
            t('theme'),
            options=list(theme_options.keys()),
            index=0 if st.session_state.theme == 'theme1' else 1
        )
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()
        st.session_state.voice_enabled = st.toggle(
            "🔊 Voice Output",
            value=st.session_state.voice_enabled
        )
        # Accessibility toggles
        st.markdown("---")
        st.markdown("### ♿ Accessibility")
        large_font = st.toggle("Large Font", key="large_font")
        dyslexia_font = st.toggle("Dyslexia-Friendly Font", key="dyslexia_font")
        if large_font:
            st.markdown("""
            <style>
            html, body, .stApp, .css-1v0mbdj, .css-1v3fvcr, .css-1c7y2kd, .css-1offfwp, .css-1lcbmhc {
                font-size: 20px !important;
            }
            </style>
            """, unsafe_allow_html=True)
        if dyslexia_font:
            st.markdown("""
            <style>
            html, body, .stApp, .css-1v0mbdj, .css-1v3fvcr, .css-1c7y2kd, .css-1offfwp, .css-1lcbmhc {
                font-family: monospace !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.info("Dyslexia-Friendly Font (for testing): Monospace. This is not a real dyslexia-friendly font, but you should see a dramatic change when toggled on.")
        st.markdown("---")
        st.markdown("### 📚 Quick Access")
        if st.button("💬 Chat with Sakhi", use_container_width=True):
            st.session_state.jump_to_section = 'chat'
            st.rerun()
        if st.button("🎯 New Quiz", use_container_width=True):
            st.session_state.jump_to_section = 'quiz'
            st.rerun()
        if st.button("📚 Study Materials", use_container_width=True):
            st.session_state.jump_to_section = 'study'
            st.rerun()
        if st.button("📊 Student Progress", use_container_width=True):
            st.session_state.jump_to_section = 'progress'
            st.rerun()
        st.markdown("---")
        st.markdown("### Main Menu", unsafe_allow_html=True)
        default_section = st.session_state.get('main_section', 'study')
        if 'jump_to_section' in st.session_state:
            default_section = st.session_state.jump_to_section
            del st.session_state.jump_to_section
        if default_section not in section_keys:
            default_section = 'study'
        selected_section = st.radio(
            "",
            [l for l, _ in section_labels],
            index=section_keys.index(default_section),
            key="main_section_radio_teacher"
        )
        for l, k in section_labels:
            if selected_section == l:
                st.session_state.main_section = k
                break
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
    section = st.session_state.main_section
    if section == 'study':
        teacher_study_materials()
    elif section == 'chat':
        chat_interface()
    elif section == 'quiz':
        quiz_interface()
        st.markdown("---")
        teacher_quiz_management()
    elif section == 'progress':
        teacher_analytics_dashboard()
    elif section == 'help':
        help_faq_interface()
    app_footer()

    # Notification banner for new study materials/quizzes (for all classes)
    total_materials = sum(len(study_materials.get_materials_for_class(cls)) for cls in range(3, 13))
    total_quizzes = sum(len(quiz_module.get_subjects_for_class(cls)) for cls in range(3, 13))
    if 'last_seen_teacher_materials' not in st.session_state:
        st.session_state.last_seen_teacher_materials = total_materials
    if 'last_seen_teacher_quizzes' not in st.session_state:
        st.session_state.last_seen_teacher_quizzes = total_quizzes
    new_teacher_materials = total_materials > st.session_state.last_seen_teacher_materials
    new_teacher_quizzes = total_quizzes > st.session_state.last_seen_teacher_quizzes
    if new_teacher_materials or new_teacher_quizzes:
        msg = []
        if new_teacher_materials:
            msg.append('New study materials have been added!')
        if new_teacher_quizzes:
            msg.append('New quizzes are available!')
        st.info(' '.join(msg))
        st.session_state.last_seen_teacher_materials = total_materials
        st.session_state.last_seen_teacher_quizzes = total_quizzes

def show_admin_interface():
    """Admin interface"""
    section_labels = [
        ("👑 Admin Dashboard", "dashboard"),
        ("❓ Help & FAQ", "help")
    ]
    section_keys = [k for _, k in section_labels]
    if 'main_section' not in st.session_state:
        st.session_state.main_section = 'dashboard'
    with st.sidebar:
        st.markdown(f"### 👑 Welcome {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        st.markdown("---")
        st.markdown("### Main Menu", unsafe_allow_html=True)
        default_section = st.session_state.get('main_section', 'dashboard')
        if default_section not in section_keys:
            default_section = section_keys[0]
        selected_section = st.radio(
            "",
            [l for l, _ in section_labels],
            index=section_keys.index(default_section),
            key="main_section_radio_admin"
        )
        for l, k in section_labels:
            if selected_section == l:
                st.session_state.main_section = k
                break
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
    section = st.session_state.main_section
    if section == 'dashboard':
        show_admin_panel()
    elif section == 'help':
        help_faq_interface()
    app_footer()

    # After the sidebar (before rendering tabs), add:
    if st.session_state.quick_access:
        st.session_state.active_tab = st.session_state.quick_access
        st.session_state.quick_access = None
        st.rerun()

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
            st.success(f"Study material for {selected_subject} - Class {selected_class} uploaded successfully!")
            st.session_state['goto_study'] = True
            st.rerun()
    
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
            st.session_state['goto_study'] = True
            st.rerun()
    else:
        st.info(f"No materials found for {selected_subject} - Class {selected_class}")
        st.write("Upload new material above to add content for this subject.")

def teacher_quiz_management():
    """Teacher interface for adding quiz questions"""
    st.markdown(f"### ➕ {t('add_quiz_questions')}")
    
    col1, col2 = st.columns(2)
    with col1:
        add_class = st.selectbox(t('select_class_for_question'), list(range(3, 13)), key="add_q_class")
    with col2:
        subjects = quiz_module.get_subjects_for_class(add_class)
        add_subject = st.selectbox(t('select_subject_for_question'), subjects, key="add_q_subject")
    
    with st.form("add_question_form"):
        question_text = st.text_area(t('question_label'), placeholder=t('question_placeholder'))
        
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.text_input(t('option_a'))
            option2 = st.text_input(t('option_b'))
        with col2:
            option3 = st.text_input(t('option_c'))
            option4 = st.text_input(t('option_d'))
        
        correct_answer = st.selectbox(t('correct_answer_label'), [t('option_a'), t('option_b'), t('option_c'), t('option_d')])
        
        if st.form_submit_button(t('add_question_btn')):
            if question_text and option1 and option2 and option3 and option4:
                options = [option1, option2, option3, option4]
                correct_idx = [t('option_a'), t('option_b'), t('option_c'), t('option_d')].index(correct_answer)
                
                question_data = {
                    'question': question_text,
                    'options': options,
                    'correct_answer': options[correct_idx]
                }
                
                if quiz_module.add_question(add_class, add_subject, question_data):
                    st.success(t('question_added_success').format(subject=add_subject, class_num=add_class))
                else:
                    st.error(t('failed_to_add_question'))
            else:
                st.error(t('fill_all_fields'))

def teacher_analytics_dashboard():
    """Teacher analytics dashboard"""
    st.markdown(f"### 📊 {t('student_progress_dashboard')}")
    quiz_history = [h for h in load_quiz_history() if h.get('username') == st.session_state.username]
    if not quiz_history:
        st.info(t('no_quiz_history'))
        return
    df = pd.DataFrame(quiz_history)
    # Bar chart: average score per subject
    st.markdown(f"#### {t('average_score_per_subject_all')}")
    if 'subject' in df and 'score' in df:
        subject_scores = df.groupby('subject')['score'].mean()
        st.bar_chart(subject_scores)
    # Line chart: average class score over time
    st.markdown(f"#### {t('average_class_score_over_time')}")
    if 'date' in df and 'score' in df:
        df_sorted = df.sort_values('date')
        avg_scores = df_sorted.groupby('date')['score'].mean()
        st.line_chart(avg_scores)
    # Pie chart: quiz completion status
    st.markdown(f"#### {t('quiz_completion_status_all')}")
    if 'status' in df:
        status_counts = Counter(df['status'])
        status_labels = [t(str(label), 'en') for label in status_counts.keys()]  # Always English
        fig, ax = plt.subplots(figsize=(7, 5))
        num_slices = len(status_labels)
        def autopct_format(pct):
            return '%1.1f%%' % pct if pct > 5 else ''
        wedges, texts, autotexts = ax.pie(
            status_counts.values(),
            labels=status_labels,
            autopct=autopct_format,
            startangle=90,
            pctdistance=1.35,
            labeldistance=1.2,
            wedgeprops=dict(width=0.7, edgecolor='w')
        )
        for i, autotext in enumerate(autotexts):
            autotext.set_fontsize(9)
            if num_slices > 2 and i > 0:
                x, y = autotext.get_position()
                autotext.set_position((x, y - 0.05 * i))
        ax.axis('equal')
        ax.legend(wedges, status_labels, title='Status', loc='center left', bbox_to_anchor=(1, 0.5))
        st.pyplot(fig)
    st.markdown("---")
    # Student selector
    if 'username' in df.columns and 'name' in df.columns and not df.empty:
        student_options = df[['username', 'name']].drop_duplicates().apply(lambda row: f"{row['name']} ({row['username']})", axis=1).tolist()
        selected_student = st.selectbox(t('select_student'), ["-- " + t('select') + " --"] + student_options)
        if selected_student != "-- " + t('select') + " --":
            # Extract username from selection
            username = selected_student.split('(')[-1].replace(')', '').strip()
            student_df = df[df['username'] == username]
            st.markdown(f"#### {t('analytics_for_student').format(student=selected_student)}")
            # Bar chart: average score per subject
            if 'subject' in student_df and 'score' in student_df:
                subject_scores = student_df.groupby('subject')['score'].mean()
                st.bar_chart(subject_scores)
            # Line chart: quiz scores over time
            if 'date' in student_df and 'score' in student_df:
                student_df_sorted = student_df.sort_values('date')
                st.line_chart(student_df_sorted.set_index('date')['score'])
            # Pie chart: completion status
            if 'status' in student_df:
                status_counts = Counter(student_df['status'])
                status_labels = [t(str(label), 'en') for label in status_counts.keys()]
                fig, ax = plt.subplots(figsize=(7, 5))  # Larger figure for clarity
                wedges, texts, autotexts = ax.pie(
                    status_counts.values(),
                    labels=status_labels,
                    autopct=autopct_format,
                    startangle=90,
                    pctdistance=1.35,      # Move percentages further out
                    labeldistance=1.2,     # Move labels further out
                    wedgeprops=dict(width=0.7, edgecolor='w')  # Donut style for clarity
                )
                # Manually adjust vertical position of percentage labels for small slices
                for i, autotext in enumerate(autotexts):
                    autotext.set_fontsize(9)
                    # For small slices, stagger the y position
                    if len(status_labels) > 2 and i > 0:
                        x, y = autotext.get_position()
                        autotext.set_position((x, y - 0.05 * i))
                ax.axis('equal')
                ax.legend(wedges, status_labels, title='Status', loc='center left', bbox_to_anchor=(1, 0.5))
                st.pyplot(fig)
            st.markdown(f"### 📈 {t('recent_quiz_history_student')}")
            st.dataframe(student_df, use_container_width=True)
        else:
            st.info(t('no_student_quiz_data'))
    st.markdown("---")
    # Recent quiz history table
    st.markdown(f"### 📈 {t('recent_quiz_history_all')}")
    st.dataframe(df, use_container_width=True)
    # Add Reset Analytics button
    st.markdown("---")
    st.markdown(f"### ⚠️ {t('reset_analytics')}")
    student_options = df[['username', 'name']].drop_duplicates().apply(lambda row: f"{row['name']} ({row['username']})", axis=1).tolist()
    reset_choice = st.selectbox(t('select_student_to_reset'), [t('all')] + student_options, key="reset_analytics")
    if st.button(t('reset_analytics_btn'), key="reset_analytics_btn"):
        if reset_choice == t('all'):
            reset_quiz_history()
            st.success(t('all_analytics_reset'))
        else:
            username = reset_choice.split('(')[-1].replace(')', '').strip()
            reset_quiz_history(username=username)
            st.success(t('analytics_reset_for_student').format(student=reset_choice))
        st.rerun()
    # Export analytics as CSV
    st.markdown("---")
    st.markdown(f"### ⬇️ {t('export_analytics')}")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=t('download_analytics_csv'),
        data=csv,
        file_name="student_analytics.csv",
        mime="text/csv"
    )
    # Leaderboard
    st.markdown("---")
    st.markdown(f"### 🏅 {t('leaderboard_top_students')}")
    if 'username' in df.columns and 'score' in df.columns:
        leaderboard = df.groupby(['username', 'name'])['score'].mean().reset_index()
        leaderboard = leaderboard.sort_values('score', ascending=False).head(10)
        st.dataframe(leaderboard.rename(columns={'score': t('avg_score_percent')}), use_container_width=True)

def chat_interface():
    st.markdown(f"### 💬 {t('chat_with_ai_companion')}")
    chat_container = st.container()
    with chat_container:
        # Group messages as user+AI pairs
        messages = st.session_state.messages
        i = 0
        while i < len(messages):
            if messages[i]["role"] == "user":
                user_msg = messages[i]["content"]
                ai_msg = ""
                translation = None
                if i+1 < len(messages) and messages[i+1]["role"] == "assistant":
                    ai_msg = messages[i+1]["content"]
                    translation = messages[i+1].get("translation")
                with st.container():
                    cols = st.columns([12,1])
                    with cols[0]:
                        st.chat_message("user").write(user_msg)
                        st.chat_message("assistant").write(ai_msg)
                        if translation:
                            st.caption(f"*Translation: {translation}*")
                    with cols[1]:
                        if st.button("🔊", key=f"voice_{i}"):
                            try:
                                combined_text = f"You asked: {user_msg}.\nAI says: {ai_msg}"
                                chatbot.speak_text(combined_text, st.session_state.selected_language)
                            except Exception as e:
                                pass
                i += 2
            else:
                # In case of orphaned assistant message
                st.chat_message(messages[i]["role"]).write(messages[i]["content"])
                i += 1
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
    # Voice output: group user question and AI response
    if st.session_state.voice_enabled:
        try:
            combined_text = f"You asked: {user_input}.\nAI says: {response}"
            chatbot.speak_text(combined_text, st.session_state.selected_language)
        except Exception as e:
            pass  # Silently handle voice errors

def quiz_interface():
    st.markdown(f"### 🧠 {t('quiz_time')}")
    load_section_lottie(QUIZ_LOTTIE_URL)
    if not st.session_state.quiz_started:
        show_quiz_menu()
    else:
        show_quiz_questions()

def show_quiz_menu():
    st.markdown(f"### 🧠 {t('test_knowledge')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subjects = quiz_module.get_subjects_for_class(st.session_state.selected_class)
        selected_subject = st.selectbox(t('choose_subject'), subjects)
        st.session_state.quiz_subject = selected_subject
    with col2:
        num_questions = st.slider(t('num_questions'), 1, 10, 5)
    
    if st.button(f"🚀 {t('start_quiz')}", type="primary", use_container_width=True):
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
    subject = st.session_state.quiz_subject
    language = st.session_state.selected_language
    lang_code = get_language_code(language)
    # Detect language change and rerun to update translation
    if 'last_quiz_language' not in st.session_state:
        st.session_state['last_quiz_language'] = language
    if st.session_state['last_quiz_language'] != language:
        st.session_state['last_quiz_language'] = language
        st.rerun()
    if current_idx >= len(questions):
        show_quiz_results()
        return
    
    question = questions[current_idx]
    # On-the-fly translation for current question if language changed
    if subject.lower() in ['english', 'hindi', 'telugu']:
        display_question = question.get('question_en', question.get('question', ''))
        display_options = question.get('options', [])
        display_explanation = question.get('explanation_en', question.get('explanation', ''))
        display_correct = question.get('correct_answer_en', question.get('correct_answer', ''))
    elif lang_code == 'en':
        # Prefer English version if available
        display_question = question.get('question_en', question.get('question', ''))
        display_options = [opt.get('option_en', opt) if isinstance(opt, dict) else opt for opt in question.get('options', [])]
        display_explanation = question.get('explanation_en', question.get('explanation', ''))
        display_correct = question.get('correct_answer_en', question.get('correct_answer', ''))
        # If not available, translate from current text
        if not display_question or display_question == question.get('question', ''):
            display_question = quiz_module.translate_text(question.get('question', ''), 'en')
        if not display_options or display_options == question.get('options', []):
            display_options = [quiz_module.translate_text(opt, 'en') for opt in question.get('options', [])]
        if not display_explanation or display_explanation == question.get('explanation', ''):
            display_explanation = quiz_module.translate_text(question.get('explanation', ''), 'en')
        try:
            idx = question.get('options', []).index(question.get('correct_answer', ''))
            display_correct = display_options[idx] if idx < len(display_options) else display_options[0]
        except Exception:
            display_correct = question.get('correct_answer', '')
    else:
        display_question = quiz_module.translate_text(question['question'], lang_code)
        display_options = [quiz_module.translate_text(opt, lang_code) for opt in question['options']]
        display_explanation = quiz_module.translate_text(question.get('explanation', ''), lang_code)
        try:
            idx = question['options'].index(question['correct_answer'])
            display_correct = display_options[idx] if idx < len(display_options) else display_options[0]
        except Exception:
            display_correct = question['correct_answer']
    # Progress bar
    progress = (current_idx + 1) / len(questions)
    st.progress(progress)
    st.markdown(f"**Question {current_idx + 1} of {len(questions)}**")
    # Question
    st.markdown(f"### {display_question}")
    # Voice output for question
    if st.session_state.voice_enabled and st.button("🔊 Read Question", key=f"read_q_{current_idx}"):
        try:
            chatbot.speak_text(display_question, language)
        except:
            pass
    # Options
    selected_option = st.radio(t('choose_subject'), display_options, key=f"q_{current_idx}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('submit_answer'), type="primary", use_container_width=True):
            # Check answer
            is_correct = selected_option == display_correct
            if is_correct:
                st.session_state.quiz_score += 1
                st.success(f"✅ {t('correct')}")
            else:
                st.error(f"❌ {t('incorrect')} {t('correct_answer')}: {display_correct}")
                if display_explanation:
                    st.info(f"{t('detailed_results')}: {display_explanation}")
            st.session_state.quiz_answers.append({
                'question': display_question,
                'selected': selected_option,
                'correct': display_correct,
                'is_correct': is_correct
            })
            # Voice output for quiz feedback
            if st.session_state.voice_enabled:
                feedback_text = t('correct') if is_correct else f"{t('incorrect')} {t('correct_answer')}: {display_correct}"
                try:
                    chatbot.speak_text(feedback_text, language)
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
        if st.button(f"🚪 {t('exit_quiz')}", type="secondary", use_container_width=True):
            attempted = len(st.session_state.quiz_answers)
            total_questions = len(st.session_state.quiz_questions)
            correct_answers = sum(1 for ans in st.session_state.quiz_answers if ans['is_correct'])
            # Score is based on total questions, not just attempted
            current_score = (correct_answers / total_questions * 100) if total_questions else 0
            # Save to quiz history
            quiz_entry = {
                'username': st.session_state.username,
                'name': st.session_state.name,
                'date': str(datetime.now().date()),
                'subject': st.session_state.get('quiz_subject', 'Unknown'),
                'score': current_score,
                'status': t('incomplete'),
                'questions_attempted': attempted,
                'questions_total': total_questions
            }
            append_quiz_history(quiz_entry)
            # Reset quiz state
            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_current = 0
            st.session_state.quiz_answers = []
            st.warning(f"{t('quiz_exited')} {current_score:.1f}% ({correct_answers}/{attempted} {t('questions_attempted')}, {t('questions_total')}: {total_questions})")
            st.info(t('note_unattempted'))
            st.rerun()

def show_quiz_results():
    st.markdown(f"### 🎉 {t('quiz_completed')}")
    score = st.session_state.quiz_score
    total = len(st.session_state.quiz_questions)
    percentage = (score / total) * 100
    # Save to quiz history
    quiz_entry = {
        'username': st.session_state.username,
        'name': st.session_state.name,
        'date': str(datetime.now().date()),
        'subject': st.session_state.get('quiz_subject', 'Unknown'),
        'score': percentage,
        'status': 'Completed',
        'questions_attempted': total
    }
    append_quiz_history(quiz_entry)
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
        st.metric(t('score'), f"{score}/{total}")
    with col2:
        st.metric(t('percentage'), f"{percentage:.1f}%")
    with col3:
        if percentage >= 80:
            st.success(f"🌟 {t('excellent')}")
        elif percentage >= 60:
            st.info(f"👍 {t('good_job')}")
        else:
            st.warning(f"📚 {t('keep_studying')}")
    # Detailed results
    with st.expander(f"📊 {t('detailed_results')}"):
        for i, answer in enumerate(st.session_state.quiz_answers):
            if answer['is_correct']:
                st.success(f"Q{i+1}: ✅ {answer['question'][:50]}...")
            else:
                st.error(f"Q{i+1}: ❌ {answer['question'][:50]}...")
                st.caption(f"{t('your_answer')}: {answer['selected']}")
                st.caption(f"{t('correct_answer')}: {answer['correct']}")
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
    st.markdown(f"### 📖 {t('study_materials')}")
    load_section_lottie(STUDY_LOTTIE_URL)
    materials = study_materials.get_materials_for_class(st.session_state.selected_class)
    if not materials:
        st.info(t('study_materials_preparing'))
        return
    video_channel_names = {
        'https://www.youtube.com/@t.srinivasacharychary7675/videos': t('tutor_srinivasa_chary'),
        'https://www.youtube.com/user/khanacademy': t('khan_academy'),
        'https://www.youtube.com/c/LearnCBSE': t('learn_cbse'),
        'https://www.youtube.com/c/MathAntics': t('math_antics'),
        'https://www.youtube.com/c/CrashCourse': t('crash_course'),
        'https://www.youtube.com/c/AmoebaSisters': t('amoeba_sisters'),
        'https://www.youtube.com/c/BritishCouncilLEARNENGLISH': t('british_council'),
        'https://www.youtube.com/c/EnglishAddictwithMrDuncan': t('mr_duncan'),
        'https://www.youtube.com/c/HindiVyakaran': t('hindi_vyakaran'),
        'https://www.youtube.com/c/ExamपुरHindi': t('exampur_hindi'),
        'https://www.youtube.com/c/LearnTeluguwithKaushik': t('kaushik_telugu'),
        'https://www.youtube.com/c/TeluguBadi': t('telugu_badi'),
        'https://www.youtube.com/c/Unacademy': t('unacademy'),
    }
    for subject, content in materials.items():
        with st.expander(f"📚 {subject}"):
            st.markdown(t(content['description']))
            if content.get('sample_pdf'):
                try:
                    pdf_data = study_materials.generate_sample_pdf(subject, st.session_state.selected_class)
                    st.download_button(
                        label=f" {t('download_notes').format(subject=subject)}",
                        data=pdf_data,
                        file_name=f"{subject}_Class_{st.session_state.selected_class}_Notes.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.warning(t('pdf_unavailable').format(subject=subject))
            study_materials.show_materials_message()
            if content.get('resources'):
                st.markdown(f"**{t('additional_resources')}**")
                for resource in content['resources']:
                    if resource.startswith('http') or resource.startswith('www.'):
                        st.markdown(f"• {resource}")
                    else:
                        st.markdown(f"• {t(resource)}")
            if content.get('videos'):
                st.markdown(f"**{t('video_explanations')}**")
                for video in content['videos']:
                    channel = video_channel_names.get(video, None)
                    if channel:
                        st.markdown(f"- **{channel}** [Watch on YouTube]({video})")
                    else:
                        st.markdown(f"- [Watch on YouTube]({video})")

def analytics_interface():
    """Student analytics and progress dashboard"""
    st.markdown(f"### 📊 {t('analytics')}")
    st.markdown(f"#### {t('student_progress_dashboard')}")
    st.markdown(f"#### {t('your_badges')}")
    st.markdown(f"#### {t('average_score_per_subject')}")
    st.markdown(f"#### {t('quiz_scores_over_time')}")
    st.markdown(f"#### {t('quiz_completion_status')}")
    st.markdown(f"#### {t('recent_quiz_history')}")
    st.markdown(f"#### {t('review_past_quizzes')}")
    load_section_lottie(ANALYTICS_LOTTIE_URL)
    quiz_history = [h for h in load_quiz_history() if h.get('username') == st.session_state.username]
    if not quiz_history:
        st.info(t('no_quiz_history'))
        return
    df = pd.DataFrame(quiz_history)
    # Gamification: Badges
    badge_map = {
        'first_quiz': t('badge_first_quiz'),
        'scored_80': t('badge_scored_80'),
        'five_quizzes': t('badge_five_quizzes'),
        'improved': t('badge_improved'),
    }
    badges = []
    if len(df) > 0:
        badges.append(badge_map['first_quiz'])
    if (df['score'] >= 80).any():
        badges.append(badge_map['scored_80'])
    if len(df) >= 5:
        badges.append(badge_map['five_quizzes'])
    if len(df) >= 2 and df['score'].iloc[-1] > df['score'].iloc[0]:
        badges.append(badge_map['improved'])
    if badges:
        st.markdown(f"#### 🏆 {t('your_badges')}")
        st.markdown(" ".join(badges))
    # Bar chart: average score per subject
    st.markdown(f"#### {t('average_score_per_subject')}")
    if 'subject' in df and 'score' in df:
        subject_scores = df.groupby('subject')['score'].mean()
        st.bar_chart(subject_scores)
    # Line chart: quiz scores over time
    st.markdown(f"#### {t('quiz_scores_over_time')}")
    if 'date' in df and 'score' in df:
        df_sorted = df.sort_values('date')
        st.line_chart(df_sorted.set_index('date')['score'])
    # Pie chart: completion status
    st.markdown(f"#### {t('quiz_completion_status')}")
    if 'status' in df:
        status_counts = Counter(df['status'])
        status_labels = [t(str(label), 'en') for label in status_counts.keys()]  # Always English
        fig, ax = plt.subplots(figsize=(7, 5))
        num_slices = len(status_labels)
        def autopct_format(pct):
            return '%1.1f%%' % pct if pct > 5 else ''
        wedges, texts, autotexts = ax.pie(
            status_counts.values(),
            labels=status_labels,
            autopct=autopct_format,
            startangle=90,
            pctdistance=1.35,
            labeldistance=1.2,
            wedgeprops=dict(width=0.7, edgecolor='w')
        )
        for i, autotext in enumerate(autotexts):
            autotext.set_fontsize(9)
            if num_slices > 2 and i > 0:
                x, y = autotext.get_position()
                autotext.set_position((x, y - 0.05 * i))
        ax.axis('equal')
        ax.legend(wedges, status_labels, title='Status', loc='center left', bbox_to_anchor=(1, 0.5))
        st.pyplot(fig)
    st.markdown("---")
    # Recent quiz history table
    st.markdown(f"### 📈 {t('recent_quiz_history')}")
    st.dataframe(df, use_container_width=True)
    # Review Past Quizzes section
    st.markdown("---")
    st.markdown(f"### 📝 {t('review_past_quizzes')}")
    for i, quiz in enumerate(reversed(quiz_history)):
        with st.expander(f"{quiz['date']} | {quiz['subject']} | {quiz['score']:.1f}% | {translate_status(quiz['status'])}"):
            st.write(f"**{t('date')}:** {quiz['date']}")
            st.write(f"**{t('subject')}:** {quiz['subject']}")
            st.write(f"**{t('score')}:** {quiz['score']:.1f}%")
            st.write(f"**{t('status')}:** {translate_status(quiz['status'])}")
            st.write(f"**{t('questions_attempted')}:** {quiz.get('questions_attempted', '-')}")
            st.write(f"**{t('questions_total')}:** {quiz.get('questions_total', quiz.get('questions_attempted', '-'))}")
            # If detailed answers are available, show them (future enhancement)
            # Retake Quiz button
            if st.button(f"{t('retake_quiz')} {quiz['subject']}", key=f"retake_{i}"):
                st.session_state.quiz_subject = quiz['subject']
                st.session_state.quiz_started = False
                st.session_state.main_section = 'quiz'
                st.rerun()

def about_us_interface():
    """About Us section"""
    st.markdown(f"### ℹ️ {t('about_us')}")
    lang = st.session_state.get('selected_language', 'en')
    if lang == 'ta':
        about_lines = [
            'about_us_intro',
            'about_what_we_offer',
            'about_for_students',
            'about_students_ai_chat',
            'about_students_quizzes',
            'about_students_materials',
            'about_students_multilang',
            'about_students_voice',
            'about_students_analytics',
            'about_for_teachers',
            'about_teachers_quiz',
            'about_teachers_monitor',
            'about_teachers_upload',
            'about_teachers_analytics',
            'about_for_admins',
            'about_admins_user_mgmt',
            'about_admins_analytics',
            'about_admins_tools',
            'about_vision',
            'about_vision_text',
            'about_key_features',
            'about_multilingual',
            'about_ai_powered',
            'about_comprehensive',
            'about_voice_enabled',
            'about_progress_tracking',
            'about_secure_safe',
            'about_acknowledgments',
            'about_acknowledgments_text',
        ]
        st.markdown('\n\n'.join([safe_translate(line) for line in about_lines]))
    else:
        about_lines = [
            "Vidya Sakhi is an innovative educational platform designed specifically for Indian school students from Classes 3-12. Our mission is to make learning engaging, accessible, and fun for every student.",
            "🎯 What We Offer",
            "For Students:",
            "🤖 AI-powered chat assistance for all subjects",
            "🧠 Interactive quizzes with instant feedback",
            "📚 Comprehensive study materials",
            "🗣️ Multi-language support including Hindi, Telugu, and regional languages",
            "🔊 Voice assistance for better learning",
            "📊 Personal progress tracking and analytics",
            "For Teachers:",
            "🤖 Easy quiz question management",
            "📋 Student progress monitoring",
            "📁 Study material upload and organization",
            "📊 Class performance analytics",
            "For Administrators:",
            "👥 User management system",
            "📈 System-wide analytics",
            "🔧 Platform administration tools",
            "🌍 Our Vision",
            "To democratize quality education by providing every Indian student with a personalized AI tutor that understands their language, culture, and learning needs.",
            "🏆 Key Features",
            "Multi-lingual Support: Learn in your preferred language",
            "AI-Powered: Intelligent responses powered by advanced AI",
            "Comprehensive Content: Covers all major subjects and classes",
            "Voice Enabled: Audio support for better accessibility",
            "Progress Tracking: Monitor your learning journey",
            "Secure & Safe: Protected user data and safe learning environment",
            "🙏 Acknowledgments",
            "Vidya Sakhi is built with love for Indian students, incorporating the best of modern technology with traditional educational values."
        ]
        st.markdown('\n\n'.join([safe_translate(line) for line in about_lines]))

def contact_interface():
    """Contact section"""
    st.markdown(f"### {t('contact')}")
    lang = st.session_state.get('selected_language', 'en')
    if lang == 'ta':
        contact_lines = [
            'contact_intro',
            'contact_info',
            'email',
            'phone',
            'address',
            'support_hours',
            'support_hours_mf',
            'support_hours_sat',
            'support_hours_sun',
            'quick_contact_form',
            'your_name',
            'email_address',
            'phone_number',
            'subject',
            'general_inquiry',
            'message',
            'describe_query',
            'connect_with_us',
            'resources',
            'user_guide',
            'faqs',
            'video_tutorials',
            'emergency_support',
            'emergency_phone',
        ]
        st.markdown('\n\n'.join([safe_translate(line) for line in contact_lines]))
    else:
        contact_lines = [
            "We'd love to hear from you! Whether you have questions, suggestions, or need support, our team is here to help.",
            "\n📧 Contact Information",
            "Email: sathviktad@gmail.com",
            "Phone: +91-6281868523",
            "Address: Plot no-21, 3-5-71/1, Gayathri Nilayam, Road no-4C, Krishna Nagar Colony, Moula-ali, Hyderabad, Telangana, India-500040",
            "\n🕒 Support Hours",
            "Monday - Friday: 9:00 AM - 6:00 PM",
            "Saturday: 10:00 AM - 4:00 PM",
            "Sunday: Closed",
            "\n💬 Quick Contact Form",
            "Your Name*",
            "Email Address*",
            "Phone Number",
            "Subject",
            "General Inquiry",
            "Message*",
            "Please describe your query or feedback...",
            "\n🤝 Connect With Us",
            "[GitHub](https://github.com/sathviktad)",
            "[LinkedIn](https://www.linkedin.com/in/sathvik-tadimeti/)",
            "[Instagram](https://www.instagram.com/_sathviktad/?hl=en)",
            "\n📚 Resources",
            "[User Guide](https://github.com/sathviktad/vidya-sakhi#readme)",
            "[FAQs](https://github.com/sathviktad/vidya-sakhi/blob/main/FAQ.md)",
            "[Video Tutorials](https://www.youtube.com/results?search_query=ai+companion+applications+demo)",
            "\n🆘 Emergency Support",
            "For urgent technical issues during school hours, please contact our emergency support line: Emergency Phone: +91-9704002277"
        ]
        st.markdown('\n\n'.join([safe_translate(line) for line in contact_lines]))

def help_faq_interface():
    st.markdown(f"### ❓ {t('help_faq')}")
    lang = st.session_state.get('selected_language', 'en')
    if lang == 'ta':
        faq_lines = [
            'faq_intro',
            'faq_q1', 'faq_a1',
            'faq_q2', 'faq_a2',
            'faq_q3', 'faq_a3',
            'faq_q4', 'faq_a4',
            'faq_q5', 'faq_a5',
            'faq_q6', 'faq_a6',
            'faq_q7', 'faq_a7',
            'faq_q8', 'faq_a8',
            'faq_q9', 'faq_a9',
            'faq_q10', 'faq_a10',
            'faq_q11', 'faq_a11',
        ]
        st.markdown('\n\n'.join([safe_translate(line) for line in faq_lines]))
    else:
        faq_lines = [
            "Welcome to Vidya Sakhi's Help & FAQ!",
            "Q: How do I take a quiz?",
            "A: Go to '🧠 Quiz Time', select your subject and number of questions, and click 'Start Quiz'.",
            "Q: How do I review my past quizzes?",
            "A: Go to '📊 Analytics' and scroll to 'Review Past Quizzes'.",
            "Q: How do I download my analytics?",
            "A: Teachers can download analytics as CSV from the analytics dashboard.",
            "Q: How do I enable accessibility features?",
            "A: Use the '♿ Accessibility' toggles in the sidebar for large font or dyslexia-friendly font.",
            "Q: How do I contact support?",
            "A: Click the button below to open the contact form.",
            "Q: I forgot my password. How can I reset it?",
            "A: Please contact your teacher or the admin to reset your password. Self-service password reset is coming soon!",
            "Q: How do I report a bug or suggest a feature?",
            "A: Use the contact form or email us at sathviktad@gmail.com with details.",
            "Q: Is my data private and secure?",
            "A: Yes! Your quiz history and personal data are stored securely and are only visible to you and your teachers.",
            "Q: What is the leaderboard and how does it work?",
            "A: The leaderboard (teacher dashboard) shows top students by average quiz score. It encourages healthy competition!",
            "Q: Can I use Vidya Sakhi on my phone or tablet?",
            "A: Yes! Vidya Sakhi works on any device with a web browser, including phones and tablets.",
            "Q: How do I use text-to-speech or voice features?",
            "A: Enable '🔊 Voice Output' in the sidebar. For quizzes and study materials, this feature is coming soon."
        ]
        st.markdown('\n\n'.join([safe_translate(line) for line in faq_lines]))
    lottie_data = load_lottie_url(HELP_LOTTIE_URL)
    if lottie_data:
        st_lottie(lottie_data, height=120, key="help_lottie")
    else:
        st.info(t('faq_intro') if lang == 'ta' else "Welcome to Vidya Sakhi's Help & FAQ!")
    if st.button(t('contact_support'), use_container_width=True):
        if st.session_state.user_role == "student":
            st.session_state.main_section = 'contact'
            st.rerun()
        else:
            st.session_state.show_inline_contact = True
    if st.session_state.get("show_inline_contact") and st.session_state.user_role != "student":
        contact_interface()
        st.session_state.show_inline_contact = False

def load_section_lottie(url):
    data = load_lottie_url(url)
    if data:
        st_lottie(data, height=120)

def app_footer():
    st.markdown('<div style="text-align:center; color:gray; font-size:0.9rem; margin-top:2rem;">© 2024 Vidya Sakhi. All rights reserved.<br><span style="font-size:0.8rem; color:#888;">Version 1.0</span></div>', unsafe_allow_html=True)

def autopct_format_factory(num_slices):
    # Returns a function that spaces out small slice labels vertically
    def autopct_format(pct):
        return '%1.1f%%' % pct
    return autopct_format

if __name__ == "__main__":
    main()
