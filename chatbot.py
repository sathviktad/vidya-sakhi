import random
import streamlit as st
from translatepy import Translate
from gtts import gTTS
import pygame
import io
import tempfile
import os
import requests
import json
from utils import get_language_code
import importlib

class ChatBot:
    def __init__(self):
        self.translator = Translate()
        self.knowledge_base = {
            'math': {
                'basic': {
                    'addition': "Addition means putting numbers together. For example, 2 + 3 = 5. Start with smaller numbers and practice daily!",
                    'subtraction': "Subtraction means taking away. Like 5 - 2 = 3. Think of it as counting backwards!",
                    'multiplication': "Multiplication is repeated addition. 3 × 4 means adding 3 four times: 3+3+3+3 = 12",
                    'division': "Division is sharing equally. 12 ÷ 3 = 4 means sharing 12 things among 3 groups equally."
                },
                'intermediate': {
                    'fractions': "Fractions show parts of a whole. 1/2 means one part out of two equal parts. To add fractions, make denominators same first.",
                    'decimals': "Decimals are another way to write fractions. 0.5 = 1/2. The digits after decimal point show parts smaller than 1.",
                    'algebra': "Algebra uses letters like x and y to represent unknown numbers. If x + 5 = 8, then x = 3.",
                    'geometry': "Geometry deals with shapes. A triangle has 3 sides, square has 4 equal sides, circle is perfectly round."
                },
                'advanced': {
                    'quadratic': "Quadratic equations have x². The formula is x = [-b ± √(b²-4ac)]/2a. Practice with simple examples first.",
                    'trigonometry': "Trigonometry studies triangles. sin, cos, tan are ratios. Remember: sin²θ + cos²θ = 1 always.",
                    'calculus': "Calculus studies change. Derivative shows rate of change, integral finds total change."
                }
            },
            'science': {
                'basic': {
                    'plants': "Plants need sunlight, water, and air to grow. They make their own food through photosynthesis using green leaves.",
                    'animals': "Animals are living beings that move, eat, breathe, and grow. They need food, water, and shelter to survive.",
                    'weather': "Weather changes daily. Sun makes it warm, clouds bring rain, wind moves air around us."
                },
                'physics': {
                    'motion': "Motion means changing position. Speed = distance/time. Acceleration means speeding up or slowing down.",
                    'force': "Force can push or pull objects. Newton's laws: 1) Objects at rest stay at rest 2) F=ma 3) Every action has equal opposite reaction.",
                    'energy': "Energy makes things happen. Kinetic energy is energy of motion, potential energy is stored energy."
                },
                'chemistry': {
                    'atoms': "Atoms are tiny building blocks of everything. They have protons (+), neutrons (0), and electrons (-).",
                    'elements': "Elements are pure substances made of one type of atom. Hydrogen is lightest, carbon forms many compounds.",
                    'reactions': "Chemical reactions change substances. Like burning, rusting, cooking. Atoms rearrange to form new compounds."
                },
                'biology': {
                    'cells': "Cells are basic units of life. Plant cells have cell wall, animal cells don't. Nucleus controls the cell.",
                    'genetics': "Genetics explains how traits pass from parents to children through DNA. DNA is like a instruction manual.",
                    'evolution': "Evolution explains how species change over time. Natural selection helps organisms adapt to environment."
                }
            },
            'english': {
                'grammar': "Grammar rules help us speak and write correctly. Subject does action, verb shows action, object receives action.",
                'vocabulary': "Building vocabulary means learning new words daily. Read books, use dictionary, practice using new words in sentences.",
                'writing': "Good writing needs clear ideas, proper grammar, and logical flow. Start with simple sentences, then combine them.",
                'literature': "Literature includes stories, poems, plays. They teach us about life, emotions, and different cultures."
            },
            'history': {
                'ancient': "Ancient India had great civilizations like Indus Valley, Mauryan Empire. They made advances in science, art, and trade.",
                'medieval': "Medieval period saw rise of Delhi Sultanate, Mughal Empire. Great architecture like Taj Mahal was built.",
                'modern': "Modern India includes freedom struggle, independence in 1947, and development as democratic nation."
            },
            'geography': {
                'earth': "Earth has land, water, and air. 71% is water (oceans), 29% is land (continents). Atmosphere protects us.",
                'climate': "Climate is long-term weather pattern. Tropical regions are hot, polar regions are cold, temperate regions are moderate.",
                'resources': "Natural resources like water, minerals, forests are gifts of nature. We must use them wisely and conserve them."
            }
        }
        
        self.responses = {
            'greeting': [
                "Hello! I'm Vidya Sakhi, your learning companion. How can I help you today?",
                "Hi there! Ready to learn something new today?",
                "Namaste! I'm here to help you with your studies. What would you like to know?"
            ],
            'motivation': [
                "You're doing great! Every small step in learning is a big achievement.",
                "Remember, even the greatest scholars started as beginners. Keep going!",
                "Learning is a journey, not a destination. I'm proud of your curiosity!"
            ],
            'study_tips': [
                "Here are some study tips: 1) Take regular breaks 2) Make notes 3) Practice daily 4) Ask questions!",
                "Study smart, not just hard! Try the Pomodoro technique - 25 minutes study, 5 minutes break.",
                "Create a study schedule, find a quiet place, and remember to stay hydrated while studying!"
            ],
            'exam_prep': [
                "Exam preparation tips: Review regularly, solve previous papers, get enough sleep, and stay positive!",
                "For exams: Make a timetable, focus on weak areas, take mock tests, and believe in yourself!"
            ]
        }
        
        # Initialize pygame mixer for audio
        try:
            pygame.mixer.init()
        except:
            pass
        
        # Try to initialize pyttsx3 for better TTS
        self.pyttsx3 = None
        self.tts_voice_id = None
        try:
            pyttsx3 = importlib.import_module('pyttsx3')
            self.pyttsx3 = pyttsx3.init()
            # Try to select a fluent female voice (e.g., Microsoft Zira)
            voices = self.pyttsx3.getProperty('voices')
            for v in voices:
                if 'zira' in v.name.lower() or (v.gender and v.gender.lower() == 'female'):
                    self.tts_voice_id = v.id
                    break
            if self.tts_voice_id:
                self.pyttsx3.setProperty('voice', self.tts_voice_id)
            self.pyttsx3.setProperty('rate', 180)  # Set a fluent, natural rate
        except Exception as e:
            self.pyttsx3 = None
    
    def categorize_input(self, text):
        """Categorize user input to provide relevant responses"""
        text_lower = text.lower()
        
        # Greeting keywords
        greeting_words = ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good afternoon']
        if any(word in text_lower for word in greeting_words):
            return 'greeting'
        
        # Subject keywords
        math_words = ['math', 'mathematics', 'algebra', 'geometry', 'arithmetic', 'calculation', 'number']
        if any(word in text_lower for word in math_words):
            return 'math'
        
        science_words = ['science', 'physics', 'chemistry', 'biology', 'experiment', 'atom', 'cell']
        if any(word in text_lower for word in science_words):
            return 'science'
        
        english_words = ['english', 'grammar', 'writing', 'reading', 'literature', 'essay', 'poem']
        if any(word in text_lower for word in english_words):
            return 'english'
        
        social_words = ['history', 'geography', 'social', 'civics', 'culture', 'society', 'government']
        if any(word in text_lower for word in social_words):
            return 'social'
        
        # Motivation keywords
        motivation_words = ['sad', 'difficult', 'hard', 'can\'t', 'impossible', 'discouraged', 'tired']
        if any(word in text_lower for word in motivation_words):
            return 'motivation'
        
        # Study tips keywords
        study_words = ['study', 'learn', 'how to', 'tips', 'method', 'technique', 'concentrate']
        if any(word in text_lower for word in study_words):
            return 'study_tips'
        
        # Exam preparation
        exam_words = ['exam', 'test', 'preparation', 'nervous', 'exam tips', 'board', 'competitive']
        if any(word in text_lower for word in exam_words):
            return 'exam_prep'
        
        return 'default'
    
    def get_response(self, user_input, language):
        """Generate response based on user input and translate if needed"""
        try:
            # Translate input to English if not in English
            if language != 'English':
                try:
                    english_input = self.translator.translate(user_input, 'English').result
                except:
                    english_input = user_input
            else:
                english_input = user_input
            
            # Get intelligent response based on content
            response = self.get_intelligent_response(english_input)
            
            # Translate response back to selected language
            if language != 'English':
                try:
                    translated_response = self.translator.translate(response, get_language_code(language)).result
                    return translated_response, response
                except Exception as e:
                    return f"{response} (Translation temporarily unavailable)", response
            else:
                return response, None
                
        except Exception as e:
            error_msg = "I'm sorry, I'm having trouble understanding right now. Please try again!"
            return error_msg, None
    
    def get_intelligent_response(self, user_input):
        """Generate intelligent responses using OpenRouter API"""
        try:
            # Try OpenRouter API first
            openrouter_response = self.get_openrouter_response(user_input)
            if openrouter_response:
                return openrouter_response
        except Exception as e:
            st.sidebar.warning("AI service temporarily unavailable, using fallback responses")
        
        # Fallback to local responses
        return self.get_local_response(user_input)
    
    def get_openrouter_response(self, user_input):
        """Get response from OpenRouter API"""
        api_key = "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"
        # Get user's class for context
        user_class = st.session_state.get('selected_class', 5)
        prompt = f"""You are Vidya Sakhi, a friendly AI tutor for Indian school students. 
        
Student's class: {user_class}
Student's question: {user_input}

Provide a helpful, educational response appropriate for class {user_class} students. 
Keep your answer:
- Simple and easy to understand
- Educational and informative
- Encouraging and supportive
- Specific to the question asked

If it's a subject question, provide clear explanations with examples."""
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are Vidya Sakhi, a helpful AI tutor for Indian school students. Always be encouraging, educational, and age-appropriate."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": 600,
                    "temperature": 0.7
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
        except Exception as e:
            pass
        return None
    
    def get_local_response(self, user_input):
        """Generate local responses as fallback"""
        text_lower = user_input.lower()
        
        # Greeting responses
        greeting_words = ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good afternoon']
        if any(word in text_lower for word in greeting_words):
            return random.choice(self.responses['greeting'])
        
        # Check for specific knowledge queries
        # Math topics
        if any(word in text_lower for word in ['addition', 'add', 'plus', 'sum']):
            return self.knowledge_base['math']['basic']['addition']
        elif any(word in text_lower for word in ['subtraction', 'subtract', 'minus', 'difference']):
            return self.knowledge_base['math']['basic']['subtraction']
        elif any(word in text_lower for word in ['multiplication', 'multiply', 'times', 'product']):
            return self.knowledge_base['math']['basic']['multiplication']
        elif any(word in text_lower for word in ['division', 'divide', 'quotient']):
            return self.knowledge_base['math']['basic']['division']
        elif any(word in text_lower for word in ['fraction', 'fractions']):
            return self.knowledge_base['math']['intermediate']['fractions']
        elif any(word in text_lower for word in ['decimal', 'decimals']):
            return self.knowledge_base['math']['intermediate']['decimals']
        elif any(word in text_lower for word in ['algebra', 'equation', 'variable']):
            return self.knowledge_base['math']['intermediate']['algebra']
        elif any(word in text_lower for word in ['geometry', 'shape', 'triangle', 'circle']):
            return self.knowledge_base['math']['intermediate']['geometry']
        elif any(word in text_lower for word in ['quadratic', 'x²', 'x square']):
            return self.knowledge_base['math']['advanced']['quadratic']
        elif any(word in text_lower for word in ['trigonometry', 'sin', 'cos', 'tan']):
            return self.knowledge_base['math']['advanced']['trigonometry']
        elif any(word in text_lower for word in ['calculus', 'derivative', 'integral']):
            return self.knowledge_base['math']['advanced']['calculus']
        
        # Science topics
        elif any(word in text_lower for word in ['plant', 'plants', 'photosynthesis']):
            return self.knowledge_base['science']['basic']['plants']
        elif any(word in text_lower for word in ['animal', 'animals']):
            return self.knowledge_base['science']['basic']['animals']
        elif any(word in text_lower for word in ['weather', 'rain', 'sun', 'wind']):
            return self.knowledge_base['science']['basic']['weather']
        elif any(word in text_lower for word in ['motion', 'speed', 'velocity']):
            return self.knowledge_base['science']['physics']['motion']
        elif any(word in text_lower for word in ['force', 'newton', 'push', 'pull']):
            return self.knowledge_base['science']['physics']['force']
        elif any(word in text_lower for word in ['energy', 'kinetic', 'potential']):
            return self.knowledge_base['science']['physics']['energy']
        elif any(word in text_lower for word in ['atom', 'atoms', 'proton', 'electron']):
            return self.knowledge_base['science']['chemistry']['atoms']
        elif any(word in text_lower for word in ['element', 'elements', 'periodic table']):
            return self.knowledge_base['science']['chemistry']['elements']
        elif any(word in text_lower for word in ['reaction', 'chemical reaction']):
            return self.knowledge_base['science']['chemistry']['reactions']
        elif any(word in text_lower for word in ['cell', 'cells', 'nucleus']):
            return self.knowledge_base['science']['biology']['cells']
        elif any(word in text_lower for word in ['dna', 'genetics', 'genes']):
            return self.knowledge_base['science']['biology']['genetics']
        elif any(word in text_lower for word in ['evolution', 'natural selection']):
            return self.knowledge_base['science']['biology']['evolution']
        
        # English topics
        elif any(word in text_lower for word in ['grammar', 'sentence', 'verb', 'noun']):
            return self.knowledge_base['english']['grammar']
        elif any(word in text_lower for word in ['vocabulary', 'words', 'meaning']):
            return self.knowledge_base['english']['vocabulary']
        elif any(word in text_lower for word in ['writing', 'essay', 'paragraph']):
            return self.knowledge_base['english']['writing']
        elif any(word in text_lower for word in ['literature', 'story', 'poem', 'novel']):
            return self.knowledge_base['english']['literature']
        
        # History topics
        elif any(word in text_lower for word in ['ancient', 'indus valley', 'mauryan']):
            return self.knowledge_base['history']['ancient']
        elif any(word in text_lower for word in ['medieval', 'mughal', 'sultanate']):
            return self.knowledge_base['history']['medieval']
        elif any(word in text_lower for word in ['modern', 'independence', 'freedom']):
            return self.knowledge_base['history']['modern']
        
        # Geography topics
        elif any(word in text_lower for word in ['earth', 'continent', 'ocean']):
            return self.knowledge_base['geography']['earth']
        elif any(word in text_lower for word in ['climate', 'tropical', 'polar']):
            return self.knowledge_base['geography']['climate']
        elif any(word in text_lower for word in ['resources', 'natural resources', 'minerals']):
            return self.knowledge_base['geography']['resources']
        
        # Study and motivation
        elif any(word in text_lower for word in ['study', 'learn', 'tips', 'how to study']):
            return random.choice(self.responses['study_tips'])
        elif any(word in text_lower for word in ['exam', 'test', 'preparation']):
            return random.choice(self.responses['exam_prep'])
        elif any(word in text_lower for word in ['sad', 'difficult', 'hard', 'can\'t']):
            return random.choice(self.responses['motivation'])
        
        # General math/science catch-all
        elif any(word in text_lower for word in ['math', 'mathematics', 'calculation']):
            return "Mathematics is a beautiful subject! I can help you with addition, subtraction, multiplication, division, fractions, algebra, geometry, and more. What specific topic would you like to learn about?"
        elif any(word in text_lower for word in ['science', 'physics', 'chemistry', 'biology']):
            return "Science is fascinating! I can explain concepts in physics (motion, force, energy), chemistry (atoms, elements, reactions), and biology (cells, genetics, evolution). What interests you?"
        elif any(word in text_lower for word in ['english', 'language']):
            return "English is a wonderful language! I can help with grammar, vocabulary, writing skills, and literature. What would you like to improve?"
        elif any(word in text_lower for word in ['history', 'past', 'ancient', 'old']):
            return "History teaches us about our past! I can tell you about ancient civilizations, medieval period, modern India, and world history. What period interests you?"
        elif any(word in text_lower for word in ['geography', 'earth', 'map', 'country']):
            return "Geography helps us understand our world! I can explain about Earth, climate, countries, natural resources, and more. What would you like to explore?"
        
        # Default intelligent response
        else:
            return f"That's a great question about '{user_input}'! I'm here to help you learn. Could you be more specific about what aspect you'd like to understand? I can help with math, science, English, history, geography, and study tips!"
    
    def speak_text(self, text, language):
        """Convert text to speech using gTTS only (for browser compatibility)"""
        if not st.session_state.voice_enabled:
            return
        try:
            lang_code = get_language_code(language)
            if lang_code == 'unknown':
                lang_code = 'en'
            tts = gTTS(text=text, lang=lang_code, slow=False)
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                try:
                    with open(tmp_file.name, 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                except Exception as e:
                    try:
                        pygame.mixer.music.load(tmp_file.name)
                        pygame.mixer.music.play()
                        import time
                        time.sleep(0.5)
                    except:
                        pass
                import os
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
        except Exception as e:
            st.sidebar.warning("Voice output temporarily unavailable")
