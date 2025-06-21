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

def get_avatar_svg():
    """Return SVG avatar for Vidya Sakhi"""
    return """
    <div style="text-align: center; margin: 2rem 0;">
        <svg width="150" height="150" viewBox="0 0 150 150" style="border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <!-- Head -->
            <circle cx="75" cy="60" r="25" fill="#fdbcb4"/>
            
            <!-- Hair -->
            <path d="M50 45 Q75 25 100 45 Q100 35 95 30 Q75 15 55 30 Q50 35 50 45" fill="#4a4a4a"/>
            
            <!-- Eyes -->
            <circle cx="68" cy="58" r="3" fill="#000"/>
            <circle cx="82" cy="58" r="3" fill="#000"/>
            <circle cx="68" cy="57" r="1" fill="#fff"/>
            <circle cx="82" cy="57" r="1" fill="#fff"/>
            
            <!-- Nose -->
            <ellipse cx="75" cy="62" rx="1" ry="2" fill="#f4a6a6"/>
            
            <!-- Mouth -->
            <path d="M70 67 Q75 72 80 67" stroke="#000" stroke-width="1" fill="none"/>
            
            <!-- Body -->
            <rect x="60" y="85" width="30" height="40" rx="15" fill="#4CAF50"/>
            
            <!-- Arms -->
            <circle cx="45" cy="95" r="8" fill="#fdbcb4"/>
            <circle cx="105" cy="95" r="8" fill="#fdbcb4"/>
            <rect x="50" y="90" width="15" height="8" fill="#4CAF50"/>
            <rect x="85" y="90" width="15" height="8" fill="#4CAF50"/>
            
            <!-- Book -->
            <rect x="35" y="85" width="12" height="8" fill="#ff6b6b" rx="1"/>
            <line x1="38" y1="87" x2="44" y2="87" stroke="#fff" stroke-width="0.5"/>
            <line x1="38" y1="89" x2="44" y2="89" stroke="#fff" stroke-width="0.5"/>
            <line x1="38" y1="91" x2="44" y2="91" stroke="#fff" stroke-width="0.5"/>
            
            <!-- Sparkles -->
            <text x="110" y="40" font-size="12" fill="#ffd700">✨</text>
            <text x="30" y="50" font-size="10" fill="#ffd700">⭐</text>
            <text x="120" y="110" font-size="8" fill="#ffd700">💫</text>
        </svg>
        <h4 style="color: #4CAF50; margin-top: 1rem;">Hi! I'm Vidya Sakhi 👋</h4>
        <p style="color: #666; font-size: 0.9rem;">Your friendly AI learning companion</p>
    </div>
    """
