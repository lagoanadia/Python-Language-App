import ollama 
SYSTEM_PROMPT = """You are a language learning assistant helping a complete beginner learn Swedish.

Rules you must always follow:
- Use only very simple Swedish — A1 level. Short sentences, basic vocabulary.
- EVERY sentence you write in Swedish MUST be followed immediately by its English translation in parentheses. No exceptions.
- If the user writes in Swedish and makes a mistake, correct it gently and explain why in English.
- If the user asks you what something means translate it and use a brief example sentence
- Keep responses short — maximum 3 sentences.
- Talk about simple everyday topics: food, weather, hobbies, city life."""
# ============================= CONVERSATION HISTORY ============================
# LIST OF DICTIONARIES — EACH DICTIONARY REPRESENTS ONE MESSAGE
# OLLAMA HAS NO MEMORY, SO WE PASS THE FULL HISTORY ON EVERY CALL
chat_history = []

def chat(user_message):
# APPEND USER MESSAGE TO HISTORY AS A DICTIONARY WITH role AND content KEYS
    chat_history.append(
        {
        "role":"user",
        "content":user_message
        }
    )
# CALL OLLAMA — PASSES SYSTEM PROMPT + FULL HISTORY ON EVERY REQUEST
# response IS AN OBJECT WITH NESTED DICTIONARIES — WE ONLY NEED response["message"]["content"]
    response = ollama.chat(
        model = "llama3.2",
        messages = [{"role":"system","content":SYSTEM_PROMPT}] + chat_history
    )
# EXTRACT THE TEXT FROM THE NESTED OBJECT: response → message → content
    ai_message = response["message"]["content"]
# APPEND AI RESPONSE TO HISTORY SO NEXT CALL INCLUDES IT
    chat_history.append(
        {
        "role":"assistant",
        "content":ai_message
        }
    )
  # RETURN THE TEXT TO THE CALLER (app.py)
    return ai_message

    