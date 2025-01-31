import unittest
from app import app, get_country_language_code, translate_word, get_definition
import json

class AppTestCase(unittest.TestCase):
    
    # ✅ Setup test client before each test
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # ✅ Test: Ensure the home page loads correctly
    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Guess the Word!", response.data)  # Check if title is in response

    # ✅ Test: Ensure `/next_word` route works
    def test_next_word(self):
        response = self.app.get("/next_word")
        self.assertEqual(response.status_code, 302)  # Should redirect back to "/"

    # ✅ Test: Fetching country language code (valid countries)
    def test_get_country_language_code_valid(self):
        self.assertEqual(get_country_language_code("France"), "fr")  # French
        self.assertEqual(get_country_language_code("Japan"), "ja")  # Japanese
        self.assertEqual(get_country_language_code("India"), "hi")  # Hindi
        self.assertEqual(get_country_language_code("Brazil"), "pt")  # Portuguese
        self.assertEqual(get_country_language_code("Germany"), "de")  # German

    # ✅ Test: Fetching country language code (invalid country)
    def test_get_country_language_code_invalid(self):
        self.assertEqual(get_country_language_code("UnknownLand"), "en")  # Should default to English
        self.assertEqual(get_country_language_code(""), "en")  # Empty string should return English
        self.assertEqual(get_country_language_code("12345"), "en")  # Invalid numbers as input

    # ✅ Test: Translate a word using Google Translate API
    def test_translate_word_valid(self):
        english_word = "hello"
        translation = translate_word(english_word, "es")  # Spanish
        self.assertNotEqual(translation, "hello")  # Should not return the same word
        self.assertIsInstance(translation, str)  # Should return a string

    # ✅ Test: Translate empty word (should return empty or None)
    def test_translate_word_empty(self):
        translation = translate_word("", "fr")  # Empty string
        self.assertIn(translation, ["", None])  # Google Translate may return empty string or None

    # ✅ Test: Fetching a word definition (valid word)
    def test_get_definition_valid(self):
        definition = get_definition("hello")
        self.assertIsNotNone(definition)
        self.assertIsInstance(definition, str)  # Should return a string

    # ✅ Test: Fetching a word definition (invalid word)
    def test_get_definition_invalid(self):
        definition = get_definition("asjkdhasd")  # Random gibberish word
        self.assertIsNone(definition)  # Should return None

    # ✅ Test: `/translate` API call (valid country)
    def test_translate_api_valid(self):
        response = self.app.post("/translate", data=json.dumps({"country": "France"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("translated_word", data)
        self.assertIsInstance(data["translated_word"], str)  # Should be a string

    # ✅ Test: `/translate` API call (invalid country)
    def test_translate_api_invalid(self):
        response = self.app.post("/translate", data=json.dumps({"country": "UnknownLand"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["translated_word"], "Language not found for this country.")

    # ✅ Test: `/translate` API call (missing country key)
    def test_translate_api_missing_country(self):
        response = self.app.post("/translate", data=json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["translated_word"], "Language not found for this country.")

    # ✅ Test: Invalid request type (GET instead of POST)
    def test_translate_api_invalid_method(self):
        response = self.app.get("/translate")  # Should be a POST request
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

if __name__ == "__main__":
    unittest.main()
