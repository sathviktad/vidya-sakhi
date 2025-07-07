import streamlit as st
import json
import re
import os
from translatepy import Translate
from googletrans import Translator

TRANSLATEPY = Translate()
GOOGLETRANS = Translator()

def get_language_options():
    """Return supported languages with their codes"""
    return {
        'English': 'en',
        'Hindi': 'hi',
        'Telugu': 'te',
        'Tamil': 'ta',
        'Malayalam': 'ml',
        'Kannada': 'kn',
        'Bengali': 'bn',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Punjabi': 'pa',
        'Urdu': 'ur'
    }

def get_language_code(language_name):
    """Get language code for a given language name"""
    languages = get_language_options()
    return languages.get(language_name, 'unknown')

def apply_theme(theme_name="theme1"):
    if theme_name == "theme1":
        st.markdown(
            """
        <style>
            body, .stApp {
                background: linear-gradient(135deg, #f8fafc 0%, #e8f5e9 100%) !important;
                font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        }
            .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button {
                background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%) !important;
                color: #fff !important;
                border: none !important;
                border-radius: 1.5rem !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 8px rgba(67,233,123,0.08);
                transition: background 0.3s;
        }
            .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover {
                background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
                background: #e8f5e9 !important;
                border-radius: 1.5rem 1.5rem 0 0 !important;
                box-shadow: 0 2px 8px rgba(67,233,123,0.08);
        }
        .stTabs [data-baseweb="tab"] {
                font-weight: 600 !important;
                color: #388e3c !important;
                border-radius: 1.5rem 1.5rem 0 0 !important;
        }
        .stTabs [aria-selected="true"] {
                background: #43e97b22 !important;
                color: #1b5e20 !important;
        }
            .stSidebar {
                background: linear-gradient(135deg, #e8f5e9 0%, #f8fafc 100%) !important;
                border-radius: 0 2rem 2rem 0 !important;
        }
            .stMetric {
                background: #e8f5e9 !important;
                border-radius: 1rem !important;
                padding: 1rem !important;
                color: #1b5e20 !important;
        }
            .stExpander, .stDataFrame, .stTable {
                border-radius: 1rem !important;
                background: #f8fafc !important;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #1b5e20 !important;
                font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
            }
            /* In dark mode, set only label and heading text color to white for readability */
            body[data-theme="dark"] label,
            body[data-theme="dark"] h1,
            body[data-theme="dark"] h2,
            body[data-theme="dark"] h3,
            body[data-theme="dark"] h4,
            body[data-theme="dark"] h5,
            body[data-theme="dark"] h6,
            body[data-theme="dark"] .stMarkdown,
            body[data-theme="dark"] .stText,
            body[data-theme="dark"] .stRadio > label,
            body[data-theme="dark"] .stSelectbox > label,
            body[data-theme="dark"] .stSidebar,
            body[data-theme="dark"] .stSidebar .css-1v0mbdj,
            body[data-theme="dark"] .stSidebar .css-1v3fvcr,
            body[data-theme="dark"] .stSidebar .css-1c7y2kd,
            body[data-theme="dark"] .stSidebar .css-1offfwp,
            body[data-theme="dark"] .stSidebar .css-1lcbmhc,
            body[data-theme="dark"] .stMarkdown.quiz-label,
            body[data-theme="dark"] .stMarkdown.quiz-header,
            body[data-theme="dark"] .stMarkdown.voice-output,
            body[data-theme="dark"] .stMarkdown.sidebar-menu-label {
                color: #fff !important;
        }
        </style>
            """,
            unsafe_allow_html=True
        )
    elif theme_name == "theme2":
        st.markdown(
            """
        <style>
            body, .stApp {
                background: linear-gradient(135deg, #232526 0%, #414345 100%) !important;
                font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
                color: #e0e0e0 !important;
        }
            .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button {
                background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
                color: #fff !important;
                border: none !important;
                border-radius: 1.5rem !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 8px rgba(56,239,125,0.08);
                transition: background 0.3s;
        }
            .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover {
                background: linear-gradient(90deg, #38ef7d 0%, #11998e 100%) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
                background: #232526 !important;
                border-radius: 1.5rem 1.5rem 0 0 !important;
                box-shadow: 0 2px 8px rgba(56,239,125,0.08);
        }
        .stTabs [data-baseweb="tab"] {
                font-weight: 600 !important;
                color: #38ef7d !important;
                border-radius: 1.5rem 1.5rem 0 0 !important;
        }
        .stTabs [aria-selected="true"] {
                background: #11998e33 !important;
                color: #fff !important;
            }
            .stSidebar, .stSidebarContent {
                background: linear-gradient(135deg, #232526 0%, #414345 100%) !important;
                border-radius: 0 2rem 2rem 0 !important;
                color: #e0e0e0 !important;
        }
            .stSidebar label {
                color: #e0e0e0 !important;
            }
            .stMetric {
                background: #232526 !important;
                border-radius: 1rem !important;
                padding: 1rem !important;
                color: #38ef7d !important;
            }
            .stExpander, .stDataFrame, .stTable {
                border-radius: 1rem !important;
                background: #232526 !important;
                color: #e0e0e0 !important;
        }
            .stChatMessage, .element-container:has(.stChatMessage) {
                background: #2d2f31 !important;
                color: #fff !important;
                border-radius: 1rem !important;
                padding: 0.5rem 1rem !important;
            }
            .stChatMessage .stMarkdown, .stChatMessage .stMarkdown p {
                color: #fff !important;
        }
            /* Quiz section styles */
            .stMarkdown.quiz-question, .stMarkdown.quiz-option, .stMarkdown.quiz-feedback, .stMarkdown.quiz-score, .stMarkdown.quiz-header {
                color: #fff !important;
                background: #232526 !important;
                border-radius: 0.75rem !important;
                padding: 0.5rem 1rem !important;
            }
            .stMarkdown.quiz-option {
                color: #38ef7d !important;
            }
            .stMarkdown.quiz-feedback {
                color: #ffd600 !important;
            }
            .stMarkdown.quiz-score {
                color: #00e676 !important;
            }
            .stMarkdown.quiz-header {
                color: #38ef7d !important;
                font-weight: 700 !important;
        }
        </style>
            """,
            unsafe_allow_html=True
        )

def get_lottie_url():
    """Return Lottie animation URL for Vidya Sakhi"""
    return "https://lottie.host/4f3c9b6d-f29e-4c14-8b4f-7d6c8e9f2a3b/KLTBGgX6pl.json"

def get_avatar_svg():
    """Return simple avatar for fallback"""
    return """
    <div style="text-align: center; margin: 2rem 0;">
        <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 48px;">
            🎓
        </div>
        <h4 style="color: #4CAF50; margin-top: 1rem;">Hi! I'm Vidya Sakhi 👋</h4>
        <p style="color: #666; font-size: 0.9rem;">Your friendly AI learning companion</p>
    </div>
    """

# Hardcoded subject lists as per get_subjects_for_class
HARDCODED_SUBJECTS = {
    3: ['Math', 'Science', 'English', 'Hindi', 'GK', 'Computers', 'Sports', 'Value Education', 'Telugu'],
    4: ['Math', 'Science', 'English', 'Hindi', 'GK', 'Computers', 'Sports', 'Value Education', 'Telugu'],
    5: ['Math', 'Science', 'English', 'Hindi', 'GK', 'Computers', 'Sports', 'Value Education', 'Telugu'],
    6: ['Math', 'Science', 'English', 'Social', 'Hindi', 'Telugu', 'GK', 'Computers'],
    7: ['Math', 'Science', 'English', 'Social', 'Hindi', 'Telugu', 'GK', 'Computers'],
    8: ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics'],
    9: ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics'],
    10: ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics'],
    11: ['Physics', 'Chemistry', 'Math', 'Biology', 'English'],
    12: ['Physics', 'Chemistry', 'Math', 'Biology', 'English'],
}

