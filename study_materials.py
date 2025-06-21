import streamlit as st
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class StudyMaterials:
    def __init__(self):
        self.materials_data = {
            3: {
                'Math': {
                    'description': '📊 Basic arithmetic, shapes, and patterns for young learners',
                    'sample_pdf': True,
                    'resources': [
                        'Addition and Subtraction practice sheets',
                        'Multiplication tables (1-10)',
                        'Shape recognition activities',
                        'Simple word problems'
                    ]
                },
                'Science': {
                    'description': '🔬 Exploring the world around us - plants, animals, and nature',
                    'sample_pdf': True,
                    'resources': [
                        'My Body parts and functions',
                        'Animals and their homes',
                        'Plants we eat',
                        'Weather and seasons'
                    ]
                },
                'English': {
                    'description': '📚 Building vocabulary and reading skills',
                    'sample_pdf': True,
                    'resources': [
                        'Phonics and letter sounds',
                        'Simple story books',
                        'Rhymes and poems',
                        'Basic grammar rules'
                    ]
                }
            },
            6: {
                'Math': {
                    'description': '🧮 Integers, fractions, geometry and basic algebra',
                    'sample_pdf': True,
                    'resources': [
                        'Number system and operations',
                        'Fractions and decimals',
                        'Basic geometry concepts',
                        'Simple equations'
                    ]
                },
                'Science': {
                    'description': '⚗️ Introduction to scientific concepts and experiments',
                    'sample_pdf': True,
                    'resources': [
                        'Matter and its properties',
                        'Light and shadows',
                        'Motion and force basics',
                        'Living and non-living things'
                    ]
                },
                'History': {
                    'description': '🏛️ Ancient civilizations and Indian history',
                    'sample_pdf': True,
                    'resources': [
                        'Indus Valley Civilization',
                        'Vedic period',
                        'Mauryan Empire',
                        'Medieval India overview'
                    ]
                },
                'Geography': {
                    'description': '🌍 Earth, maps, and environmental studies',
                    'sample_pdf': True,
                    'resources': [
                        'Solar system basics',
                        'Continents and oceans',
                        'Climate and weather',
                        'Natural resources'
                    ]
                }
            },
            9: {
                'Math': {
                    'description': '📐 Advanced algebra, geometry, and coordinate geometry',
                    'sample_pdf': True,
                    'resources': [
                        'Real numbers and irrational numbers',
                        'Polynomials and factorization',
                        'Linear equations in two variables',
                        'Quadrilaterals and triangles',
                        'Statistics and probability'
                    ]
                },
                'Physics': {
                    'description': '⚡ Motion, force, work, energy and sound',
                    'sample_pdf': True,
                    'resources': [
                        'Motion in one dimension',
                        'Force and laws of motion',
                        'Gravitation',
                        'Work and energy',
                        'Sound waves'
                    ]
                },
                'Chemistry': {
                    'description': '🧪 Atoms, molecules, and chemical reactions',
                    'sample_pdf': True,
                    'resources': [
                        'Matter in our surroundings',
                        'Atoms and molecules',
                        'Structure of the atom',
                        'Chemical reactions and equations'
                    ]
                },
                'Biology': {
                    'description': '🦠 Cell structure, tissues, and diversity in living organisms',
                    'sample_pdf': True,
                    'resources': [
                        'The fundamental unit of life - Cell',
                        'Tissues',
                        'Diversity in living organisms',
                        'Natural resources management'
                    ]
                }
            },
            11: {
                'Physics': {
                    'description': '🔬 Advanced mechanics, thermodynamics, and waves',
                    'sample_pdf': True,
                    'resources': [
                        'Physical world and measurement',
                        'Kinematics and dynamics',
                        'Work, energy and power',
                        'System of particles and rotational motion',
                        'Gravitation and oscillations',
                        'Mechanical properties of solids and fluids',
                        'Thermodynamics and kinetic theory',
                        'Waves and acoustics'
                    ]
                },
                'Chemistry': {
                    'description': '⚛️ Atomic structure, bonding, and organic chemistry basics',
                    'sample_pdf': True,
                    'resources': [
                        'Some basic concepts of chemistry',
                        'Structure of atom',
                        'Classification of elements',
                        'Chemical bonding and molecular structure',
                        'States of matter',
                        'Thermodynamics',
                        'Equilibrium and redox reactions',
                        'Organic chemistry - basic principles',
                        'Hydrocarbons'
                    ]
                },
                'Math': {
                    'description': '🔢 Sets, functions, trigonometry, and coordinate geometry',
                    'sample_pdf': True,
                    'resources': [
                        'Sets and functions',
                        'Trigonometric functions',
                        'Principle of mathematical induction',
                        'Complex numbers and quadratic equations',
                        'Linear inequalities',
                        'Permutations and combinations',
                        'Binomial theorem',
                        'Sequences and series',
                        'Straight lines and conic sections',
                        'Introduction to 3D geometry',
                        'Limits and derivatives',
                        'Mathematical reasoning',
                        'Statistics and probability'
                    ]
                },
                'Biology': {
                    'description': '🧬 Plant and animal physiology, cell biology',
                    'sample_pdf': True,
                    'resources': [
                        'Diversity in living world',
                        'Structural organization in animals and plants',
                        'Cell structure and function',
                        'Plant physiology',
                        'Human physiology'
                    ]
                }
            }
        }
    
    def get_materials_for_class(self, class_num):
        """Get study materials for a specific class"""
        # Find the closest available class materials
        available_classes = sorted(self.materials_data.keys())
        if class_num in available_classes:
            return self.materials_data[class_num]
        else:
            # Find nearest class
            nearest_class = min(available_classes, key=lambda x: abs(x - class_num))
            return self.materials_data[nearest_class]
    
    def generate_sample_pdf(self, subject, class_num):
        """Generate a sample PDF for the given subject and class"""
        if not REPORTLAB_AVAILABLE:
            return self._generate_text_pdf_fallback(subject, class_num)
            
        try:
            # Create a bytes buffer for the PDF
            buffer = io.BytesIO()
            
            # Create the PDF document
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(f"{subject} - Class {class_num} Study Notes", title_style))
            story.append(Spacer(1, 20))
            
            # Get materials data
            materials = self.get_materials_for_class(class_num)
            subject_data = materials.get(subject, {})
            
            # Description
            if subject_data.get('description'):
                story.append(Paragraph("Overview:", styles['Heading2']))
                story.append(Paragraph(subject_data['description'], styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Topics/Resources
            if subject_data.get('resources'):
                story.append(Paragraph("Key Topics Covered:", styles['Heading2']))
                for i, resource in enumerate(subject_data['resources'], 1):
                    story.append(Paragraph(f"{i}. {resource}", styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Sample content based on subject
            story.append(Paragraph("Sample Study Material:", styles['Heading2']))
            
            if subject == 'Math':
                story.append(Paragraph("Important Formulas and Concepts:", styles['Heading3']))
                if class_num <= 5:
                    content = """
                    Basic Addition: a + b = sum
                    Basic Subtraction: a - b = difference
                    Multiplication Tables: Practice tables 1-10
                    Shapes: Circle, Square, Triangle, Rectangle
                    """
                elif class_num <= 8:
                    content = """
                    Algebraic Expressions: ax + b
                    Geometry: Area of rectangle = length × width
                    Fractions: a/b + c/d = (ad + bc)/bd
                    Percentages: x% = x/100
                    """
                else:
                    content = """
                    Quadratic Formula: x = [-b ± √(b²-4ac)]/2a
                    Trigonometry: sin²θ + cos²θ = 1
                    Coordinate Geometry: Distance formula
                    Calculus: d/dx(xⁿ) = nxⁿ⁻¹
                    """
                story.append(Paragraph(content, styles['Normal']))
            
            elif subject == 'Science' or subject == 'Physics':
                story.append(Paragraph("Key Concepts and Laws:", styles['Heading3']))
                if class_num <= 5:
                    content = """
                    Living and Non-living things
                    Parts of a plant: Root, Stem, Leaves, Flowers
                    Human body parts and their functions
                    Weather changes and seasons
                    """
                elif class_num <= 8:
                    content = """
                    Newton's Laws of Motion
                    States of Matter: Solid, Liquid, Gas
                    Photosynthesis in plants
                    Light travels in straight lines
                    """
                else:
                    content = """
                    Newton's Laws: F = ma
                    Energy Conservation: Energy cannot be created or destroyed
                    Wave Equation: v = fλ
                    Ohm's Law: V = IR
                    """
                story.append(Paragraph(content, styles['Normal']))
            
            elif subject == 'Chemistry':
                story.append(Paragraph("Chemical Concepts:", styles['Heading3']))
                content = """
                Periodic Table organization
                Chemical Bonding: Ionic and Covalent
                Acids and Bases: pH scale
                Chemical Reactions and Balancing
                Atomic Structure: Protons, Neutrons, Electrons
                """
                story.append(Paragraph(content, styles['Normal']))
            
            elif subject == 'Biology':
                story.append(Paragraph("Biological Concepts:", styles['Heading3']))
                content = """
                Cell Theory: All living things are made of cells
                Photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂
                Human Body Systems: Circulatory, Respiratory, Digestive
                Genetics: DNA structure and function
                Evolution: Natural selection and adaptation
                """
                story.append(Paragraph(content, styles['Normal']))
            
            else:
                content = f"""
                This is a sample study material for {subject} - Class {class_num}.
                
                Key points to remember:
                • Regular practice is essential
                • Make notes while studying
                • Solve previous year questions
                • Ask questions when in doubt
                
                Study Tips:
                1. Create a study schedule
                2. Take regular breaks
                3. Discuss with friends and teachers
                4. Stay positive and motivated
                """
                story.append(Paragraph(content, styles['Normal']))
            
            # Footer
            story.append(Spacer(1, 30))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=10,
                alignment=1,
                textColor='gray'
            )
            story.append(Paragraph("Generated by Vidya Sakhi - Your Learning Bestie", footer_style))
            story.append(Paragraph("Keep Learning! Keep Growing! 🌟", footer_style))
            
            # Build PDF
            doc.build(story)
            
            # Get the value of the buffer
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            # Return a simple text-based PDF content as fallback
            return self._generate_text_pdf_fallback(subject, class_num)
    
    def _generate_text_pdf_fallback(self, subject, class_num):
        """Generate a simple text-based study material when PDF generation fails"""
        materials = self.get_materials_for_class(class_num)
        subject_data = materials.get(subject, {})
        
        content = f"""VIDYA SAKHI - STUDY NOTES
        
Subject: {subject}
Class: {class_num}

OVERVIEW:
{subject_data.get('description', 'Study material for ' + subject)}

KEY TOPICS:
"""
        
        if subject_data.get('resources'):
            for i, resource in enumerate(subject_data['resources'], 1):
                content += f"{i}. {resource}\n"
        
        content += f"""

STUDY TIPS:
- Create a regular study schedule
- Take notes while reading
- Practice problems daily
- Ask questions when in doubt
- Review regularly before exams

Generated by Vidya Sakhi - Your Learning Bestie
Keep Learning! Keep Growing!
"""
        
        return content.encode('utf-8')
