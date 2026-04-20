from flask import Flask, render_template, request
import json
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Smart response (priority-based)
def get_response(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["placement", "placed", "package", "company"]):
        return data["intents"][5]["responses"][0]

    elif any(word in user_input for word in ["fee", "fees", "cost"]):
        return data["intents"][3]["responses"][0]

    elif any(word in user_input for word in ["admission", "apply"]):
        return data["intents"][4]["responses"][0]

    elif any(word in user_input for word in ["course", "branch"]):
        return data["intents"][2]["responses"][0]

    elif any(word in user_input for word in ["facility", "facilities"]):
        return data["intents"][6]["responses"][0]

    elif any(word in user_input for word in ["about", "college", "ait"]):
        return data["intents"][1]["responses"][0]

    elif any(word in user_input for word in ["hi", "hello", "hey"]):
        return data["intents"][0]["responses"][0]

    return "Please ask about college, fees, courses, admissions, or placements."

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

    try:
        translated = GoogleTranslator(source='auto', target='en').translate(userText)
    except:
        translated = userText

    bot_response = get_response(translated)

    try:
        final_response = GoogleTranslator(source='en', target=user_lang).translate(bot_response)
    except:
        final_response = bot_response

    return final_response


if __name__ == "__main__":
    app.run(debug=True)
