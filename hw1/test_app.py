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

    # ✅ Test: Fetching country language code
    def test_get_country_language_code(self):
        self.assertEqual(get_country_language_code("France"), "fr")  # French
        self.assertEqual(get_country_language_code("Japan"), "ja")  # Japanese
        self.assertEqual(get_country_language_code("India"), "hi")  # Hindi

    # ✅ Test: Translate a word using Google Translate API
    def test_translate_word(self):
        english_word = "hello"
        translation = translate_word(english_word, "es")  # Spanish
        self.assertNotEqual(translation, "hello")  # Should not return the same word
        self.assertIsInstance(translation, str)  # Should return a string

    # ✅ Test: Fetching a word definition
    def test_get_definition(self):
        definition = get_definition("hello")
        self.assertIsNotNone(definition)
        self.assertIsInstance(definition, str)  # Should return a string

    # ✅ Test: `/translate` API call
    def test_translate_api(self):
        response = self.app.post("/translate", data=json.dumps({"country": "France"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("translated_word", data)
        self.assertIsInstance(data["translated_word"], str)  # Should be a string

if __name__ == "__main__":
    unittest.main()
