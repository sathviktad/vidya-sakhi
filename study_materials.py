import streamlit as st
import io
from utils import t

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
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/3rd%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Science': {
                    'description': '🌿 Official SCERT Telangana Environmental Studies textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/3rd%20Class%20EVS%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📚 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/3rd%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📖 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/3rd%20Class%20Hindi%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📖 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/3rd%20Class%20Telugu%20TM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            4: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/4th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Science': {
                    'description': '🌿 Official SCERT Telangana Environmental Studies textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/4th%20Class%20EVS%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📚 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/4th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📖 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/4th%20Class%20Hindi%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📖 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/4th%20Class%20Telugu%20TM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            5: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/5th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Science': {
                    'description': '🌿 Official SCERT Telangana Environmental Studies textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/5th%20Class%20EVS%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📚 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/5th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📖 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/5th%20Class%20Hindi%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📖 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': True,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/5th%20Class%20Telugu%20TM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            6: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/6th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Science': {
                    'description': '🔬 Official SCERT Telangana General Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/6th%20Class%20General%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/6th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Social': {
                    'description': '🌏 Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/6th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📝 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/6th%20Class%20Hindi.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📗 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/6th%20Class%20Telugu.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'GK': {
                    'description': '🌐 General Knowledge resource (sample link)',
                    'sample_pdf': False,
                    'resources': [
                        'https://ncert.nic.in/textbook/pdf/legk1dd.zip',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Computers': {
                    'description': '💻 Computer Studies resource (sample link)',
                    'sample_pdf': False,
                    'resources': [
                        'https://www.typingbaba.com/',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            7: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/7th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Science': {
                    'description': '🔬 Official SCERT Telangana General Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/7th%20Class%20General%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/7th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Social': {
                    'description': '🌏 Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/7th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📝 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/7th%20Class%20Hindi.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📗 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/7th%20Class%20Telugu.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'GK': {
                    'description': '🌐 General Knowledge resource (sample link)',
                    'sample_pdf': False,
                    'resources': [
                        'https://ncert.nic.in/textbook/pdf/legk1dd.zip',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Computers': {
                    'description': '💻 Computer Studies resource (sample link)',
                    'sample_pdf': False,
                    'resources': [
                        'https://www.typingbaba.com/',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            8: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Physics': {
                    'description': '🔬 Official SCERT Telangana Physical Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Physical%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Chemistry': {
                    'description': '🧪 Official SCERT Telangana Physical Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Physical%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Biology': {
                    'description': '🌱 Official SCERT Telangana Biological Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Biological%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📝 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Hindi.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📗 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Telugu.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'History': {
                    'description': '📜 Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Geography': {
                    'description': '🗺️ Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Civics': {
                    'description': '⚖️ Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/8th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            9: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Physics': {
                    'description': '🔬 Official SCERT Telangana Physical Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Physical%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Chemistry': {
                    'description': '🧪 Official SCERT Telangana Physical Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Physical%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Biology': {
                    'description': '🌱 Official SCERT Telangana Biological Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Biological%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📝 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Hindi.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📗 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Telugu.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'History': {
                    'description': '📜 Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Geography': {
                    'description': '🗺️ Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Civics': {
                    'description': '⚖️ Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/9th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            10: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Physics': {
                    'description': '🔬 Official SCERT Telangana Physical Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Physical%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Chemistry': {
                    'description': '🧪 Official SCERT Telangana Physical Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Physical%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Biology': {
                    'description': '🌱 Official SCERT Telangana Biological Science textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Biological%20Science%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Hindi': {
                    'description': '📝 Official SCERT Telangana Hindi textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Hindi.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Telugu': {
                    'description': '📗 Official SCERT Telangana Telugu textbook',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Telugu.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'History': {
                    'description': '📜 Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Geography': {
                    'description': '🗺️ Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Civics': {
                    'description': '⚖️ Official SCERT Telangana Social Studies textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/10th%20Class%20Social%20Studies%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            11: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/11th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Physics': {
                    'description': '🔬 Official SCERT Telangana Physics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/11th%20Class%20Physics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Chemistry': {
                    'description': '🧪 Official SCERT Telangana Chemistry textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/11th%20Class%20Chemistry%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Biology': {
                    'description': '🌱 Official SCERT Telangana Biology textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/11th%20Class%20Biology%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/11th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            },
            12: {
                'Math': {
                    'description': '🧮 Official SCERT Telangana Mathematics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/12th%20Class%20Mathematics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Physics': {
                    'description': '🔬 Official SCERT Telangana Physics textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/12th%20Class%20Physics%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Chemistry': {
                    'description': '🧪 Official SCERT Telangana Chemistry textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/12th%20Class%20Chemistry%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'Biology': {
                    'description': '🌱 Official SCERT Telangana Biology textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/12th%20Class%20Biology%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                },
                'English': {
                    'description': '📘 Official SCERT Telangana English textbook (English Medium)',
                    'sample_pdf': False,
                    'resources': [
                        'https://scert.telangana.gov.in/pdf/publication/ebooks2023/12th%20Class%20English%20EM.pdf',
                        'https://scert.telangana.gov.in/ebooks.html'
                    ]
                }
            }
        }
        # Ensure all classes and subjects have at least a placeholder
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
        for class_num, subjects in HARDCODED_SUBJECTS.items():
            if class_num not in self.materials_data:
                self.materials_data[class_num] = {}
            for subject in subjects:
                if subject not in self.materials_data[class_num]:
                    self.materials_data[class_num][subject] = {
                        'description': f'Sample study material for {subject} (Class {class_num}): This subject covers important concepts and practice topics to help you excel.',
                        'sample_pdf': True,
                        'resources': [
                            f'Key concepts and practice questions for {subject}',
                            f'Important notes and revision tips for {subject} (Class {class_num})'
                        ]
                    }
        
        # Add a 'videos' field to every subject in every class with relevant YouTube links for explanations.
        for class_num, subjects in self.materials_data.items():
            for subject, data in subjects.items():
                videos = []
                subj = subject.lower()
                if subj == 'physics':
                    videos = [
                        'https://www.youtube.com/@t.srinivasacharychary7675/videos',
                        'https://www.youtube.com/user/khanacademy',
                        'https://www.youtube.com/c/LearnCBSE'
                    ]
                elif subj == 'math':
                    videos = [
                        'https://www.youtube.com/user/khanacademy',
                        'https://www.youtube.com/c/LearnCBSE',
                        'https://www.youtube.com/c/MathAntics'
                    ]
                elif subj == 'chemistry':
                    videos = [
                        'https://www.youtube.com/user/khanacademy',
                        'https://www.youtube.com/c/LearnCBSE',
                        'https://www.youtube.com/c/CrashCourse'
                    ]
                elif subj == 'biology':
                    videos = [
                        'https://www.youtube.com/user/khanacademy',
                        'https://www.youtube.com/c/AmoebaSisters',
                        'https://www.youtube.com/c/CrashCourse'
                    ]
                elif subj == 'english':
                    videos = [
                        'https://www.youtube.com/c/BritishCouncilLEARNENGLISH',
                        'https://www.youtube.com/c/EnglishAddictwithMrDuncan',
                        'https://www.youtube.com/c/LearnCBSE'
                    ]
                elif subj == 'hindi':
                    videos = [
                        'https://www.youtube.com/c/HindiVyakaran',
                        'https://www.youtube.com/c/ExamपुरHindi'
                    ]
                elif subj == 'telugu':
                    videos = [
                        'https://www.youtube.com/c/LearnTeluguwithKaushik',
                        'https://www.youtube.com/c/TeluguBadi'
                    ]
                elif subj == 'social':
                    videos = [
                        'https://www.youtube.com/c/LearnCBSE',
                        'https://www.youtube.com/c/Unacademy'
                    ]
                elif subj == 'evs' or subj == 'science':
                    videos = [
                        'https://www.youtube.com/user/khanacademy',
                        'https://www.youtube.com/c/LearnCBSE'
                    ]
                else:
                    videos = [
                        'https://www.youtube.com/user/khanacademy'
                    ]
                data['videos'] = videos
    
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

    def show_materials_message(self):
        st.info(t('scert_link_info'))
