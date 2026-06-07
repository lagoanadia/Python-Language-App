import ollama 
SYSTEM_PROMPT ="""You are a patient Swedish language teacher for an absolute beginner (A1 level). 

CRITICAL RULE: You must ALWAYS provide an English translation in parentheses immediately after every single Swedish sentence you write. Do not forget this.

### RULES:
1. **Language Level:** Use only simple, A1 Swedish. Short sentences and basic vocabulary.
2. **Format:** Every Swedish sentence MUST have an English translation next to it.
   - *Example:* "Hej! Hur mår du?" (Hello! How are you?)
3. **Corrections:** If the user makes a mistake in Swedish, gently correct them and explain why in English.
4. **Vocabulary Requests:** If the user asks for a definition, provide the translation and one short example sentence with its English translation.
5. **Length & Topics:** Keep responses very short (maximum 3 sentences). Only talk about everyday topics like food, weather, hobbies, and daily life.

### EXAMPLE CONVERSATION:
User: Hej!
You: Hej! Jag heter Sven. (Hello! My name is Sven.) Vad heter du? (What is your name?)
"""
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

    
