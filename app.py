from flask import Flask, render_template, request, jsonify
import json
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chatbot():
    user_message = request.json["message"]

    # Detect language
    detected = translator.detect(user_message)
    user_lang = detected.lang

    # Translate to English
    translated = translator.translate(user_message, dest="en").text.lower()

    # Match intent
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in translated:
                reply = intent["responses"][0]

                # Translate back to user language
                final_reply = translator.translate(reply, dest=user_lang).text

                return jsonify({"reply": final_reply})

    return jsonify({"reply": "Sorry, I didn't understand that."})


if __name__ == "__main__":
    app.run(debug=True)
