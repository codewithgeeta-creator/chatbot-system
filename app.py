@app.route("/get", methods=["POST"])
def chatbot():
    user_message = request.json["message"]

    # Detect language from user input
    if any(char in user_message for char in "ಅಆಇಈಉಊಎಏಐಒಓಔ"):
        lang = "kn"
    elif any(char in user_message for char in "अआइईउऊएऐओऔ"):
        lang = "hi"
    elif any(char in user_message for char in "అఆఇఈఉఊఎఏఐఒఓఔ"):
        lang = "te"
    else:
        lang = "en"

    user_message = user_message.lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message or user_message in pattern:

                responses = intent["responses"]

                # If responses are dictionary (multi-language)
                if isinstance(responses, dict):
                    return jsonify({"reply": responses.get(lang, responses["en"])})

                # fallback
                return jsonify({"reply": responses[0]})

    return jsonify({"reply": "Sorry, I didn't understand that."})