def ensure_minimum_questions(filename="quiz_questions.json", min_questions=30):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for class_num in range(3, 13):
        class_key = f"class_{class_num}"
        if class_key not in data:
            data[class_key] = {}
        subjects = HARDCODED_SUBJECTS.get(class_num, [])
        for subject in subjects:
            if subject not in data[class_key]:
                data[class_key][subject] = []
            qlist = data[class_key][subject]
            # Add placeholders if less than min_questions
            for i in range(len(qlist), min_questions):
                qlist.append({
                    "question": f"{subject} Placeholder Question {i+1} for Class {class_num}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A"
                })

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Ensured at least {min_questions} questions for every class/subject combination.")

def remove_placeholder_questions(filename="quiz_questions.json", min_questions=10):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    placeholder_patterns = [
        re.compile(r"Placeholder", re.IGNORECASE),
        re.compile(r"Question \\d+ for Class \\d+", re.IGNORECASE),
        re.compile(r"level \\d+", re.IGNORECASE)
    ]

    def is_full_option_placeholder(q):
        return (
            q["options"] == ["Option A", "Option B", "Option C", "Option D"]
            and q["correct_answer"] == "Option A"
        )

    summary = []
    for class_key, class_data in data.items():
        for subject, questions in class_data.items():
            # Remove placeholders
            real_questions = [
                q for q in questions
                if not any(pat.search(q["question"]) for pat in placeholder_patterns)
                and not is_full_option_placeholder(q)
            ]
            data[class_key][subject] = real_questions
            if len(real_questions) < min_questions:
                summary.append(f"{class_key} - {subject}: {len(real_questions)} real questions left")

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Removed all placeholder questions.")
    if summary:
        print("\nClass/Subject combinations with fewer than 10 real questions:")
        for line in summary:
            print(line)
    else:
        print("All combinations have at least 10 real questions.")

def ensure_unique_real_questions(filename="quiz_questions.json", min_questions=30):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    placeholder_patterns = [
        re.compile(r"Placeholder", re.IGNORECASE),
        re.compile(r"Question \\d+ for Class \\d+", re.IGNORECASE),
        re.compile(r"level \\d+", re.IGNORECASE)
    ]

    summary = []
    template_needed = []
    for class_key, class_data in data.items():
        for subject, questions in class_data.items():
            # Remove placeholders and duplicates
            real_questions = [q for q in questions if not any(pat.search(q["question"]) for pat in placeholder_patterns)]
            seen = set()
            unique_questions = []
            for q in real_questions:
                q_text = q["question"].strip().lower()
                if q_text not in seen:
                    seen.add(q_text)
                    unique_questions.append(q)
            data[class_key][subject] = unique_questions
            if len(unique_questions) < min_questions:
                summary.append(f"{class_key} - {subject}: {len(unique_questions)} real unique questions left")
                template_needed.append((class_key, subject, min_questions - len(unique_questions)))

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Ensured only real, unique questions for each class/subject.")
    if summary:
        print("\nClass/Subject combinations with fewer than 30 real unique questions:")
        for line in summary:
            print(line)
        print("\nTEMPLATE for adding more questions:")
        for class_key, subject, num_needed in template_needed:
            print(f"\nAdd {num_needed} more questions to {class_key} - {subject}:")
            for i in range(num_needed):
                print(f"  {{\n    'question': 'Your question here',\n    'options': ['A', 'B', 'C', 'D'],\n    'correct_answer': 'A'\n  }}")
    else:
        print("All combinations have at least 30 real unique questions.")

def reset_and_populate_with_real_questions(filename="quiz_questions.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    placeholder_patterns = [
        re.compile(r"Placeholder", re.IGNORECASE),
        re.compile(r"Question \\d+ for Class \\d+", re.IGNORECASE),
        re.compile(r"level \\d+", re.IGNORECASE)
    ]
    def is_full_option_placeholder(q):
        return (
            q["options"] == ["Option A", "Option B", "Option C", "Option D"]
            and q["correct_answer"] == "Option A"
        )

    new_data = {}
    for class_key, class_data in data.items():
        new_data[class_key] = {}
        for subject, questions in class_data.items():
            # Remove placeholders and duplicates
            real_questions = [
                q for q in questions
                if not any(pat.search(q["question"]) for pat in placeholder_patterns)
                and not is_full_option_placeholder(q)
            ]
            seen = set()
            unique_questions = []
            for q in real_questions:
                q_text = q["question"].strip().lower()
                if q_text not in seen:
                    seen.add(q_text)
                    unique_questions.append(q)
            if unique_questions:
                new_data[class_key][subject] = unique_questions
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print("Reset and repopulated quiz_questions.json with all available real, unique questions.")

def classify_question_difficulty(question_text):
    # Simple heuristics for demonstration
    text = question_text.lower()
    if 'competitive' in text or 'jee' in text or 'neet' in text or 'olympiad' in text:
        return 'competitive'
    if 'board' in text:
        return 'board'
    if re.search(r'level \d+', text):
        level = int(re.search(r'level (\d+)', text).group(1))
        if level <= 3:
            return 'easy'
        elif level <= 7:
            return 'medium'
        elif level <= 12:
            return 'hard'
        else:
            return 'competitive'
    # Math/Science: use numbers and terms
    if any(word in text for word in ['add', 'plus', 'sum', 'subtract', 'minus', 'difference', 'multiply', 'divide', 'times', 'product', 'quotient', 'basic', 'simple', 'triangle', 'square', 'circle', 'count', 'how many']):
        return 'easy'
    if any(word in text for word in ['atom', 'molecule', 'photosynthesis', 'gravity', 'force', 'energy', 'planet', 'organ', 'digest', 'respiration', 'evaporation', 'condensation', 'fraction', 'decimal', 'percent', 'average', 'mean', 'median', 'geometry', 'algebra', 'equation', 'expression', 'prime', 'composite', 'perimeter', 'area', 'volume']):
        return 'medium'
    if any(word in text for word in ['derivative', 'integral', 'vector', 'matrix', 'theorem', 'proof', 'calculus', 'trigonometry', 'logarithm', 'stoichiometry', 'valency', 'oxidation', 'reduction', 'circuit', 'current', 'voltage', 'resistance', 'magnetic', 'inertia', 'momentum', 'kinetic', 'potential', 'enzyme', 'genetics', 'chromosome', 'mitosis', 'meiosis', 'ecosystem', 'biodiversity']):
        return 'hard'
    # If question is long or has complex words
    if len(text.split()) > 18 or any(len(word) > 12 for word in text.split()):
        return 'hard'
    # Default
    return 'medium'

