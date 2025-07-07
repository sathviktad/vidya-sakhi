import json
import shutil
import os

# File paths
QUIZ_FILE = 'quiz_questions.json'
BACKUP_FILE = 'quiz_questions_backup.json'

# Backup the original file
if not os.path.exists(BACKUP_FILE):
    shutil.copy(QUIZ_FILE, BACKUP_FILE)

# Load the quiz questions
with open(QUIZ_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

def generate_explanation(q):
    # Use the question and correct answer to generate a simple explanation
    # Try to keep it in the same language as the question
    question = q['question']
    answer = q['correct_answer']
    # Heuristic: if question or answer is in Hindi or Telugu script, use that language
    if any('\u0900' <= c <= '\u097F' for c in question+answer):
        return f"सही उत्तर: {answer}।"
    if any('\u0C00' <= c <= '\u0C7F' for c in question+answer):
        return f"సరైన సమాధానం: {answer}"
    # Otherwise, default to English
    return f"The correct answer is: {answer}."

# Patch all questions
for class_key, subjects in data.items():
    for subject, questions in subjects.items():
        for q in questions:
            if 'explanation' not in q:
                q['explanation'] = generate_explanation(q)

# Save the updated file
with open(QUIZ_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Explanations added to all questions! Backup saved as quiz_questions_backup.json.') 