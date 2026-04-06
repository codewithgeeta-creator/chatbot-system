from flask import Flask, render_template, request
import json
from deep_translator import GoogleTranslator
from difflib import get_close_matches

app = Flask(__name__)

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Smart matching
def get_response(user_input):
    user_input = user_input.lower()
    all_patterns = []

    for intent in data["intents"]:
        all_patterns.extend(intent["patterns"])

    match = get_close_matches(user_input, all_patterns, n=1, cutoff=0.5)

    if match:
        for intent in data["intents"]:
            if match[0] in intent["patterns"]:
                return intent["responses"][0]

    return "I’m here to help with information about courses, admissions, fees, placements, and facilities. Please ask your query clearly."

# Detect language
def detect_language(text):
    if any('\u0C80' <= ch <= '\u0CFF' for ch in text):
        return 'kn'
    elif any('\u0900' <= ch <= '\u097F' for ch in text):
        return 'hi'
    elif any('\u0C00' <= ch <= '\u0C7F' for ch in text):
        return 'te'
    else:
        return 'en'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot():
    userText = request.form["msg"]

    user_lang = detect_language(userText)

    # Translate to English
    translated = GoogleTranslator(source='auto', target='en').translate(userText)

    # Get response
    bot_response = get_response(translated)

    # Translate back
    final_response = GoogleTranslator(source='en', target=user_lang).translate(bot_response)

    return final_response

if __name__ == "__main__":
    app.run(debug=True)