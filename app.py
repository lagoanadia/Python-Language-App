import threading
import customtkinter as ctk
from vocab import save_word, create_file_if_not_exists, get_all_words, delete_word, get_translation
from quiz import create_quiz_if_not_exists, save_word_quiz, update_word_status, unlearnt_words, delete_quiz_word
from ai import chat

app = ctk.CTk()
app.title("AI Converstion!")
app.state("zoomed")
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)
quiz_frame = ctk.CTkFrame(app)

#=================================MAIN FRAME========================================
ai_chat = ctk.CTkFrame(main_frame)
ai_chat.pack(side="left", fill="both", expand=True, padx=20, pady=10)

vocabulary = ctk.CTkFrame(main_frame)
vocabulary.pack(side="right", fill="both", expand=True, padx=20, pady=10)

# ============================= CHAT HISTORY ====================
chatbox = ctk.CTkTextbox(ai_chat, font=("Segoe UI", 15))
chatbox.pack(fill="both", expand=True, pady=10, padx=10)
chatbox.configure(state="disabled")

# ============================= VOCABULARY LIST ====================
vocab_list = ctk.CTkScrollableFrame(vocabulary)
vocab_list.pack(fill="both", expand=True, pady=10, padx=10)

# ============================= SEND FRAME ====================
send_frame = ctk.CTkFrame(ai_chat)
send_frame.pack(fill="x", padx=10, pady=5)

msg_input = ctk.CTkEntry(send_frame, height=40, fg_color="gray", font=("Segoe UI", 15))
msg_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)

send_btn = ctk.CTkButton(send_frame, text="Send", width=100, height=40, font=("Segoe UI", 15))
send_btn.pack(side="right", padx=10, pady=10)

# ============================= ADD FRAME ====================
add_frame = ctk.CTkFrame(vocabulary)
add_frame.pack(fill="x", padx=10, pady=5)

word_input = ctk.CTkEntry(add_frame, height=40, fg_color="gray", font=("Segoe UI", 15))
word_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)

add_btn = ctk.CTkButton(add_frame, text="Add", width=100, height=40, font=("Segoe UI", 15))
add_btn.pack(side="right", padx=10, pady=10)

# =================================== QUIZ FRAME =====================================
quiz_btn = ctk.CTkButton(ai_chat, height=50, text="Quiz Mode", font=("Segoe UI", 15))
quiz_btn.pack(fill="x", padx=10, pady=10)

back_btn = ctk.CTkButton(quiz_frame, width=50, height=30, text="Chat Mode", font=("Segoe UI", 15))
back_btn.pack(padx=10, pady=10)

progress = ctk.CTkLabel(quiz_frame, width=50,height=50, font=("Segoe UI", 10))
progress.pack(pady=20)

word_card = ctk.CTkTextbox(quiz_frame, width=500, height=200, font=("Segoe UI", 30))
word_card.pack(pady=50)
word_card.configure(state="disabled")
word_card.tag_config("center", justify="center")

guess_frame = ctk.CTkFrame(quiz_frame)
guess_frame.pack()

user_guess = ctk.CTkEntry(guess_frame, width=500, height=50, placeholder_text="translate", font=("Segoe UI", 15))
user_guess.pack(side="left")

guess_btn = ctk.CTkButton(guess_frame, text="Check", font=("Segoe UI", 15))
guess_btn.pack(side="right", fill="y")

# ==================================FUNCTIONS===================================================
def send_message():
    message = msg_input.get()
    if not message:
        return
    chatbox.configure(state="normal")
    chatbox.insert("end", "\nYou: " + message + "\n")
    chatbox.configure(state="disabled")
    send_btn.configure(state="disabled", text="Writing...")
    msg_input.delete(0, "end")

    def get_response():
        response = chat(message)
        chatbox.configure(state="normal")
        chatbox.insert("end", "AI: " + response + "\n\n")
        chatbox.configure(state="disabled")
        send_btn.configure(text="Send", state="normal")

    threading.Thread(target=get_response).start()

send_btn.configure(command=send_message)

create_file_if_not_exists()
create_quiz_if_not_exists()

def add_word():
    word = word_input.get()
    if not word:
        return
    create_row(word, "")
    word_input.delete(0, "end")

def create_row(word, saved_translation):
    row = ctk.CTkFrame(vocab_list)
    row.pack(fill="x", padx=5, pady=2)

    word_Frame = ctk.CTkFrame(row)
    word_Frame.pack(side="left", padx=5, pady=3)

    ctk.CTkLabel(word_Frame, text=word, font=("Segoe UI", 15)).pack(side="left", padx=5)

    translation = ctk.CTkEntry(word_Frame, placeholder_text="translation", font=("Segoe UI", 15))
    if saved_translation:
        translation.insert(0, saved_translation)
    translation.pack(side="right", padx=5)

    def on_save(btn):
        save_word(word, translation.get(), "Swedish")
        save_word_quiz(word, 'unlearnt')
        btn.configure(state="disabled", text="Saved")

    save_btn = ctk.CTkButton(row, text="Save", width=70, font=("Segoe UI", 15))
    save_btn.configure(command=lambda b=save_btn: on_save(b))
    save_btn.pack(side="right", padx=5)
    if saved_translation:
        save_btn.configure(state="disabled", text="Saved")

    ctk.CTkButton(row, text="Delete", command=lambda r=row, w=word: (r.destroy(), delete_word(w), delete_quiz_word(w)), width=70, font=("Segoe UI", 15)).pack(side="right", padx=5)

add_btn.configure(command=add_word)

def load_words():
    for word in get_all_words():
        create_row(word["word"], word["translation"])

app.after(100, load_words)

current_word = unlearnt_words()
current_index = 0

progress.configure(text=f"Word {current_index + 1} of {len(current_word)}")


def show_word():
    global current_index
    word_card.configure(state="normal", fg_color="gray10")
    word_card.delete("1.0", "end")
    word_card.insert("1.0", "\n\n" + current_word[current_index], "center")
    word_card.configure(state="disabled")
    progress.configure(text=f"Word {current_index + 1} of {len(current_word)}")

def check_answer():
    global current_index, current_word
    if user_guess.get() == get_translation(current_word[current_index]):
        result(True, current_word[current_index])
        current_index += 1
        if current_index < len(current_word):
            show_word()
        else:
            remaining = unlearnt_words()
            if not remaining:
                word_card.configure(state="normal")
                word_card.delete("1.0", "end")
                word_card.insert("1.0", "\n\n             Well Done!")
                word_card.configure(state="disabled")
            else:
                current_word = remaining
                current_index = 0
                show_word()
    else:
        result(False, current_word[current_index])
    user_guess.delete(0, "end")
          
def show_quiz():
    global current_word, current_index
    current_word = unlearnt_words()
    current_index = 0
    main_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)
    if not current_word:
        word_card.configure(state="normal")
        word_card.delete("1.0", "end")
        word_card.insert("1.0", "\n\n              No words to study!")
        word_card.configure(state="disabled")
    else:
        show_word()

quiz_btn.configure(command=show_quiz)

def quit_quiz():
    main_frame.pack(fill="both", expand=True)
    quiz_frame.pack_forget()

back_btn.configure(command=quit_quiz)

def result(correct, word):
    if correct:
        word_card.configure(fg_color="green")
        update_word_status(word, "learnt") 
        word_card.after(1000, lambda: word_card.configure(fg_color="gray10"))
    else:
        word_card.configure(fg_color="red")
        word_card.after(1000, lambda: word_card.configure(fg_color="gray10"))

guess_btn.configure(command=check_answer)
app.mainloop()