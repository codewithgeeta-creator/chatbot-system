from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chatbot():
    user_message = request.json["message"].lower()

    # Loop through intents
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message:
                
                # Detect language based on user input
                if any(char in user_message for char in "ಅಆಇಈಉಊಎಏಐಒಓಔ"):
                    return jsonify({"reply": intent.get("response_kn", intent["responses"][0])})

                elif any(char in user_message for char in "अआइईउऊएऐओऔ"):
                    return jsonify({"reply": intent.get("response_hi", intent["responses"][0])})

                elif any(char in user_message for char in "అఆఇఈఉఊఎఏఐఒఓఔ"):
                    return jsonify({"reply": intent.get("response_te", intent["responses"][0])})

                else:
                    return jsonify({"reply": intent["responses"][0]})

    return jsonify({"reply": "Sorry, I didn't understand that."})


if __name__ == "__main__":
    app.run(debug=True)
