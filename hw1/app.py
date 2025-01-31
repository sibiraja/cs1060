from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import random

app = Flask(__name__)

# Load predefined word list
with open("new_words.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]

word_index = 0
selected_word = None

# Function to get a word definition from the dictionary API
def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data[0]["meanings"][0]["definitions"][0]["definition"]
        except (KeyError, IndexError):
            return None
    return None

# Function to get the official language of a country
def get_country_language(country_name):
    country_api_url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(country_api_url)
    if response.status_code == 200:
        try:
            data = response.json()[0]
            # Extract the first official language from the response
            return list(data["languages"].values())[0]  # Returns the language name
        except (IndexError, KeyError):
            return None
    return None

# Function to translate a word using Google Translate API
def translate_word(word, target_lang_code):
    translate_url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",  # Source language: English
        "tl": target_lang_code,  # Target language
        "dt": "t",
        "q": word
    }
    response = requests.get(translate_url, params=params)
    if response.status_code == 200:
        try:
            return response.json()[0][0][0]  # Extract translated text
        except (IndexError, KeyError):
            return None
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    global word_index, selected_word

    if word_index >= len(words):
        word_index = 0  # Restart from the first word

    selected_word = words[word_index]
    definition = get_definition(selected_word)

    # Skip word if no definition is found
    if not definition:
        word_index += 1
        return redirect(url_for("index"))

    message = ""
    show_map = False

    if request.method == "POST":
        user_guess = request.form.get("guess", "").strip().lower()
        if user_guess == selected_word.lower():
            message = "✅ Correct! Click a country to translate the word."
            show_map = True  # Show the world map for country selection
        else:
            message = "❌ Incorrect! Try again."

    return render_template("index.html", definition=definition, message=message, show_map=show_map)

@app.route("/translate", methods=["POST"])
def translate():
    global selected_word

    data = request.get_json()
    country = data.get("country")

    # Get the primary language of the selected country
    language = get_country_language(country)
    if not language:
        return jsonify({"translated_word": "Language not found for this country."})

    # Translate word to detected language
    translated_word = translate_word(selected_word, language)

    if not translated_word:
        translated_word = "Translation not found."

    return jsonify({"translated_word": translated_word})

@app.route("/next_word", methods=["GET"])
def next_word():
    global word_index
    word_index += 1  # Move to the next word
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
