import random
import streamlit as st
from translatepy import Translate
from gtts import gTTS
import pygame
import io
import tempfile
import os
from utils import get_language_code

class ChatBot:
    def __init__(self):
        self.translator = Translate()
        self.responses = {
            'greeting': [
                "Hello! I'm Vidya Sakhi, your learning companion. How can I help you today?",
                "Hi there! Ready to learn something new today?",
                "Namaste! I'm here to help you with your studies. What would you like to know?"
            ],
            'math': [
                "Math is like a puzzle - once you understand the pattern, it becomes fun! What specific topic do you need help with?",
                "Mathematics is the language of the universe. Let's solve some problems together!",
                "Don't worry about math - practice makes perfect! Which concept would you like me to explain?"
            ],
            'science': [
                "Science is all around us! From the air we breathe to the stars we see. What scientific concept interests you?",
                "Every great scientist started with curiosity. What would you like to explore today?",
                "Science helps us understand our amazing world. Which subject - Physics, Chemistry, or Biology?"
            ],
            'english': [
                "English opens doors to the world! Whether it's grammar, literature, or writing, I'm here to help.",
                "Reading and writing are superpowers! What aspect of English would you like to improve?",
                "English is a beautiful language. Let's work on your vocabulary, grammar, or comprehension!"
            ],
            'social': [
                "History and geography tell the story of our world. What period or place interests you?",
                "Understanding our society and culture makes us better citizens. What topic shall we explore?",
                "From ancient civilizations to modern times, there's so much to learn! What's your question?"
            ],
            'motivation': [
                "You're doing great! Every small step in learning is a big achievement.",
                "Remember, even the greatest scholars started as beginners. Keep going!",
                "Learning is a journey, not a destination. I'm proud of your curiosity!",
                "Mistakes are proof that you're trying. Every error is a step closer to success!"
            ],
            'study_tips': [
                "Here are some study tips: 1) Take regular breaks 2) Make notes 3) Practice daily 4) Ask questions!",
                "Study smart, not just hard! Try the Pomodoro technique - 25 minutes study, 5 minutes break.",
                "Create a study schedule, find a quiet place, and remember to stay hydrated while studying!"
            ],
            'exam_prep': [
                "Exam preparation tips: Review regularly, solve previous papers, get enough sleep, and stay positive!",
                "For exams: Make a timetable, focus on weak areas, take mock tests, and believe in yourself!",
                "Don't stress about exams. Prepare well, eat healthy, and remember - you've got this!"
            ],
            'default': [
                "That's an interesting question! While I may not have all the answers, I encourage you to explore and learn more.",
                "Great question! This is exactly the kind of curiosity that leads to great discoveries.",
                "I love your enthusiasm for learning! Let's think about this together.",
                "That's a thoughtful question. What do you think might be the answer?"
            ]
        }
        
        # Initialize pygame mixer for audio
        try:
            pygame.mixer.init()
        except:
            pass
    
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
            
            # Categorize and get response
            category = self.categorize_input(english_input)
            response = random.choice(self.responses[category])
            
            # Translate response back to selected language
            if language != 'English':
                try:
                    translated_response = self.translator.translate(response, get_language_code(language)).result
                    return translated_response, response
                except Exception as e:
                    # Fallback: return English response with error note
                    return f"{response} (Translation temporarily unavailable)", response
            else:
                return response, None
                
        except Exception as e:
            error_msg = "I'm sorry, I'm having trouble understanding right now. Please try again!"
            return error_msg, None
    
    def speak_text(self, text, language):
        """Convert text to speech using gTTS"""
        if not st.session_state.voice_enabled:
            return
            
        try:
            # Get language code for gTTS
            lang_code = get_language_code(language)
            if lang_code == 'unknown':
                lang_code = 'en'
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Play audio using pygame
                try:
                    pygame.mixer.music.load(tmp_file.name)
                    pygame.mixer.music.play()
                except:
                    pass
                
                # Clean up
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
                    
        except Exception as e:
            # Silently fail for voice output
            pass
