import random
from translatepy import Translate
from utils import get_language_code

class QuizModule:
    def __init__(self):
        self.translator = Translate()
        self.questions_data = {
            # Class 3-5 Questions (Basic Level)
            3: {
                'Math': [
                    {
                        'question': 'What is 5 + 3?',
                        'options': ['6', '7', '8', '9'],
                        'correct_answer': '8'
                    },
                    {
                        'question': 'How many sides does a triangle have?',
                        'options': ['2', '3', '4', '5'],
                        'correct_answer': '3'
                    },
                    {
                        'question': 'What is 10 - 4?',
                        'options': ['5', '6', '7', '8'],
                        'correct_answer': '6'
                    },
                    {
                        'question': 'Which number comes after 19?',
                        'options': ['18', '20', '21', '22'],
                        'correct_answer': '20'
                    },
                    {
                        'question': 'What is 2 × 4?',
                        'options': ['6', '7', '8', '9'],
                        'correct_answer': '8'
                    },
                    {
                        'question': 'Which is the smallest number?',
                        'options': ['5', '2', '8', '6'],
                        'correct_answer': '2'
                    },
                    {
                        'question': 'How many days are there in a week?',
                        'options': ['5', '6', '7', '8'],
                        'correct_answer': '7'
                    },
                    {
                        'question': 'What is 15 - 10?',
                        'options': ['3', '4', '5', '6'],
                        'correct_answer': '5'
                    }
                ],
                'Science': [
                    {
                        'question': 'Which planet do we live on?',
                        'options': ['Mars', 'Venus', 'Earth', 'Jupiter'],
                        'correct_answer': 'Earth'
                    },
                    {
                        'question': 'How many legs does a spider have?',
                        'options': ['6', '8', '10', '12'],
                        'correct_answer': '8'
                    },
                    {
                        'question': 'What do plants need to grow?',
                        'options': ['Only water', 'Only sunlight', 'Water and sunlight', 'Only soil'],
                        'correct_answer': 'Water and sunlight'
                    }
                ],
                'English': [
                    {
                        'question': 'How many letters are in the English alphabet?',
                        'options': ['24', '25', '26', '27'],
                        'correct_answer': '26'
                    },
                    {
                        'question': 'What is the opposite of "hot"?',
                        'options': ['Warm', 'Cool', 'Cold', 'Mild'],
                        'correct_answer': 'Cold'
                    }
                ]
            },
            
            # Class 6-8 Questions
            6: {
                'Math': [
                    {
                        'question': 'What is the LCM of 12 and 18?',
                        'options': ['24', '36', '48', '54'],
                        'correct_answer': '36'
                    },
                    {
                        'question': 'If x + 5 = 12, what is x?',
                        'options': ['5', '6', '7', '8'],
                        'correct_answer': '7'
                    },
                    {
                        'question': 'What is the area of a rectangle with length 8 and width 6?',
                        'options': ['14', '28', '48', '56'],
                        'correct_answer': '48'
                    }
                ],
                'Science': [
                    {
                        'question': 'What is the chemical formula for water?',
                        'options': ['H2O', 'CO2', 'NaCl', 'CH4'],
                        'correct_answer': 'H2O'
                    },
                    {
                        'question': 'Which organ pumps blood in the human body?',
                        'options': ['Brain', 'Lungs', 'Heart', 'Liver'],
                        'correct_answer': 'Heart'
                    }
                ],
                'History': [
                    {
                        'question': 'Who was the first Prime Minister of India?',
                        'options': ['Mahatma Gandhi', 'Jawaharlal Nehru', 'Sardar Patel', 'Dr. Rajendra Prasad'],
                        'correct_answer': 'Jawaharlal Nehru'
                    }
                ],
                'Geography': [
                    {
                        'question': 'Which is the largest continent?',
                        'options': ['Africa', 'Asia', 'Europe', 'North America'],
                        'correct_answer': 'Asia'
                    }
                ]
            },
            
            # Class 9-10 Questions (Board Level)
            9: {
                'Math': [
                    {
                        'question': 'If the roots of equation ax² + bx + c = 0 are real and equal, then:',
                        'options': ['b² - 4ac > 0', 'b² - 4ac = 0', 'b² - 4ac < 0', 'None of these'],
                        'correct_answer': 'b² - 4ac = 0'
                    },
                    {
                        'question': 'The value of sin²θ + cos²θ is:',
                        'options': ['0', '1', '2', 'θ'],
                        'correct_answer': '1'
                    }
                ],
                'Physics': [
                    {
                        'question': 'The SI unit of force is:',
                        'options': ['Joule', 'Newton', 'Watt', 'Pascal'],
                        'correct_answer': 'Newton'
                    },
                    {
                        'question': 'Light travels fastest in:',
                        'options': ['Air', 'Water', 'Glass', 'Vacuum'],
                        'correct_answer': 'Vacuum'
                    }
                ],
                'Chemistry': [
                    {
                        'question': 'The atomic number of carbon is:',
                        'options': ['4', '6', '8', '12'],
                        'correct_answer': '6'
                    }
                ],
                'Biology': [
                    {
                        'question': 'Photosynthesis takes place in:',
                        'options': ['Roots', 'Stem', 'Leaves', 'Flowers'],
                        'correct_answer': 'Leaves'
                    }
                ]
            },
            
            # Class 11-12 Questions (Competitive Level)
            11: {
                'Physics': [
                    {
                        'question': 'The dimensional formula for impulse is:',
                        'options': ['[MLT⁻¹]', '[MLT⁻²]', '[ML²T⁻²]', '[MLT⁻³]'],
                        'correct_answer': '[MLT⁻¹]'
                    },
                    {
                        'question': 'In Young\'s double slit experiment, the fringe width is:',
                        'options': ['λD/d', 'λd/D', 'D/λd', 'λ/Dd'],
                        'correct_answer': 'λD/d'
                    },
                    {
                        'question': 'A particle undergoes SHM with amplitude A. At what displacement is the kinetic energy equal to potential energy?',
                        'options': ['A/2', 'A/√2', 'A/√3', 'A/4'],
                        'correct_answer': 'A/√2'
                    },
                    {
                        'question': 'The work function of a metal is 2.5 eV. What is the threshold frequency?',
                        'options': ['6.0 × 10¹⁴ Hz', '4.8 × 10¹⁴ Hz', '3.6 × 10¹⁴ Hz', '7.2 × 10¹⁴ Hz'],
                        'correct_answer': '6.0 × 10¹⁴ Hz'
                    },
                    {
                        'question': 'For a conducting sphere of radius R carrying charge Q, the electric field inside is:',
                        'options': ['kQ/R²', 'kQ/r²', '0', 'kQ/(4πR²)'],
                        'correct_answer': '0'
                    },
                    {
                        'question': 'The coefficient of restitution for a perfectly elastic collision is:',
                        'options': ['0', '1', '-1', '∞'],
                        'correct_answer': '1'
                    },
                    {
                        'question': 'In a uniform magnetic field, a charged particle moves in a circular path. The radius depends on:',
                        'options': ['velocity only', 'mass only', 'charge only', 'momentum'],
                        'correct_answer': 'momentum'
                    },
                    {
                        'question': 'The ratio of speeds of sound in hydrogen and oxygen at same temperature is:',
                        'options': ['4:1', '1:4', '2:1', '1:2'],
                        'correct_answer': '4:1'
                    }
                ],
                'Chemistry': [
                    {
                        'question': 'Which of the following has maximum ionic character?',
                        'options': ['NaCl', 'MgO', 'AlF₃', 'CaF₂'],
                        'correct_answer': 'MgO'
                    },
                    {
                        'question': 'The hybridization of carbon in diamond is:',
                        'options': ['sp', 'sp²', 'sp³', 'sp³d'],
                        'correct_answer': 'sp³'
                    },
                    {
                        'question': 'For the reaction A + B → C, if concentration of A is doubled and B is tripled, the rate increases 12 times. The order with respect to A is:',
                        'options': ['1', '2', '3', '0'],
                        'correct_answer': '2'
                    },
                    {
                        'question': 'The entropy change for an adiabatic reversible process is:',
                        'options': ['Positive', 'Negative', 'Zero', 'Infinite'],
                        'correct_answer': 'Zero'
                    },
                    {
                        'question': 'In SN2 mechanism, the stereochemistry is:',
                        'options': ['Retention', 'Inversion', 'Racemization', 'No change'],
                        'correct_answer': 'Inversion'
                    },
                    {
                        'question': 'The number of unpaired electrons in Fe³⁺ (Z=26) is:',
                        'options': ['3', '4', '5', '6'],
                        'correct_answer': '5'
                    },
                    {
                        'question': 'Which quantum number determines the shape of orbital?',
                        'options': ['n', 'l', 'm', 's'],
                        'correct_answer': 'l'
                    },
                    {
                        'question': 'The pH of 0.1 M CH₃COOH (Ka = 1.8 × 10⁻⁵) is approximately:',
                        'options': ['1', '2.9', '4.8', '7'],
                        'correct_answer': '2.9'
                    }
                ],
                'Math': [
                    {
                        'question': 'The derivative of x^x is:',
                        'options': ['x^x(1 + ln x)', 'x^(x-1)', 'x^x ln x', 'x^x'],
                        'correct_answer': 'x^x(1 + ln x)'
                    },
                    {
                        'question': 'If |z| = 1, then |z + 1/z| equals:',
                        'options': ['1', '2', '2|Re(z)|', '2|Im(z)|'],
                        'correct_answer': '2|Re(z)|'
                    }
                ],
                'Biology': [
                    {
                        'question': 'Which enzyme is responsible for DNA replication?',
                        'options': ['DNA ligase', 'DNA polymerase', 'Helicase', 'Primase'],
                        'correct_answer': 'DNA polymerase'
                    }
                ]
            }
        }
    
    def get_subjects_for_class(self, class_num):
        """Get available subjects for a given class"""
        base_subjects = ['Math', 'Science', 'English', 'GK', 'Computers', 'Sports', 'Value Education']
        
        if class_num <= 5:
            return base_subjects + ['Regional Language']
        elif class_num <= 7:
            return ['Math', 'Science', 'English', 'Social', 'Hindi', 'GK', 'Computers']
        elif class_num <= 8:
            return ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Geography', 'Civics']
        elif class_num <= 10:
            return ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Geography', 'Civics']
        else:  # Class 11-12
            return ['Physics', 'Chemistry', 'Math', 'Biology', 'English']
    
    def generate_quiz(self, class_num, subject, num_questions, language):
        """Generate quiz questions for given parameters"""
        try:
            # Get questions for the class
            class_questions = self.questions_data.get(class_num, {})
            
            # If exact class not found, find nearest available class
            if not class_questions:
                available_classes = sorted(self.questions_data.keys())
                nearest_class = min(available_classes, key=lambda x: abs(x - class_num))
                class_questions = self.questions_data[nearest_class]
            
            # Get subject questions
            subject_questions = class_questions.get(subject, [])
            
            if not subject_questions:
                # Try to find similar subject
                for available_subject in class_questions.keys():
                    if subject.lower() in available_subject.lower() or available_subject.lower() in subject.lower():
                        subject_questions = class_questions[available_subject]
                        break
            
            if not subject_questions:
                return []
            
            # Select random questions
            selected_questions = random.sample(
                subject_questions, 
                min(num_questions, len(subject_questions))
            )
            
            # Translate questions if needed
            if language != 'English':
                translated_questions = []
                for question in selected_questions:
                    translated_q = self.translate_question(question, language)
                    translated_questions.append(translated_q)
                return translated_questions
            
            return selected_questions
            
        except Exception as e:
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
