import random
from translatepy import Translate
from utils import get_language_code

class QuizModule:
    def __init__(self):
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
        self.translator = Translate()
        self.questions_data = {
            # Copy data for classes 4 and 5 (same as class 3 with slight variations)
            4: {
                'Math': [
                    {
                        'question': 'What is 7 + 6?',
                        'options': ['12', '13', '14', '15'],
                        'correct_answer': '13'
                    },
                    {
                        'question': 'How many sides does a rectangle have?',
                        'options': ['3', '4', '5', '6'],
                        'correct_answer': '4'
                    },
                    {
                        'question': 'What is 16 - 8?',
                        'options': ['6', '7', '8', '9'],
                        'correct_answer': '8'
                    },
                    {
                        'question': 'What is 3 × 5?',
                        'options': ['12', '15', '18', '20'],
                        'correct_answer': '15'
                    }
                ],
                'Science': [
                    {
                        'question': 'What do we get from bees?',
                        'options': ['Milk', 'Honey', 'Eggs', 'Wool'],
                        'correct_answer': 'Honey'
                    },
                    {
                        'question': 'Which sense organ do we use to see?',
                        'options': ['Nose', 'Ears', 'Eyes', 'Tongue'],
                        'correct_answer': 'Eyes'
                    }
                ],
                'English': [
                    {
                        'question': 'What is the first letter of the alphabet?',
                        'options': ['B', 'A', 'C', 'D'],
                        'correct_answer': 'A'
                    },
                    {
                        'question': 'Which is a vowel?',
                        'options': ['B', 'C', 'E', 'F'],
                        'correct_answer': 'E'
                    }
                ]
            },
            5: {
                'Math': [
                    {
                        'question': 'What is 12 ÷ 3?',
                        'options': ['3', '4', '5', '6'],
                        'correct_answer': '4'
                    },
                    {
                        'question': 'How many minutes are in one hour?',
                        'options': ['50', '60', '70', '80'],
                        'correct_answer': '60'
                    },
                    {
                        'question': 'What is 9 × 6?',
                        'options': ['52', '54', '56', '58'],
                        'correct_answer': '54'
                    },
                    {
                        'question': 'What is 144 ÷ 12?',
                        'options': ['11', '12', '13', '14'],
                        'correct_answer': '12'
                    },
                    {
                        'question': 'How many sides does a pentagon have?',
                        'options': ['4', '5', '6', '7'],
                        'correct_answer': '5'
                    }
                ],
                'Science': [
                    {
                        'question': 'What is the hardest natural substance?',
                        'options': ['Gold', 'Iron', 'Diamond', 'Silver'],
                        'correct_answer': 'Diamond'
                    },
                    {
                        'question': 'Which gas do we breathe in?',
                        'options': ['Carbon dioxide', 'Oxygen', 'Nitrogen', 'Hydrogen'],
                        'correct_answer': 'Oxygen'
                    }
                ],
                'English': [
                    {
                        'question': 'What is the past tense of "go"?',
                        'options': ['Goed', 'Gone', 'Went', 'Going'],
                        'correct_answer': 'Went'
                    },
                    {
                        'question': 'What is a synonym for "big"?',
                        'options': ['Small', 'Large', 'Tiny', 'Little'],
                        'correct_answer': 'Large'
                    },
                    {
                        'question': 'Which is a complete sentence?',
                        'options': ['Running fast', 'The dog barks', 'Very happy', 'In the garden'],
                        'correct_answer': 'The dog barks'
                    }
                ],
                'Telugu': [
                    {
                        'question': 'తెలుగు లో "నమస్కారం" అర్థం ఏమిటి?',
                        'options': ['వెళ్ళిపో', 'రండి', 'హలో', 'బాయ్'],
                        'correct_answer': 'హలో'
                    }
                ]
            },
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
                    },
                    {
                        'question': 'Which animal gives us milk?',
                        'options': ['Dog', 'Cat', 'Cow', 'Lion'],
                        'correct_answer': 'Cow'
                    },
                    {
                        'question': 'How many seasons are there in a year?',
                        'options': ['2', '3', '4', '5'],
                        'correct_answer': '4'
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
                    },
                    {
                        'question': 'Which word rhymes with "cat"?',
                        'options': ['Dog', 'Hat', 'Run', 'Sun'],
                        'correct_answer': 'Hat'
                    },
                    {
                        'question': 'What comes after the letter M?',
                        'options': ['L', 'N', 'O', 'P'],
                        'correct_answer': 'N'
                    }
                ],
                'GK': [
                    {
                        'question': 'Who is known as the Father of our Nation?',
                        'options': ['Nehru', 'Gandhi', 'Patel', 'Bose'],
                        'correct_answer': 'Gandhi'
                    },
                    {
                        'question': 'What is the national bird of India?',
                        'options': ['Crow', 'Peacock', 'Eagle', 'Parrot'],
                        'correct_answer': 'Peacock'
                    },
                    {
                        'question': 'How many colors are in the Indian flag?',
                        'options': ['2', '3', '4', '5'],
                        'correct_answer': '3'
                    }
                ],
                'Telugu': [
                    {
                        'question': 'తెలుగు భాషలో అక్షరాలు ఎన్ని?',
                        'options': ['50', '52', '56', '60'],
                        'correct_answer': '56'
                    },
                    {
                        'question': 'తెలుగు రాష్ట్రం ఏది?',
                        'options': ['కర్ణాటక', 'తమిళనాడు', 'తెలంగాణ', 'కేరళ'],
                        'correct_answer': 'తెలంగాణ'
                    },
                    {
                        'question': 'కవిసమ్రాట్ అని పిలువబడేవారు?',
                        'options': ['విశ్వనాథ', 'తిక్కన', 'నన్నయ', 'ఎర్రన'],
                        'correct_answer': 'విశ్వనాథ'
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
                    },
                    {
                        'question': 'What is 3/4 + 1/4?',
                        'options': ['4/8', '1', '4/4', '2/4'],
                        'correct_answer': '1'
                    },
                    {
                        'question': 'Find the perimeter of a square with side 5 cm',
                        'options': ['15 cm', '20 cm', '25 cm', '10 cm'],
                        'correct_answer': '20 cm'
                    },
                    {
                        'question': 'What is the HCF of 24 and 36?',
                        'options': ['6', '8', '12', '18'],
                        'correct_answer': '12'
                    },
                    {
                        'question': 'If a = 3 and b = 4, what is a² + b²?',
                        'options': ['25', '49', '16', '9'],
                        'correct_answer': '25'
                    },
                    {
                        'question': 'What is 0.25 as a fraction?',
                        'options': ['1/2', '1/4', '1/3', '1/5'],
                        'correct_answer': '1/4'
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
                    },
                    {
                        'question': 'What gas do plants release during photosynthesis?',
                        'options': ['Carbon dioxide', 'Oxygen', 'Nitrogen', 'Hydrogen'],
                        'correct_answer': 'Oxygen'
                    },
                    {
                        'question': 'Which planet is known as the Red Planet?',
                        'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                        'correct_answer': 'Mars'
                    },
                    {
                        'question': 'What is the boiling point of water?',
                        'options': ['90°C', '100°C', '110°C', '120°C'],
                        'correct_answer': '100°C'
                    },
                    {
                        'question': 'Which gas is most abundant in Earth\'s atmosphere?',
                        'options': ['Oxygen', 'Carbon dioxide', 'Nitrogen', 'Hydrogen'],
                        'correct_answer': 'Nitrogen'
                    },
                    {
                        'question': 'What is the smallest unit of matter?',
                        'options': ['Molecule', 'Atom', 'Cell', 'Electron'],
                        'correct_answer': 'Atom'
                    }
                ],
                'English': [
                    {
                        'question': 'What is the plural of "child"?',
                        'options': ['Childs', 'Children', 'Childes', 'Childern'],
                        'correct_answer': 'Children'
                    },
                    {
                        'question': 'Which is a proper noun?',
                        'options': ['city', 'Delhi', 'book', 'tree'],
                        'correct_answer': 'Delhi'
                    },
                    {
                        'question': 'What type of word is "quickly"?',
                        'options': ['Noun', 'Verb', 'Adjective', 'Adverb'],
                        'correct_answer': 'Adverb'
                    },
                    {
                        'question': 'What is the superlative form of "good"?',
                        'options': ['Gooder', 'Goodest', 'Better', 'Best'],
                        'correct_answer': 'Best'
                    },
                    {
                        'question': 'Which sentence is in passive voice?',
                        'options': ['I wrote a letter', 'The letter was written by me', 'I am writing', 'I will write'],
                        'correct_answer': 'The letter was written by me'
                    }
                ],
                'Hindi': [
                    {
                        'question': 'कौन सा वर्ण स्वर है?',
                        'options': ['क', 'अ', 'च', 'म'],
                        'correct_answer': 'अ'
                    },
                    {
                        'question': 'राम का विलोम शब्द क्या है?',
                        'options': ['श्याम', 'कृष्ण', 'रावण', 'हनुमान'],
                        'correct_answer': 'रावण'
                    },
                    {
                        'question': 'हिंदी में कितने वर्ण होते हैं?',
                        'options': ['44', '46', '48', '52'],
                        'correct_answer': '52'
                    }
                ],
                'Telugu': [
                    {
                        'question': 'తెలుగు భాష దేనిని కూడా పిలుస्तారు?',
                        'options': ['దక्षिణ గंగ', 'తెనुగు', 'आंధ्র भाषा', 'सभी सही हैं'],
                        'correct_answer': 'సभी సही हैं'
                    }
                ],
                'History': [
                    {
                        'question': 'Who was the first Prime Minister of India?',
                        'options': ['Mahatma Gandhi', 'Jawaharlal Nehru', 'Sardar Patel', 'Dr. Rajendra Prasad'],
                        'correct_answer': 'Jawaharlal Nehru'
                    },
                    {
                        'question': 'In which year did India gain independence?',
                        'options': ['1945', '1946', '1947', '1948'],
                        'correct_answer': '1947'
                    }
                ],
                'Geography': [
                    {
                        'question': 'Which is the largest continent?',
                        'options': ['Africa', 'Asia', 'Europe', 'North America'],
                        'correct_answer': 'Asia'
                    },
                    {
                        'question': 'Which river is known as the Ganga of South India?',
                        'options': ['Krishna', 'Godavari', 'Kaveri', 'Narmada'],
                        'correct_answer': 'Godavari'
                    }
                ],
                'Civics': [
                    {
                        'question': 'How many fundamental rights are there in Indian Constitution?',
                        'options': ['5', '6', '7', '8'],
                        'correct_answer': '6'
                    },
                    {
                        'question': 'Who is the head of the state government?',
                        'options': ['Governor', 'Chief Minister', 'President', 'Prime Minister'],
                        'correct_answer': 'Governor'
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
            },
            
            # Class 7 Questions
            7: {
                'Math': [
                    {
                        'question': 'What is the value of (-5) + (-3)?',
                        'options': ['-8', '-2', '2', '8'],
                        'correct_answer': '-8'
                    },
                    {
                        'question': 'The sum of angles in a triangle is:',
                        'options': ['90°', '180°', '270°', '360°'],
                        'correct_answer': '180°'
                    }
                ],
                'Science': [
                    {
                        'question': 'Which acid is present in lemon?',
                        'options': ['Acetic acid', 'Citric acid', 'Sulphuric acid', 'Hydrochloric acid'],
                        'correct_answer': 'Citric acid'
                    }
                ],
                'English': [
                    {
                        'question': 'What is a metaphor?',
                        'options': ['Direct comparison', 'Indirect comparison', 'Question', 'Statement'],
                        'correct_answer': 'Indirect comparison'
                    }
                ]
            },
            
            # Class 8 Questions
            8: {
                'Math': [
                    {
                        'question': 'What is x² - 4x + 4 when factored?',
                        'options': ['(x-2)²', '(x+2)²', '(x-4)²', '(x+4)²'],
                        'correct_answer': '(x-2)²'
                    }
                ],
                'Physics': [
                    {
                        'question': 'The unit of pressure is:',
                        'options': ['Newton', 'Pascal', 'Joule', 'Watt'],
                        'correct_answer': 'Pascal'
                    }
                ],
                'Chemistry': [
                    {
                        'question': 'What is the pH of pure water?',
                        'options': ['5', '6', '7', '8'],
                        'correct_answer': '7'
                    }
                ]
            },
            
            # Class 10 Questions
            10: {
                'Math': [
                    {
                        'question': 'The quadratic formula is used to find:',
                        'options': ['Roots of linear equations', 'Roots of quadratic equations', 'Area of circle', 'Volume of sphere'],
                        'correct_answer': 'Roots of quadratic equations'
                    }
                ],
                'Physics': [
                    {
                        'question': 'The resistance of a conductor depends on:',
                        'options': ['Length only', 'Area only', 'Material only', 'All of these'],
                        'correct_answer': 'All of these'
                    }
                ]
            },
            
            # Class 12 Questions (Advanced Competitive Level)
            12: {
                'Physics': [
                    {
                        'question': 'The de Broglie wavelength is given by:',
                        'options': ['λ = h/p', 'λ = h/mv', 'λ = hf', 'λ = c/f'],
                        'correct_answer': 'λ = h/p'
                    },
                    {
                        'question': 'In photoelectric effect, the stopping potential depends on:',
                        'options': ['Intensity only', 'Frequency only', 'Both intensity and frequency', 'Neither'],
                        'correct_answer': 'Frequency only'
                    }
                ],
                'Chemistry': [
                    {
                        'question': 'The rate constant of a zero order reaction has units:',
                        'options': ['mol L⁻¹ s⁻¹', 's⁻¹', 'mol⁻¹ L s⁻¹', 'mol² L⁻² s⁻¹'],
                        'correct_answer': 'mol L⁻¹ s⁻¹'
                    }
                ],
                'Math': [
                    {
                        'question': 'The range of function f(x) = sin⁻¹(x) is:',
                        'options': ['[-π/2, π/2]', '[0, π]', '[-π, π]', '[-1, 1]'],
                        'correct_answer': '[-π/2, π/2]'
                    }
                ]
            }
        }
    
    def get_subjects_for_class(self, class_num):
        """Get available subjects for a given class"""
        base_subjects = ['Math', 'Science', 'English', 'Hindi', 'GK', 'Computers', 'Sports', 'Value Education']
        
        if class_num <= 5:
            return base_subjects + ['Telugu']
        elif class_num <= 7:
            return ['Math', 'Science', 'English', 'Social', 'Hindi', 'Telugu', 'GK', 'Computers']
        elif class_num <= 8:
            return ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics']
        elif class_num <= 10:
            return ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 'Hindi', 'Telugu', 'History', 'Geography', 'Civics']
        else:  # Class 11-12
            return ['Physics', 'Chemistry', 'Math', 'Biology', 'English']
    
    def generate_quiz(self, class_num, subject, num_questions, language):
        """Generate quiz questions for given parameters"""
        try:
            # Get questions for the class, with fallback logic
            class_questions = self.questions_data.get(class_num, {})
            
            # If exact class not found, find nearest available class
            if not class_questions:
                available_classes = sorted(self.questions_data.keys())
                if class_num <= 5:
                    nearest_class = 3
                elif class_num <= 8:
                    nearest_class = 6
                elif class_num <= 10:
                    nearest_class = 9
                else:
                    nearest_class = 11
                class_questions = self.questions_data.get(nearest_class, {})
            
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
