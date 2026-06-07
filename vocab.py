import csv
import os
from datetime import date

FILE = "data/vocabulary.csv"
COLUMNS = ["date", "word","translation", "language"]

def create_file_if_not_exists():
    if not os.path.exists(FILE):
        with open(FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)

def save_word(word,translation,language, encoding='utf-8'):
    with open(FILE, 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([date.today(), word,translation, language]) 

def delete_word(word):
    words = get_all_words()
    with open(FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for w in words:
            if w["word"] != word:
                writer.writerow(w)

def get_translation(word):
    with open(FILE, 'r',encoding='utf-8')as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['word'] == word:
                return row['translation']
def get_all_words():
    with open(FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)