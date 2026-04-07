from flask import Flask, render_template, request, jsonify
import json
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Detect language manually
def detect_language(text):
    if any(char in text for char in "ಅಆಇಈಉಊಎಏಐಒಓಔ"):
        return "kn"
    elif any(char in text for char in "अआइईउऊएऐओऔ"):
        return "hi"
    elif any(char in text for char in "అఆఇఈఉఊఎఏఐఒఓఔ"):
        return "te"
    else:
        return "en"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot():
    user_message = request.json["message"]
    lang = detect_language(user_message)

    user_message = user_message.lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message or user_message in pattern:

                reply = intent["responses"][0]

                # Translate only if not English
                if lang != "en":
                    try:
                        reply = GoogleTranslator(source='en', target=lang).translate(reply)
                    except:
                        pass  # fallback to English if error

                return jsonify({"reply": reply})

    return jsonify({"reply": "Sorry, I didn't understand that."})

if __name__ == "__main__":
    app.run(debug=True)