def redistribute_questions_by_difficulty(filename="quiz_questions.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Collect all questions by subject and difficulty
    subject_difficulty_questions = {}
    for class_key, class_data in data.items():
        for subject, questions in class_data.items():
            if subject not in subject_difficulty_questions:
                subject_difficulty_questions[subject] = {'easy': [], 'medium': [], 'hard': [], 'board': [], 'competitive': []}
            for q in questions:
                diff = classify_question_difficulty(q['question'])
                subject_difficulty_questions[subject][diff].append(q)

    # Define class to difficulty mapping
    class_difficulty_map = {
        3: ['easy'],
        4: ['easy', 'medium'],
        5: ['easy', 'medium'],
        6: ['easy', 'medium', 'hard'],
        7: ['medium', 'hard'],
        8: ['medium', 'hard'],
        9: ['board', 'hard', 'medium'],
        10: ['board', 'hard', 'medium'],
        11: ['competitive', 'hard', 'board'],
        12: ['competitive', 'hard', 'board']
    }

    new_data = {}
    for class_num in range(3, 13):
        class_key = f'class_{class_num}'
        new_data[class_key] = {}
        for subject, diff_dict in subject_difficulty_questions.items():
            selected = []
            for diff in class_difficulty_map[class_num]:
                selected.extend(diff_dict[diff])
            # Remove duplicates by question text
            seen = set()
            unique_selected = []
            for q in selected:
                q_text = q['question'].strip().lower()
                if q_text not in seen:
                    seen.add(q_text)
                    unique_selected.append(q)
            if unique_selected:
                new_data[class_key][subject] = unique_selected
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print("Questions redistributed by class and difficulty.")

QUIZ_HISTORY_FILE = "quiz_history.json"

def load_quiz_history():
    if not os.path.exists(QUIZ_HISTORY_FILE):
        return []
    with open(QUIZ_HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_quiz_history(history):
    with open(QUIZ_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def append_quiz_history(entry):
    history = load_quiz_history()
    history.append(entry)
    save_quiz_history(history)

def reset_quiz_history(username=None):
    if username is None:
        save_quiz_history([])
    else:
        history = load_quiz_history()
        history = [h for h in history if h.get('username') != username]
        save_quiz_history(history)

# Translation dictionary for UI
TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome',
        'role': 'Role',
        'logout': 'Logout',
        'settings': 'Settings',
        'select_class': 'Select Class',
        'language': 'Speech / Language',
        'theme': 'Theme',
        'voice_output': 'Voice Output',
        'accessibility': 'Accessibility',
        'large_font': 'Large Font',
        'dyslexia_font': 'Dyslexia-Friendly Font',
        'quick_access': 'Quick Access',
        'chat_with_sakhi': 'Chat with Sakhi',
        'new_quiz': 'New Quiz',
        'study_materials': 'Study Materials',
        'main_menu': 'Main Menu',
        'test_knowledge': 'Test Your Knowledge',
        'choose_subject': 'Choose a subject:',
        'num_questions': 'Number of questions:',
        'start_quiz': 'Start Quiz',
        'quiz_time': 'Quiz Time',
        'submit_answer': 'Submit Answer',
        'exit_quiz': 'Exit Quiz',
        'try_again': 'Try Again',
        'back_to_menu': 'Back to Menu',
        'correct': 'Correct!',
        'incorrect': 'Incorrect!',
        'quiz_completed': 'Quiz Completed!',
        'score': 'Score',
        'percentage': 'Percentage',
        'excellent': 'Excellent!',
        'good_job': 'Good job!',
        'keep_studying': 'Keep studying!',
        'detailed_results': 'Detailed Results',
        'your_answer': 'Your answer',
        'correct_answer': 'Correct answer',
        'incomplete': 'Incomplete',
        'completed': 'Completed',
        'questions_attempted': 'Questions attempted',
        'questions_total': 'Total questions',
        'quiz_exited': 'Quiz exited!',
        'note_unattempted': 'Note: Unattempted questions are treated as incorrect. This quiz is marked as Incomplete in your analytics.',
        'analytics': 'Analytics',
        'about_us': 'About Us',
        'contact': 'Contact',
        'help_faq': 'Help & FAQ',
        'vidya_sakhi': 'Vidya Sakhi',
        'learning_bestie': 'Your Learning Bestie & AI Companion',
        'hi_vidya_sakhi': "Hi! I'm Vidya Sakhi 👋",
        'friendly_ai_companion': 'Your friendly AI learning companion',
        'your_badges': 'Your Badges:',
        'average_score_per_subject': 'Average Score per Subject',
        'quiz_scores_over_time': 'Quiz Scores Over Time',
        'quiz_completion_status': 'Quiz Completion Status',
        'recent_quiz_history': 'Recent Quiz History',
        'review_past_quizzes': 'Review Past Quizzes',
        'student_progress_dashboard': 'Student Progress Dashboard',
        'get_in_touch': 'Get in Touch',
        'ai_learning_companion': 'Your AI Learning Companion',
        'manage_study_materials': 'Manage Study Materials & Monitor Progress',
        'faq_intro': 'Frequently Asked Questions',
        'faq_q1': 'How do I start a quiz?',
        'faq_a1': 'Go to the Quiz section and click Start Quiz.',
        'faq_q2': 'How do I change the language?',
        'faq_a2': 'Use the language dropdown in the sidebar.',
        'faq_q3': 'How do I see my progress?',
        'faq_a3': 'Go to Analytics to see your scores and badges.',
        'faq_q4': 'Who can I contact for help?',
        'faq_a4': 'Use the Contact section to reach out.',
        'badge_first_quiz': '🏅 First Quiz Completed',
        'badge_scored_80': '🌟 Scored 80%+ on a Quiz',
        'badge_five_quizzes': '🎯 5+ Quizzes Completed',
        'badge_improved': '📈 Improved Over Time',
        'no_quiz_history': 'No quiz history available. Take some quizzes to see your progress!',
        'date': 'Date',
        'subject': 'Subject',
        'score': 'Score',
        'status': 'Status',
        'retake_quiz': 'Retake Quiz',
        'study_materials_preparing': 'Study materials for this class are being prepared. Please check back soon!',
        'download_notes': 'Download {subject} Notes',
        'pdf_unavailable': 'PDF generation temporarily unavailable for {subject}. Please try again later.',
        'additional_resources': 'Additional Resources:',
        'video_explanations': 'Video Explanations:',
        'tutor_srinivasa_chary': 'T. Srinivasa Chary (Physics)',
        'khan_academy': 'Khan Academy',
        'learn_cbse': 'LearnCBSE',
        'math_antics': 'Math Antics',
        'crash_course': 'CrashCourse',
        'amoeba_sisters': 'Amoeba Sisters',
        'british_council': 'British Council',
        'mr_duncan': 'English Addict with Mr. Duncan',
        'hindi_vyakaran': 'Hindi Vyakaran',
        'exampur_hindi': 'Examपुर Hindi',
        'kaushik_telugu': 'Learn Telugu with Kaushik',
        'telugu_badi': 'Telugu Badi',
        'unacademy': 'Unacademy',
        'scert_link_info': 'If the direct textbook link does not work, please use the SCERT eBooks portal link below it to access the latest materials.',
        'chat_with_ai_companion': 'Chat with Your AI Companion',
    },
    'hi': {
        'welcome': 'स्वागतम्',
        'role': 'भूमिका',
        'logout': 'लॉगआउट',
        'settings': 'सेटिंग्स',
        'select_class': 'कक्षा चुनें',
        'language': 'भाषा / Language',
        'theme': 'थीम',
        'voice_output': 'वायिस आउटपुट',
        'accessibility': 'उपयोग्यता',
        'large_font': 'बड़े अक्षर',
        'dyslexia_font': 'डिस्लेक्सिया-फ्रेंडली फ़ॉन्ट',
        'quick_access': 'क्विक एसेस',
        'chat_with_sakhi': 'सखितो चाट करें',
        'new_quiz': 'नया क्विज',
        'study_materials': 'अध्याय सामग्री',
        'main_menu': 'मुख्य मेनू',
        'test_knowledge': 'अपने ज्ञान का परीक्षण करें',
        'choose_subject': 'विषय चुनें:',
        'num_questions': 'प्रश्नों की संख्या:',
        'start_quiz': 'क्विज शुरू करें',
        'quiz_time': 'क्विज समय',
        'submit_answer': 'उत्तर सबमिट करें',
        'exit_quiz': 'क्विज से निर्गम करें',
        'try_again': 'फिर से प्रयास करें',
        'back_to_menu': 'मेनू पर वापस जाएं',
        'correct': 'सही है!',
        'incorrect': 'गलत है!',
        'quiz_completed': 'क्विज पूर्ण है!',
        'score': 'स्कोर',
        'percentage': 'प्रतिशत',
        'excellent': 'अद्भुत है!',
        'good_job': 'अच्छा करने के लिए बहुत अच्छा!',
        'keep_studying': 'अगले अध्याय के लिए अध्याय करें!',
        'detailed_results': 'विस्तृत परिणाम',
        'your_answer': 'आपका उत्तर',
        'correct_answer': 'सही उत्तर',
        'incomplete': 'अपूर्ण',
        'completed': 'पूर्ण',
        'questions_attempted': 'प्रयास किए गए प्रश्न',
        'questions_total': 'कुल प्रश्न',
        'quiz_exited': 'क्विज से निर्गम हुआ!',
        'note_unattempted': 'टिपणी: अप्रयास किए गए प्रश्न गलत माना जाता है। यह क्विज आपके विश्लेषण में अपूर्ण माना गया है।',
        'analytics': 'विश्लेषण',
        'about_us': 'हमारे बारे में',
        'contact': 'संपर्क करें',
        'help_faq': 'मदद और अक्सर पूछे जाने वाले प्रश्न',
        'vidya_sakhi': 'विद्यासखि',
        'learning_bestie': 'आपका अभ्यास मित्र और AI सहयोगी',
        'hi_vidya_sakhi': 'हाय! मैं विद्यासखि 👋',
        'friendly_ai_companion': 'आपका स्नेही अभ्यास सहयोगी',
        'your_badges': 'आपके ब्याड्ज़ी:',
        'average_score_per_subject': 'प्रत्येक विषय के लिए औसत स्कोर',
        'quiz_scores_over_time': 'समय के साथ क्विज स्कोर',
        'quiz_completion_status': 'क्विज पूर्णता स्थिति',
        'recent_quiz_history': 'हाल ही में क्विज इतिहास',
        'review_past_quizzes': 'पिछले क्विज़ को समीक्षित करें',
        'student_progress_dashboard': 'विद्यार्थी प्रगति डैशबोर्ड',
        'get_in_touch': 'संपर्क करें',
        'ai_learning_companion': 'आपका AI अभ्यास सहयोगी',
        'manage_study_materials': 'अध्याय सामग्री प्रबंधित करें और प्रगति निगरान करें',
        'faq_intro': 'अक्सर पूछे जाने वाले प्रश्न',
        'faq_q1': 'क्विज कैसे शुरू करें?',
        'faq_a1': 'क्विज विभाग में जाएं और Start Quiz क्लिक करें।',
        'faq_q2': 'भाषा कैसे बदलें?',
        'faq_a2': 'साइडबार में भाष ड्रॉपडाउन का उपयोग करें।',
        'faq_q3': 'मेरी प्रगति कैसे देखें?',
        'faq_a3': 'आपके स्कोर और ब्याड्ज़ देखने के लिए विश्लेषण में जाएं।',
        'faq_q4': 'कैसे मदद कर सकते हैं?',
        'faq_a4': 'संपर्क विभाग का उपयोग करें।',
        'badge_first_quiz': '🏅 पहली क्विज पूर्ण है',
        'badge_scored_80': '🌟 80%+ स्कोर स्कोर किया',
        'badge_five_quizzes': '🎯 5+ क्विज़ पूर्ण है',
        'badge_improved': '📈 समय के साथ बेहतर हो गया',
        'no_quiz_history': 'क्विज़ इतिहास उपलब्ध नहीं है। अपनी प्रगति देखने के लिए कुछ क्विज़ को प्रयास करें!',
        'date': 'तारीख',
        'subject': 'विषय',
        'score': 'स्कोर',
        'status': 'स्थिति',
        'retake_quiz': 'क्विज फिर से प्रयास करें',
        'study_materials_preparing': 'इस कक्षा के लिए अध्याय सामग्री तैयार है। कृपया जल्द वापस देखें!',
        'download_notes': '{subject} नोट्स डाउनलोड करें',
        'pdf_unavailable': '{subject} के लिए PDF अस्थायी रूप से उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।',
        'additional_resources': 'अतिरिक्त संसाधन:',
        'video_explanations': 'वीडियो व्याख्यान:',
        'tutor_srinivasa_chary': 'टी. श्रीनिवास चारी (फిजिक्स)',
        'khan_academy': 'खान अकाडमी',
        'learn_cbse': 'लर्न सीबीएसई',
        'math_antics': 'गणित यांत्रिकी',
        'crash_course': 'क्रैश कोर्स',
        'amoeba_sisters': 'अमीबा सिस्टर्स',
        'british_council': 'ब्रिटिश कौन्सिल',
        'mr_duncan': 'अंग्रेजी अडिक्ट मिस्टर डंकन',
        'hindi_vyakaran': 'हिंदी व्याकरण',
        'exampur_hindi': 'एग्जांपूर हिंदी',
        'kaushik_telugu': 'कौशिक से तेलुगु नेरचुकोंडि',
        'telugu_badi': 'तेलुगु बड़ी',
        'unacademy': 'यूनकाडमी',
        'scert_link_info': 'यदि सीधा पाठ्यपुस्तक लिंक काम नहीं करता है, तो कृपया नीचे दिए गए SCERT ई-बुक्स पोर्टल लिंक का उपयोग करें ताकि नवीनतम सामग्री प्राप्त कर सकें।',
        'chat_with_ai_companion': 'अपने AI साथी से चैट करें',
    },
    'te': {
        'welcome': 'స్వాగతం',
        'role': 'పాత్ర',
        'logout': 'లాగ్ అవుట్',
        'settings': 'సెట్టింగ్స్',
        'select_class': 'తరగతి ఎంచుకోండి',
        'language': 'భాష / Language',
        'theme': 'థీమ్',
        'voice_output': 'వాయిస్ అవుట్‌పుట్',
        'accessibility': 'ప్రాప్యత',
        'large_font': 'పెద్ద అక్షరాలు',
        'dyslexia_font': 'డిస్లెక്సియా-ఫ్రెండ్లీ ఫాంట్',
        'quick_access': 'త్వరిత యాక్సెస്',
        'chat_with_sakhi': 'సఖితో చాట్ చేయండి',
        'new_quiz': 'పుతియ క్విజ్',
        'study_materials': 'పాఠ്య పదార్థాలు',
        'main_menu': 'ప్రధాన మెనూ',
        'test_knowledge': 'మీ జ్ఞానాన్ని పరీక్షించుకోండి',
        'choose_subject': 'విషయం ఎంచుకోండి:',
        'num_questions': 'ప్రశ్నల సంఖ్య:',
        'start_quiz': 'క్విజ్ ప్రారంభించండి',
        'quiz_time': 'క్విజ్ సమయం',
        'submit_answer': 'సమాధానం సమర్పించండి',
        'exit_quiz': 'క్విజ్ నుండి నిష్క్రమించండి',
        'try_again': 'మళ్లీ ప్రయత్నించండి',
        'back_to_menu': 'మెనూకు తిరిగి వెళ్ళండి',
        'correct': 'సరైనది!',
        'incorrect': 'తప్పు!',
        'quiz_completed': 'క్విజ్ పూర്తయింది!',
        'score': 'స్కോర్',
        'percentage': 'శాతం',
        'excellent': 'అద్భుతం!',
        'good_job': 'బాగుంది!',
        'keep_studying': 'ఇంకా చదవండి!',
        'detailed_results': 'వివరణాత്మక ఫలితాలు',
        'your_answer': 'మీ సమాధానం',
        'correct_answer': 'సరైన సమాధానం',
        'incomplete': 'అపూర్ణం',
        'completed': 'పూర్తయింది',
        'questions_attempted': 'ప్రయత్నించిన ప్రశ్నలు',
        'questions_total': 'మొత్తం ప్రశ్నలు',
        'quiz_exited': 'క్విజ్ నుండి నిష్క్రమించారు!',
        'note_unattempted': 'గమనిక: ప్రయత్నించని ప్రశ్నలు తప్పుగా పరిగణించబడతాయి. ఈ క్విజ్ మీ విశ్లేషణలో అపూర్ణంగా గుర్తించబడింది.',
        'analytics': 'విశ్లేషణ',
        'about_us': 'మా గురించి',
        'contact': 'సంప్రదించండి',
        'help_faq': 'సహాయం & తరచుగా అడిగే ప్రశ్నలు',
        'vidya_sakhi': 'విద్యా సఖి',
        'learning_bestie': 'మీ అభ్యాస మిత్రుడు & AI సహచరుడు',
        'hi_vidya_sakhi': 'హాయ్! నేను విద్యా సఖి 👋',
        'friendly_ai_companion': 'మీ స్నేహపూర్వక AI అభ్యాస సహచరుడు',
        'your_badges': 'మీ బ్యాడ్జీలు:',
        'average_score_per_subject': 'ప్రతి విషయానికి సగటు స్కോర్',
        'quiz_scores_over_time': 'సమయంలో క്విజ് స్కോర്',
        'quiz_completion_status': 'క്విజ് పూర്తి స్థితి',
        'recent_quiz_history': 'ఇటీవలి క്విజ് చరిత్ర',
        'review_past_quizzes': 'గత క്విజ్‌లను సమీక్షించండి',
        'student_progress_dashboard': 'విద్యార్థి పురోగతి డాష్‌బోర్డ్',
        'get_in_touch': 'సంప్రదించండి',
        'ai_learning_companion': 'మీ AI అభ్యాస సహచరుడు',
        'manage_study_materials': 'పాఠ്య పదార്థాలను నిర్వహించండి & పురോగతిని పర్యవేక్షించండి',
        'faq_intro': 'తరచుగా అడిగే ప్రశ్నలు',
        'faq_q1': 'క్విజ్‌ను ఎలా ప్రారంభించాలి?',
        'faq_a1': 'క్విజ్ విభాగానికి వెళ్లి Start Quiz క్లిక్ చేయండి.',
        'faq_q2': 'భాషను ఎలా మార్చాలి?',
        'faq_a2': 'సైడ్‌బార్‌లో భాష డ్రాప్‌డౌన్‌ను ఉపయోగించండి.',
        'faq_q3': 'నా పురోగతిని ఎలా చూడాలి?',
        'faq_a3': 'మీ స్కోర్లు మరియు బ్యాడ్జ్‌లను చూడటానికి విశ్లేషణలకు వెళ్లండి.',
        'faq_q4': 'సహాయం కోసం ఎవరిని సంప్రదించాలి?',
        'faq_a4': 'సంప్రదించండి విభాగాన్ని ఉపయోగించండి.',
        'badge_first_quiz': '🏅 మొదటి క్విజ్ పూర్తి చేశారు',
        'badge_scored_80': '�� క్విజ్‌లో 80%+ స్కോర్ సాధించారు',
        'badge_five_quizzes': '🎯 5+ క్విజ్‌లు పూర్తి చేశారు',
        'badge_improved': '📈 సమయానుకూలంగా మెరుగుపడ్డారు',
        'no_quiz_history': 'క్విజ్ చరిత్ర లేదు. మీ పురోగతిని చూడటానికి కొన్ని క్విజ్‌లు ప్రయత్నించండి!',
        'date': 'తేదీ',
        'subject': 'విషయం',
        'score': 'స్కോర్',
        'status': 'స్థితి',
        'retake_quiz': 'క్విజ్ మళ్లీ ప్రయత్నించండి',
        'study_materials_preparing': 'ఈ తరగతికి అధ్యయన పదార్థాలు సిద్ధంగా ఉన్నాయి. దయచేసి త్వరలో మళ్లీ చూడండి!',
        'download_notes': '{subject} నోట్స్ డౌన్‌లోడ్ చేయండి',
        'pdf_unavailable': '{subject} కోసం PDF తాత్కాలికంగా అందుబాటులో లేదు. దయచేసి తర్వాత ప్రయత్నించండి.',
        'additional_resources': 'అదనపు వనరులు:',
        'video_explanations': 'వీడియో వివరణలు:',
        'tutor_srinivasa_chary': 'టి. శ్రీనివాస చారి (ఫిజిక్స్)',
        'khan_academy': 'ఖాన్ అకాడమీ',
        'learn_cbse': 'లెర్న్ CBSE',
        'math_antics': 'మ్యాథ్ యాంటిక్స్',
        'crash_course': 'క్రాష్ కోర్స్',
        'amoeba_sisters': 'అమీబా సిస్టర్స్',
        'british_council': 'బ్రిటిష్ కౌన్సిల్',
        'mr_duncan': 'ఇంగ్లీష్ అడిక్ట్ మిస్టర్ డంకన్',
        'hindi_vyakaran': 'హిందీ వ్యాకరణ్',
        'exampur_hindi': 'ఎగ్జాంపూర్ హిందీ',
        'kaushik_telugu': 'కౌశిక్ తో తెలుగు నేర్చుకోండి',
        'telugu_badi': 'తెలుగు బడి',
        'unacademy': 'యూనకాడమీ',
        'scert_link_info': 'ప్రత్యక్ష పాఠ్యపుస్తక లింక్ పనిచేయకపోతే, దయచేసి క్రింద ఉన్న SCERT eBooks పోర్టల్ లింక్‌ను ఉపయోగించి తాజా పదార్థాలను పొందండి.',
        'chat_with_ai_companion': 'మీ AI సహచరుతో చాట్ చేయండి',
    },
    'ta': {
        'welcome': 'வரவும்',
        'role': 'பாதியம்',
        'logout': 'வீழ்ச்சி',
        'settings': 'அமைப்புகள்',
        'select_class': 'வகுப்பைத் தேர்ந்தெடுக்க',
        'language': 'மொழி / Language',
        'theme': 'தேம்',
        'voice_output': 'கேட்டு வெளியுள்ள',
        'accessibility': 'பயன்புல்',
        'large_font': 'பெரிய எழுத்து',
        'dyslexia_font': 'டிஸ்லெக்ஸியா-புரிந்து பாதியம்',
        'quick_access': 'வேகமாக அணுகுதல்',
        'chat_with_sakhi': 'சாட்டுடன் சாட்டு செய்ய',
        'new_quiz': 'புதிய குவிஜ்',
        'study_materials': 'பாடப்புத்தகங்கள்',
        'main_menu': 'முக்கிய மெனு',
        'test_knowledge': 'உங்கள் அறிவை சரிபார்க்க',
        'choose_subject': 'பாடம் தேர்ந்தெடுக்க',
        'num_questions': 'கேள்விகள் எண்',
        'start_quiz': 'குவிஜ் தொடங்க',
        'quiz_time': 'குவிஜ் நேரம்',
        'submit_answer': 'பதிலை சமர்பிக்க',
        'exit_quiz': 'குவிஜ் வெளியே செல்ல',
        'try_again': 'மீண்டும் முயற்சிக்க',
        'back_to_menu': 'மெனுக்கு போக',
        'correct': 'சரியானது!',
        'incorrect': 'தவறானது!',
        'quiz_completed': 'குவிஜ் முடிந்தது!',
        'score': 'மதிப்பெண்',
        'percentage': 'சதவீதம்',
        'excellent': 'மிகவும் நல்லது!',
        'good_job': 'நல்ல வேலை!',
        'keep_studying': 'அடுத்த பாடத்தை படிக்க',
        'detailed_results': 'விரிவான விளைவுகள்',
        'your_answer': 'உங்கள் பதில்',
        'correct_answer': 'சரியான பதில்',
        'incomplete': 'முட்டும்',
        'completed': 'முடிந்தது',
        'questions_attempted': 'முயற்சிக்கப்பட்ட கேள்விகள்',
        'questions_total': 'மொத்த கேள்விகள்',
        'quiz_exited': 'குவிஜ் வெளியே செல்லப்பட்டது!',
        'note_unattempted': 'குறிப்பு: முயற்சிக்கப்படாத கேள்விகள் தவறாகப்படுத்தப்படுகின்றன. இந்த குவிஜ் உங்கள் பகுப்பாய்வில் முட்டும் என்று குறிப்பிடப்படுகின்றது.',
        'analytics': 'பகுப்பாய்வு',
        'about_us': 'நம்மைப் பற்றி',
        'contact': 'இணைய',
        'help_faq': 'உதவி மற்றும் அடிப்படையான கேள்விகள்',
        'vidya_sakhi': 'விதியாசி',
        'learning_bestie': 'உங்கள் படிப்பு நண்பகர் & AI உதவியாளர்',
        'hi_vidya_sakhi': 'ஹாய்! நான் விதியாசி 👋',
        'friendly_ai_companion': 'உங்கள் நேரியல் படிப்பு உதவியாளர்',
        'your_badges': 'உங்கள் பிரதிபலிக்கும்',
        'average_score_per_subject': 'ஒவ்வொரு பாடத்திற்கும் சராசரி மதிப்பெண்',
        'quiz_scores_over_time': 'நேரம் முன்னில் குவிஜ் மதிப்பெண்கள்',
        'quiz_completion_status': 'குவிஜ் முடிவு நிலை',
        'recent_quiz_history': 'சில நேரம் குவிஜ் வரலாறு',
        'review_past_quizzes': 'முன்னில் குவிஜ்களைப் பரிந்துரைக்க',
        'student_progress_dashboard': 'மாணிகர் முன்னில் பட்டியல்',
        'get_in_touch': 'இணைய',
        'ai_learning_companion': 'உங்கள் AI படிப்பு உதவியாளர்',
        'manage_study_materials': 'பாடப்புத்தகங்களைச் சமர்பிக்கவும் & முன்னில் பட்டியல் நிர்வாகம்',
        'faq_intro': 'அடிப்படையான கேள்விகள்',
        'faq_q1': 'குவிஜ் எப்படி தொடங்கவா?',
        'faq_a1': 'குவிஜ் பகுதிக்கு செல்லவும் & Start Quiz கிளிக் செய்ய',
        'faq_q2': 'மொழி எப்படி மாற்றவா?',
        'faq_a2': 'பக்கப்பாதலில் மொழி ட்ராப் டௌன் பயன்புல்',
        'faq_q3': 'என் முன்னில் எப்படி பார்க்கலா?',
        'faq_a3': 'உங்கள் மதிப்பெண்கள் & பிரதிபலிக்கும் பரிந்துரைக்க',
        'faq_q4': 'எப்படி உதவி செய்யலாம்?',
        'faq_a4': 'இணைய பகுதல் பயன்புல்',
        'badge_first_quiz': '🏅 முதல் குவிஜ் முடிந்தது',
        'badge_scored_80': '🌟 80%+ மதிப்பெண் மதிப்பெண்',
        'badge_five_quizzes': '🎯 5+ குவிஜ்கள் முடிந்தது',
        'badge_improved': '📈 நேரம் முன்னில் மேலிருக்கவும்',
        'no_quiz_history': 'குவிஜ் வரலாறு இல்லை. உங்கள் முன்னில் படிக்கவும்!',
        'date': 'தேதி',
        'subject': 'பாடம்',
        'score': 'மதிப்பெண்',
        'status': 'நிலை',
        'retake_quiz': 'மீண்டும் முயற்சிக்க',
        'study_materials_preparing': 'இந்த வகுப்பிற்கு பாடப்புத்தகங்கள் தயாரிக்கப்படுகின்றன. மேலும் சில நேரம் மீண்டும் பார்க்கவும்!',
        'download_notes': '{subject} குத்துக்கள் பதிவிறக்கவும்',
        'pdf_unavailable': '{subject} க்கு PDF மறுக்கும் பயன்புல் இல்லை. மேலும் நேரம் மீண்டும் முயற்சிக்கவும்.',
        'additional_resources': 'மேலும் வளர்ச்சிக்கும் வளர்ச்சிக்கும்',
        'video_explanations': 'வீடியோ விளக்கங்கள்:',
        'tutor_srinivasa_chary': 'டி. சுரீனிவாச சாரி (இயற்பியல்)',
        'khan_academy': 'காந் அகாடமி',
        'learn_cbse': 'படிக்க CBSE',
        'math_antics': 'கணித யான்றிக்கை',
        'crash_course': 'கிராஷ் கோர்ஸ்',
        'amoeba_sisters': 'அமீபா சிஸ்டர்ஸ்',
        'british_council': 'பிரிட்டிஷ் கௌன்ஸில்',
        'mr_duncan': 'ஆங்கில அடிக்கும் மிஸ்டர் டங்கன்',
        'hindi_vyakaran': 'ஹிந்தி விகாரணம்',
        'exampur_hindi': 'ஏக்மாபூர் ஹிந்தி',
        'kaushik_telugu': 'கௌஷிக் மேலும் தெலுங்கு நேர்ச்சிக்க',
        'telugu_badi': 'தெலுங்கு பெரிய',
        'unacademy': 'யூனகாடமி',
        'chat_with_ai_companion': 'உங்கள் AI படிப்பு உதவியாளர்',
        'faq_q5': 'எப்படி ஆதரவை தொடர்பு கொள்வது?',
        'faq_a5': 'கீழே உள்ள contact form-ஐ கிளிக் செய்து உங்கள் விவரங்களை அனுப்பவும்.',
        'faq_q6': 'நான் என் கடவுச்சொல்லை மறந்துவிட்டேன். எப்படி மீட்டமைப்பது?',
        'faq_a6': 'உங்கள் ஆசிரியர் அல்லது நிர்வாகியை தொடர்பு கொள்ளவும். விரைவில் Self-service password reset வசதி வரும்!',
        'faq_q7': 'பிழை அல்லது புதிய அம்சம் பரிந்துரைக்க எப்படி?',
        'faq_a7': 'Contact form-ஐ பயன்படுத்தவும் அல்லது sathviktad@gmail.com-க்கு மின்னஞ்சல் அனுப்பவும்.',
        'faq_q8': 'என் தரவு பாதுகாப்பாக இருக்கிறதா?',
        'faq_a8': 'ஆம்! உங்கள் க்விஸ் வரலாறும் தனிப்பட்ட தரவும் பாதுகாப்பாக சேமிக்கப்படுகிறது. நீங்கள் மற்றும் உங்கள் ஆசிரியர்கள் மட்டுமே பார்க்க முடியும்.',
        'faq_q9': 'Leaderboard என்றால் என்ன? அது எப்படி செயல்படுகிறது?',
        'faq_a9': 'Leaderboard (ஆசிரியர் dashboard) மாணவர்களின் சராசரி க்விஸ் மதிப்பெண் அடிப்படையில் Top students-ஐ காட்டும். இது ஆரோக்கியமான போட்டியை ஊக்குவிக்கிறது!',
        'faq_q10': 'Vidya Sakhi-யை என் கைபேசி அல்லது டேப்லெட்டில் பயன்படுத்த முடியுமா?',
        'faq_a10': 'ஆம்! Vidya Sakhi எந்த சாதனத்திலும் (கைபேசி, டேப்லெட்) உலாவியில் வேலை செய்யும்.',
        'faq_q11': 'Text-to-speech அல்லது Voice அம்சங்களை எப்படி பயன்படுத்துவது?',
        'faq_a11': "Sidebar-இல் '🔊 Voice Output' ஐ இயக்கவும். க்விஸ் மற்றும் பாடப்பொருளுக்கு விரைவில் இந்த அம்சம் வரும்.",
        'contact_info': 'தொடர்பு தகவல்',
        'email': 'மின்னஞ்சல்',
        'phone': 'தொலைபேசி',
        'address': 'முகவரி',
        'support_hours': 'ஆதரவு நேரம்',
        'quick_contact_form': 'விரைவு தொடர்பு படிவம்',
        'your_name': 'உங்கள் பெயர்*',
        'email_address': 'மின்னஞ்சல் முகவரி*',
        'phone_number': 'தொலைபேசி எண்',
        'subject': 'பொருள்',
        'general_inquiry': 'பொது விசாரணை',
        'message': 'செய்தி*',
        'describe_query': 'உங்கள் கேள்வி அல்லது கருத்தை விவரிக்கவும்...',
        'connect_with_us': 'எங்களை தொடர்பு கொள்ள',
        'resources': 'வளங்கள்',
        'user_guide': 'பயனர் வழிகாட்டி',
        'faqs': 'அடிக்கடி கேட்கப்படும் கேள்விகள்',
        'video_tutorials': 'வீடியோ பயிற்சிகள்',
        'emergency_support': 'அவசர ஆதரவு',
        'emergency_phone': 'அவசர தொலைபேசி',
        'acknowledgments': 'நன்றி',
        'vision': 'எங்கள் நோக்கம்',
        'mission': 'எங்கள் பணி',
        'ai_powered': 'AI இயக்கம்',
        'comprehensive_content': 'முழுமையான உள்ளடக்கம்',
        'voice_enabled': 'குரல் ஆதரவு',
        'progress_tracking': 'முன்னேற்ற கண்காணிப்பு',
        'secure_safe': 'பாதுகாப்பான மற்றும் பாதுகாக்கப்பட்ட',
        'personalized_ai_tutor': 'தனிப்பயன் AI டியூட்டர்',
        'democratize_education': 'தரமான கல்வியை அனைவருக்கும் வழங்குதல்',
    },
    'ml': {
        'welcome': 'സ്വാഗതം',
        'role': 'പാത്ര',
        'logout': 'ലാഗ് അവുട്',
        'settings': 'സെറ്റിംഗ്സ്',
        'select_class': 'തരഗതി എന്ന് തിരഞ്ഞെടുക്ക',
        'language': 'ഭാഷ / Language',
        'theme': 'ഥീമ്',
        'voice_output': 'വായിസ് അവുട്പുട്',
        'accessibility': 'പ്രാപ്യത',
        'large_font': 'പെദ്ദ അക്ഷരാലുള്ള',
        'dyslexia_font': 'ഡിസ്ലെക്സിയാ-ഫ്രെംഡ്ലീ ഫാംട്',
        'quick_access': 'ത്വരിത യാക്സെസ്',
        'chat_with_sakhi': 'സഖിതോ ചാട് ചേയംഡി',
        'new_quiz': 'പുതിയ ക്വിജ്',
        'study_materials': 'പാഠ്യ പദാര്ഥാലുള്ള',
        'main_menu': 'പ്രധാന മെനൂ',
        'test_knowledge': 'നിങ്ങളുടെ ജ്ഞാനം പരിക്ഷിക്കുക',
        'choose_subject': 'വിഷയം എന്ന് തിരഞ്ഞെടുക്ക',
        'num_questions': 'പ്രശ్നങ്ങളുടെ എണ്ണം:',
        'start_quiz': 'ക്വിജ് പ്രാരംഭിക്ക',
        'quiz_time': 'ക്വിജ് സമയം',
        'submit_answer': 'ഉത്തരം സമര്പിക്ക',
        'exit_quiz': 'ക്വിജ് നുംഡി നിഷ്ക్രമിക്ക',
        'try_again': 'മള്ലീ പ്രയത്നിക്ക',
        'back_to_menu': 'മെനൂക്കു തിരിച്ചു വയര്‍',
        'correct': 'ശരിയായി!',
        'incorrect': 'തെറ്റായി!',
        'quiz_completed': 'ക്വിജ് പൂര്ത്തി വരും!',
        'score': 'സ്കോര്',
        'percentage': 'ശതമാനം',
        'excellent': 'അദ്ഭുതം!',
        'good_job': 'ബാഗുംദി!',
        'keep_studying': 'ഇടുക്കയായി പാഠം പാലിക്ക',
        'detailed_results': 'വിവരണാത്മക ഫലിതാലുള്ള',
        'your_answer': 'നിങ്ങളുടെ ഉത്തരം',
        'correct_answer': 'ശരിയായ ഉത്തരം',
        'incomplete': 'അപൂര്ണം',
        'completed': 'പൂര്ത്തി വരും',
        'questions_attempted': 'പ്രയത്നിക്കയായ പ്രശ്നങ്ങളുടെ എണ്ണം:',
        'questions_total': 'മൊത്തം പ്രശ്നങ്ങളുടെ എണ്ണം:',
        'quiz_exited': 'ക്വിജ് നുംഡി നിഷ്ക్രമിക്കാരുള്ള!',
        'note_unattempted': 'ഗമനിക: പ്രയത്നിക്കയായ പ്രശ്നങ്ങളുടെ തെറ്റായി പരിഗണിക്കയായിരിക്കും. ഈ ക്വിജ് നിങ്ങളുടെ വിശ్ലేഷണത്തില്‍ അപൂര്ണം വരും എന്ന് കാര്യം പറയാം.',
        'analytics': 'വിശ്ലേഷണ',
        'about_us': 'ഞങ്ങളുടെ ബാക്ക്',
        'contact': 'സംപ്രദിംച്ചു',
        'help_faq': 'സഹായം & തരചുഗാ അഡിഗേ പ്രശ്നങ്ങളുടെ',
        'vidya_sakhi': 'വിദ്യാ സഖി',
        'learning_bestie': 'നിങ്ങളുടെ അഭിസാദ്ധ്യം മിത്രവും & AI സഹചര്യം',
        'hi_vidya_sakhi': 'ഹായ്! ഞാൻ വിദ്യാ സഖി 👋',
        'friendly_ai_companion': 'നിങ്ങളുടെ സ്നേഹപൂര്വക അഭിസാദ്ധ്യം സഹചര്യം',
        'your_badges': 'നിങ്ങളുടെ ബ്യാഡ്ജ്ജീ:',
        'average_score_per_subject': 'ഒരു വിഷയത്തില്‍ ശരാശരി സ്കോര്',
        'quiz_scores_over_time': 'സമയത്തില്‍ ക്വിജ് സ്കോര്',
        'quiz_completion_status': 'ക്വിജ് പൂര്ത്തി സ്ഥിതി',
        'recent_quiz_history': 'ഇത്തരത്തിലുള്ള ക്വിജ് ഇതിഹാസം',
        'review_past_quizzes': 'പിന്നിലുള്ള ക്വിജർ സമയം കാരക്കുക',
        'student_progress_dashboard': 'വിദ്യാര്ഥി പ്രഗതി ഡാഷ്ബോറ്ഡ്',
        'get_in_touch': 'സംപ്രദിംച്ചു',
        'ai_learning_companion': 'നിങ്ങളുടെ AI അഭിസാദ്ധ്യം സഹചര്യം',
        'manage_study_materials': 'പാഠ്യ പദാര്ഥാലുള്ള നിര്വഹിക്കവും & പുരോഗതി പരിശോധിക്കവും',
        'faq_intro': 'അടിപ്പടുമ്പോളുള്ള പ്രശ്നങ്ങളുടെ',
        'faq_q1': 'ക്വിജ് എങ്ങനെ പ്രാരംഭിക്കലോ?',
        'faq_a1': 'ക്വിസ് ആരംഭിക്കാൻ, ക്വിസ് വിഭാഗത്തിൽ നിന്ന് ഒരു വിഷയം തിരഞ്ഞെടുക്കുക, തുടർന്ന് "ക്വിസ് ആരംഭിക്കുക" ബട്ടൺ ക്ലിക്ക് ചെയ്യുക.',
        'faq_q5': 'എന്നെ സഹായിക്കാൻ എന്ത് ചെയ്യാം?',
        'faq_a5': 'നിങ്ങളുടെ ഇമെയിൽ അല്ലെങ്കിൽ ഇമെയിൽ പോലുള്ള ഒരു ഫോറിലുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_q6': 'നാം പിന്നെ എന്നെ കാര്യം പറയാനുള്ള പോലുള്ള ഒരു ഫോറിലുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_a6': 'നിങ്ങളുടെ ആച്ഛരിയർ അല്ലെങ്കിൽ നിര്വാകിയെ തൊടരുന്നുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_q7': 'പിഴ്ശയും പുതിയ അമ്മയും പരിന്നിക്കാൻ എന്ത് ചെയ്യാം?',
        'faq_a7': 'നിങ്ങളുടെ ഇമെയിൽ അല്ലെങ്കിൽ ഇമെയിൽ പോലുള്ള ഒരു ഫോറിലുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_q8': 'നാം പിന്നെ എന്നെ കാര്യം പറയാനുള്ള പോലുള്ള ഒരു ഫോറിലുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_a8': 'നിങ്ങളുടെ ആച്ഛരിയർ അല്ലെങ്കിൽ നിര്വാകിയെ തൊടരുന്നുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_q9': 'ലെഡറ്റ് ബോർഡ് എന്നാൽ എന്ന്?',
        'faq_a9': 'ലെഡറ്റ് ബോർഡ് (ആച്ഛരിയർ ഡാഷ്ബോർഡ്) ആരംഭിക്കാൻ ആരംഭിക്കാൻ നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_q10': 'നാം പിന്നെ എന്നെ കാര്യം പറയാനുള്ള പോലുള്ള ഒരു ഫോറിലുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_a10': 'നിങ്ങളുടെ ആച്ഛരിയർ അല്ലെങ്കിൽ നിര്വാകിയെ തൊടരുന്നുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_q11': 'പാഠപ്പുത്തകങ്കളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'faq_a11': 'നിങ്ങളുടെ ആച്ഛരിയർ അല്ലെങ്കിൽ നിര്വാകിയെ തൊടരുന്നുകൾ ഉപയോഗിക്കുക. അതു നിങ്ങളുടെ പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'contact_info': 'തൊടരുന്ന പ്രശ്നങ്ങളുടെ പരിഹരണത്തില്‍ സഹായിക്കാനുള്ള ഒരു പ്രായം നല്കുക.',
        'email': 'ഇമെയിൽ',
        'phone': 'തൊലൈയും',
        'address': 'വിവരങ്ങളുടെ പാലം',
        'support_hours': 'ആതരവും നേരം',
        'quick_contact_form': 'വിരൈവ് പ്രശ്നങ്ങളുടെ പരിഹരണം',
        'your_name': 'നിങ്ങളുടെ പേര്*',
        'email_address': 'ഇമെയിൽ വിവരങ്ങളുടെ പാലം*',
        'phone_number': 'തൊലൈയും എണ്ണം',
        'subject': 'പൊരുള്ളില്‍',
        'general_inquiry': 'പൊതു വിചാരണ്യം',
        'message': 'ചെയ്യുക*',
        'describe_query': 'നിങ്ങളുടെ കേള്വി അല്ലെങ്കിൽ കരുത്തൈ വിവരിക്കുക...',
        'connect_with_us': 'എങ്കളുടെ തൊടരുന്ന പ്രശ്നങ്ങളുടെ പരിഹരണം',
        'resources': 'വളങ്ങളുടെ പാലം',
        'user_guide': 'പയനരുടെ വഴികാട്ടി',
        'faqs': 'അടിക്കടി കേട്കപ്പടുമ്പോളുള്ള കേള്വികളുടെ പരിഹരണം',
        'video_tutorials': 'വീഡിയോ പയിറ്റകളുടെ പാലം',
        'emergency_support': 'അവചര ആതരവും',
        'emergency_phone': 'അവചര തൊലൈയും',
        'acknowledgments': 'നന്ദി',
        'vision': 'എങ്കളുടെ നോക്കം',
        'mission': 'എങ്കളുടെ പണി',
        'ai_powered': 'AI ഇയക്കമ്',
        'comprehensive_content': 'മുഴുമൈയായ ഉള്ളടക്കം',
        'voice_enabled': 'കുരല് ആതരവും',
        'progress_tracking': 'മുന്ന് കണ്കാണിപ്പും',
        'secure_safe': 'പാതുകാപ്പായിയും പാതുകാക്കപ്പട്ട',
        'personalized_ai_tutor': 'തഩിപ്പയന് അയ്യില്‍ ടുടോർ',
        'democratize_education': 'തരമായ കല്വിയൈ അന്നവരെയും വഴങ്കുതല്‍',
    },
    'kn': {},
    'bn': {},
    'mr': {},
    'gu': {
        'test_knowledge': 'તમારી જાણકારીની કસોટી લો'
    },
    'pa': {},
    'ur': {},
}

def t(key, lang=None):
    """
    Translation helper for UI text.
    Usage: t('welcome') or t('welcome', 'te')
    If lang is None, uses st.session_state.selected_language if available, else 'en'.
    If translation is missing for a supported language, uses translatepy/googletrans to translate from English at runtime, translation should be accurate and correct.
    """
    if lang is None:
        try:
            lang = st.session_state.selected_language
        except Exception:
            lang = 'English'
    code = get_language_code(lang) if len(lang) > 2 else lang
    if code not in TRANSLATIONS:
        code = 'en'
    # Try dictionary translation first
    value = TRANSLATIONS.get(code, {}).get(key)
    if value:
        return value
    # Fallback to English if available
    en_value = TRANSLATIONS['en'].get(key, key)
    # For any non-English language, try runtime translation
    if code != 'en':
        try:
            result = TRANSLATEPY.translate(en_value, code).result
            if result and result != en_value:
                return result
        except Exception:
            pass
        try:
            result = GOOGLETRANS.translate(en_value, dest=code).text
            if result and result != en_value:
                return result
        except Exception:
            pass
    return en_value
