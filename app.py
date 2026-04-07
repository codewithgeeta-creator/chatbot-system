from flask import Flask, render_template, request, jsonify
import json

# ✅ Create app (THIS WAS MISSING / ERROR BEFORE)
app = Flask(__name__)

# Load intents file
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot API
@app.route("/get", methods=["POST"])
def chatbot():
    user_message = request.json["message"]

    # Language detection
    if any(char in user_message for char in "ಅಆಇಈಉಊಎಏಐಒಓಔ"):
        lang = "kn"
    elif any(char in user_message for char in "अआइईउऊएऐओऔ"):
        lang = "hi"
    elif any(char in user_message for char in "అఆఇఈఉఊఎఏఐఒఓఔ"):
        lang = "te"
    else:
        lang = "en"

    user_message = user_message.lower()

    # Match intent
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message or user_message in pattern:

                responses = intent["responses"]

                # Multilingual response
                if isinstance(responses, dict):
                    return jsonify({"reply": responses.get(lang, responses["en"])})

                return jsonify({"reply": responses[0]})

    return jsonify({"reply": "Sorry, I didn't understand that."})

# Run app
if __name__ == "__main__":
    app.run(debug=True)
