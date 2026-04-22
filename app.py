from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Smart response function
def get_response(user_input):
    user_input = user_input.lower()

    if "course" in user_input or "intake" in user_input:
        return data["intents"][1]["responses"][0]

    elif "placement" in user_input:
        return data["intents"][2]["responses"][0]

    elif "fee" in user_input:
        return data["intents"][3]["responses"][0]

    elif "admission" in user_input:
        return data["intents"][4]["responses"][0]

    elif "hi" in user_input or "hello" in user_input:
        return data["intents"][0]["responses"][0]

    return "Please ask about courses, placements, fees or admission."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot():
    userText = request.form["msg"]
    return get_response(userText)

if __name__ == "__main__":
    app.run(debug=True)
