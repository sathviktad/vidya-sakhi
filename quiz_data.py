import random
from translatepy import Translate
from utils import get_language_code
from googletrans import Translator

class QuizModule:
    def __init__(self):
        self.translator = Translate()
        self.google_translator = Translator()
        self.load_questions_from_file()
    
    def load_questions_from_file(self):
        """Load questions from JSON file, create default if doesn't exist"""
        try:
            import json
            with open('quiz_questions.json', 'r', encoding='utf-8') as f:
                self.questions_db = json.load(f)
        except FileNotFoundError:
            self.create_default_questions()
            self.save_questions_to_file()
    
    def save_questions_to_file(self):
        """Save questions to JSON file"""
        import json
        with open('quiz_questions.json', 'w', encoding='utf-8') as f:
            json.dump(self.questions_db, f, ensure_ascii=False, indent=2)
    
    def add_question(self, class_num, subject, question_data):
        """Add a new question to the database"""
        class_key = f"class_{class_num}"
        if class_key not in self.questions_db:
            self.questions_db[class_key] = {}
        if subject not in self.questions_db[class_key]:
            self.questions_db[class_key][subject] = []
        
        self.questions_db[class_key][subject].append(question_data)
        self.save_questions_to_file()
        return True
    
    def create_default_questions(self):
        self.questions_data = {}
        for class_num in range(3, 9):
            self.questions_data[class_num] = {}
            # Math
            self.questions_data[class_num]['Math'] = [
                {'question': f'What is {a} + {b}?', 'options': [str(a+b), str(a+b+1), str(a+b-1), str(a+b+2)], 'correct_answer': str(a+b)}
                for a, b in zip(range(1+class_num, 16+class_num), range(2, 17+class_num))
            ][:10] + [
                {'question': f'What is {a} × {b}?', 'options': [str(a*b), str(a*b+1), str(a*b-1), str(a*b+2)], 'correct_answer': str(a*b)}
                for a, b in zip(range(2+class_num, 12+class_num), range(2, 12+class_num))
            ][:10] + [
                {'question': f'What is {a} - {b}?', 'options': [str(a-b), str(a-b+1), str(a-b-1), str(a-b+2)], 'correct_answer': str(a-b)}
                for a, b in zip(range(20+class_num, 30+class_num), range(1, 11))
            ][:10]
            # Science
            self.questions_data[class_num]['Science'] = [
                {'question': q, 'options': opts, 'correct_answer': ans} for q, opts, ans in [
                    ("What is the boiling point of water?", ["100°C", "0°C", "50°C", "25°C"], "100°C"),
                    ("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Saturn"], "Mars"),
                    ("What gas do plants absorb?", ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"], "Carbon dioxide"),
                    ("Which organ pumps blood?", ["Heart", "Liver", "Lungs", "Kidney"], "Heart"),
                    ("What is H2O?", ["Water", "Oxygen", "Hydrogen", "Salt"], "Water"),
                    ("Which is a mammal?", ["Whale", "Shark", "Octopus", "Starfish"], "Whale"),
                    ("What is the largest organ in the human body?", ["Skin", "Liver", "Heart", "Brain"], "Skin"),
                    ("What do bees make?", ["Honey", "Milk", "Wax", "Oil"], "Honey"),
                    ("Which vitamin do we get from sunlight?", ["Vitamin D", "Vitamin A", "Vitamin C", "Vitamin B"], "Vitamin D"),
                    ("What is the process of plants making food?", ["Photosynthesis", "Respiration", "Digestion", "Transpiration"], "Photosynthesis"),
                    ("Which animal lays eggs?", ["Duck", "Dog", "Cow", "Cat"], "Duck"),
                    ("What is the center of an atom called?", ["Nucleus", "Electron", "Proton", "Neutron"], "Nucleus"),
                    ("Which is a renewable resource?", ["Solar energy", "Coal", "Petrol", "Diesel"], "Solar energy"),
                    ("What is the hardest natural substance?", ["Diamond", "Gold", "Iron", "Silver"], "Diamond"),
                    ("Which is a reptile?", ["Snake", "Frog", "Fish", "Bird"], "Snake"),
                    ("What is the main source of energy for Earth?", ["Sun", "Moon", "Stars", "Wind"], "Sun"),
                    ("Which part of the plant conducts photosynthesis?", ["Leaf", "Root", "Stem", "Flower"], "Leaf"),
                    ("What is the largest planet?", ["Jupiter", "Earth", "Mars", "Venus"], "Jupiter"),
                    ("Which is not a sense organ?", ["Hair", "Eye", "Ear", "Nose"], "Hair"),
                    ("What is the freezing point of water?", ["0°C", "100°C", "50°C", "-10°C"], "0°C"),
                    ("Which is a herbivore?", ["Cow", "Tiger", "Lion", "Wolf"], "Cow"),
                    ("What is the function of roots?", ["Absorb water", "Make food", "Breathe", "Reproduce"], "Absorb water"),
                    ("Which is a non-metal?", ["Oxygen", "Iron", "Copper", "Gold"], "Oxygen"),
                    ("What is the smallest unit of life?", ["Cell", "Tissue", "Organ", "Organism"], "Cell"),
                    ("Which is a vertebrate?", ["Fish", "Worm", "Snail", "Jellyfish"], "Fish"),
                    ("What is the main gas in air?", ["Nitrogen", "Oxygen", "Carbon dioxide", "Hydrogen"], "Nitrogen"),
                    ("Which is a solid?", ["Ice", "Water", "Steam", "Air"], "Ice"),
                    ("What is the color of chlorophyll?", ["Green", "Red", "Blue", "Yellow"], "Green"),
                    ("Which is a carnivore?", ["Lion", "Cow", "Goat", "Sheep"], "Lion"),
                    ("What is the main function of leaves?", ["Make food", "Absorb water", "Support plant", "Store food"], "Make food")
                ]]
            # ... Repeat for all other subjects, with 30 unique, real, and increasing-difficulty questions per class ...
        # (Leave classes 9-12 as is)
        # Save to self.questions_db
        self.questions_db = {}
        for class_num, subjects in self.questions_data.items():
            class_key = f'class_{class_num}'
            self.questions_db[class_key] = {}
            for subject, questions in subjects.items():
                self.questions_db[class_key][subject] = questions
        self.save_questions_to_file()
    
    def get_subjects_for_class(self, class_num):
        """Get available subjects for a given class, dynamically from loaded questions"""
        class_key = f'class_{class_num}'
        if hasattr(self, 'questions_db') and class_key in self.questions_db:
            return list(self.questions_db[class_key].keys())
        # fallback to previous logic if not loaded
        base_subjects = ['Math', 'Science', 'English', 'Hindi', 'GK', 'Computers', 'Sports', 'Value Education']
        if class_num <= 5:
            return base_subjects + ['Telugu']
        elif class_num <= 7:
            return ['Math', 'Science', 'English', 'Social', 'Hindi', 'Telugu', 'GK', 'Computers']
        elif class_num <= 8:
            return ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics']
        elif class_num <= 10:
            return ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics']
        else:
            return ['Physics', 'Chemistry', 'Math', 'Biology', 'English']
    
    def translate_text(self, text, lang_code):
        print(f"Translating: '{text}' to '{lang_code}'")
        try:
            result = self.translator.translate(text, lang_code).result
            print(f"translatepy result: {result}")
            if result and result != text:
                return result
        except Exception as e:
            print(f"translatepy error: {e}")
        try:
            result = self.google_translator.translate(text, dest=lang_code).text
            print(f"googletrans result: {result}")
            return result
        except Exception as e:
            print(f"googletrans error: {e}")
        return text
    
    def generate_quiz(self, class_num, subject, num_questions, language):
        """Generate quiz questions for given parameters"""
        try:
            class_key = f"class_{class_num}"
            class_questions = self.questions_db.get(class_key, {})
            if not class_questions:
                available_classes = sorted(self.questions_db.keys())
                if class_num <= 5:
                    nearest_class = "class_3"
                elif class_num <= 8:
                    nearest_class = "class_6"
                elif class_num <= 10:
                    nearest_class = "class_9"
                else:
                    nearest_class = "class_11"
                class_questions = self.questions_db.get(nearest_class, {})
            subject_questions = class_questions.get(subject, [])
            if not subject_questions:
                for available_subject in class_questions.keys():
                    if subject.lower() in available_subject.lower() or available_subject.lower() in subject.lower():
                        subject_questions = class_questions[available_subject]
                        break
            if not subject_questions:
                return []
            selected_questions = random.sample(
                subject_questions, 
                min(num_questions, len(subject_questions))
            )
            output_questions = []
            lang_code = get_language_code(language)
            for q in selected_questions:
                # For English, Hindi, and Telugu subjects, always use original
                if subject.lower() in ['english', 'hindi', 'telugu']:
                    question_text = q['question']
                    options = q['options']
                    explanation = q.get('explanation', '')
                elif lang_code == 'en':
                    question_text = q['question']
                    options = q['options']
                    explanation = q.get('explanation', '')
                else:
                    question_text = self.translate_text(q['question'], lang_code)
                    options = [self.translate_text(opt, lang_code) for opt in q['options']]
                    explanation = self.translate_text(q.get('explanation', ''), lang_code)
                random.shuffle(options)
                correct_answer = q['correct_answer']
                # Try to match the correct answer in the translated options
                try:
                    idx = q['options'].index(correct_answer)
                    correct_answer_translated = options[idx] if idx < len(options) else options[0]
                except Exception:
                    correct_answer_translated = correct_answer
                output_questions.append({
                    'question': question_text,
                    'options': options,
                    'correct_answer': correct_answer_translated,
                    'explanation': explanation
                })
            return output_questions
        except Exception as e:
            print(f"[QUIZ GENERATE ERROR] {e}")
            return []
    
    def translate_question(self, question, target_language):
        """Translate a question to target language"""
        try:
            lang_code = get_language_code(target_language)
            if lang_code == 'unknown':
                return question
            
            translated_question = {
                'question': self.translator.translate(question['question'], lang_code).result,
                'options': [self.translator.translate(opt, lang_code).result for opt in question['options']],
                'correct_answer': self.translator.translate(question['correct_answer'], lang_code).result
            }
            return translated_question
            
        except Exception as e:
            # Fallback to original question
            return question
