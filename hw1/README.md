# 🌍 Word Guessing & Translation Game

## 📌 Overview
This is a **full-stack Flask web application** that challenges users to **guess a word based on its definition**. Once a word is correctly guessed, users can **click on a country** to see the word translated into that country's primary language using **Google Translate API**.

## 🎮 How It Works
1️⃣ **Guess the Word:** The user is presented with a word definition and must guess the correct word.  
2️⃣ **If Correct:** A world map appears, allowing the user to click on a country.  
3️⃣ **Translation:** The selected word is translated into the primary language of the clicked country.  
4️⃣ **Next Word:** The user can move to the next word and continue playing.  

## 🛠️ Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **APIs Used:**
  - **Dictionary API**: Fetches definitions of words.
  - **Google Translate API**: Translates words into different languages.
  - **OpenStreetMap (Leaflet.js + Nominatim API)**: Provides an interactive map for country selection.
  - **REST Countries API**: Retrieves the official language of a country.

## 📥 Installation & Setup
### **1. Clone the Repository**
```bash
$ git clone https://github.com/your-repo/word-guess-game.git
$ cd word-guess-game
```

### **2. Set Up Virtual Environment (Recommended)**
```bash
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scriptsctivate
```

### **3. Install Dependencies**
```bash
$ pip install flask requests
```

### **4. Run the Flask App**
```bash
$ python app.py
```
**Access the app in your browser:** `http://127.0.0.1:5000/`

## ✅ How to Use the App
1. Start the app and visit `http://127.0.0.1:5000/`.
2. Guess the word based on the given definition.
3. If correct, a world map appears.
4. Click on a country to see the word translated into the country’s primary language.
5. Click the "Next Word" button to continue playing.

## 🧪 Running Unit Tests
This app includes a **comprehensive test suite** to ensure correctness.

### **1. Run All Tests**
```bash
$ python -m unittest test_app.py
```

### **2. What’s Tested?**
| Test Name | Description |
|-----------|-------------|
| `test_home_page` | Checks if the homepage loads successfully |
| `test_next_word` | Ensures the `/next_word` route works correctly |
| `test_get_country_language_code_valid` | Tests language detection for valid countries |
| `test_get_country_language_code_invalid` | Ensures unknown countries default to English |
| `test_translate_word_valid` | Tests translation of words into various languages |
| `test_translate_word_empty` | Ensures empty words return a proper response |
| `test_get_definition_valid` | Checks word definitions from the dictionary API |
| `test_get_definition_invalid` | Ensures gibberish words return `None` |
| `test_translate_api_valid` | Tests `/translate` API with valid country input |
| `test_translate_api_invalid` | Ensures `/translate` API handles unknown countries |
| `test_translate_api_missing_country` | Handles cases where no country is provided |
| `test_translate_api_invalid_method` | Ensures only POST requests work for `/translate` |

## 🔥 Future Enhancements
- **Leaderboard & Score Tracking** 📊
- **Timed Challenge Mode** ⏳
- **More Language Options & Custom Translations** 🌎
- **User Accounts & Game History** 👤

## 📜 License
MIT License - Feel free to modify and improve!

## 🤝 Contributing
Have ideas or found a bug? Create an issue or submit a pull request!

## 🎯 Contact
For questions or feedback, reach out via GitHub Issues.

---
Enjoy the game! 🚀