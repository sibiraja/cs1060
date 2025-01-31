from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random

app = Flask(__name__)

# Load country-related words from JSON file
with open("country_words.json", "r") as f:
    country_words = json.load(f)

selected_country = None
selected_word = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/select_country", methods=["POST"])
def select_country():
    global selected_country, selected_word

    data = request.get_json()
    selected_country = data.get("country")

    if selected_country in country_words:
        selected_word = random.choice(country_words[selected_country])
        hint = f"This word is related to {selected_country}."
    else:
        selected_word = None
        hint = "No words available for this country."

    return jsonify({"hint": hint})

@app.route("/guess", methods=["POST"])
def guess():
    global selected_word

    user_guess = request.form.get("guess", "").strip().lower()
    correct = user_guess.lower() == selected_word.lower()
    
    return render_template("game.html", hint=f"Hint: This word is related to {selected_country}.", 
                           message="✅ Correct!" if correct else "❌ Incorrect! Try again.", 
                           show_next_button=correct)

if __name__ == "__main__":
    app.run(debug=True)
