import streamlit as st

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

def apply_theme(theme):
    """Apply dark or light theme to the app"""
    if theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #ffffff;
        }
        .stButton > button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        .stSelectbox > div > div {
            background-color: #2e2e2e;
            color: white;
            border-radius: 8px;
        }
        .stTextInput > div > div > input {
            background-color: #2e2e2e;
            color: white;
            border-radius: 8px;
            border: 1px solid #4CAF50;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #2e2e2e;
            border-radius: 8px;
            color: white;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(45deg, #4CAF50, #45a049);
        }
        .stProgress > div > div > div {
            background: linear-gradient(45deg, #4CAF50, #45a049);
        }
        .stChatMessage {
            background-color: #2e2e2e;
            border-radius: 12px;
            border: 1px solid #4CAF50;
        }
        .stExpander {
            background-color: #2e2e2e;
            border-radius: 8px;
            border: 1px solid #4CAF50;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2c3e50;
        }
        .stButton > button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 1px solid #4CAF50;
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #4CAF50;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
        }
        .stProgress > div > div > div {
            background: linear-gradient(45deg, #4CAF50, #45a049);
        }
        .stChatMessage {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stExpander {
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

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
