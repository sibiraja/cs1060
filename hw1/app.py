from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Load words from the text file
with open("new_words.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]

word_index = 0  # In-memory tracking, resets when server restarts

# Function to get a word definition from the dictionary API
def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data[0]["meanings"][0]["definitions"][0]["definition"]
        except (KeyError, IndexError):
            return None
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    global word_index  # Use global variable for tracking progress

    if word_index >= len(words):  # Restart from the first word when the list is done
        word_index = 0

    current_word = words[word_index]
    definition = get_definition(current_word)

    # If no definition is found, skip to the next word
    if not definition:
        word_index += 1
        return redirect(url_for("index"))  

    message = ""
    show_next_button = False  # Controls whether "Next Word" button appears

    if request.method == "POST":
        user_guess = request.form.get("guess", "").strip().lower()
        if user_guess == current_word:
            message = "✅ Correct!"
            show_next_button = True  # Show "Next Word" button
        else:
            message = "❌ Incorrect! Try again."

    return render_template("index.html", definition=definition, message=message, show_next_button=show_next_button)

@app.route("/next")
def next_word():
    global word_index
    word_index += 1  # Move to the next word
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
