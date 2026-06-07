import csv
import os
from datetime import date

FILE = "data/quiz.csv"
COLUMNS =["date","word","status"]

def create_quiz_if_not_exists():
    if not os.path.exists(FILE):
        with open(FILE, 'w', newline='', encoding='utf-8')as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)


def save_word_quiz(word, status, encoding='utf-8'):
    with open(FILE, 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([date.today(), word,status]) 


def update_word_status(word, status):
    with open(FILE, 'r',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for row in rows:
        if row['word'] == word:
            row['status']=status
    with open(FILE, 'w', newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

def get_all_words():
    with open(FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)
    
def delete_quiz_word(word):
    words = get_all_words()
    with open(FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for w in words:
            if w["word"] != word:
                writer.writerow(w)               
def unlearnt_words():
    with open(FILE,'r',encoding='utf-8')as f:
        reader = csv.DictReader(f)
        unlearnt = []
        for row in reader:
            if row['status'] == 'unlearnt':
                unlearnt.append(row['word'])
    return unlearnt

