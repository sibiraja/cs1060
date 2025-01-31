from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import random

app = Flask(__name__)

# Load predefined word list
with open("wordlists/new_words.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]

word_index = 0
selected_word = None

# Language name to ISO 639-1 code mapping
language_codes = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
    "Bulgarian": "bg", "Catalan": "ca", "Cebuano": "ceb", "Chichewa": "ny", "Chinese": "zh",
    "Corsican": "co", "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl",
    "English": "en", "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi",
    "French": "fr", "Frisian": "fy", "Galician": "gl", "Georgian": "ka", "German": "de",
    "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht", "Hausa": "ha", "Hawaiian": "haw",
    "Hebrew": "iw", "Hindi": "hi", "Hmong": "hmn", "Hungarian": "hu", "Icelandic": "is",
    "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it", "Japanese": "ja",
    "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km", "Korean": "ko",
    "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la", "Latvian": "lv",
    "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk", "Malagasy": "mg",
    "Malay": "ms", "Malayalam": "ml", "Maltese": "mt", "Maori": "mi", "Marathi": "mr",
    "Mongolian": "mn", "Myanmar (Burmese)": "my", "Nepali": "ne", "Norwegian": "no",
    "Pashto": "ps", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
    "Romanian": "ro", "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd", "Serbian": "sr",
    "Sesotho": "st", "Shona": "sn", "Sindhi": "sd", "Sinhala": "si", "Slovak": "sk",
    "Slovenian": "sl", "Somali": "so", "Spanish": "es", "Sundanese": "su", "Swahili": "sw",
    "Swedish": "sv", "Tajik": "tg", "Tamil": "ta", "Telugu": "te", "Thai": "th",
    "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Uzbek": "uz", "Vietnamese": "vi",
    "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}

# Function to get the ISO language code for a country
def get_country_language_code(country_name):
    country_api_url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(country_api_url)
    if response.status_code == 200:
        try:
            data = response.json()[0]
            languages = list(data["languages"].values())
            language_name = languages[0]  # Get the first language
            if len(languages) > 1 and language_name == "English": # NOTE: sometimes the countries list English as the first language, so use the second one if it exists
                language_name = languages[1]
            # print(language_name)
            return language_codes.get(language_name, "en")  # Default to English if not found
        except (IndexError, KeyError):
            return "en"  # Default to English if no language found
    return "en"

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

    # Get the primary language code of the selected country
    language_code = get_country_language_code(country)

    if language_code == "en" and country != "USA":  # If the language is English but it's not the USA, it's an invalid country
        return jsonify({"translated_word": "Language not found for this country."})

    # Translate word to detected language
    translated_word = translate_word(selected_word, language_code)

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
