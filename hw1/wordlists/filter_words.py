import requests
import time

INPUT_FILE = "words.txt"
OUTPUT_FILE = "new_words.txt"
API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def has_definition(word):
    """Checks if a word has a definition in the dictionary API."""
    response = requests.get(API_URL + word)
    return response.status_code == 200  # If 200, the word exists

def filter_words():
    """Filters out words without definitions and saves valid words."""
    with open(INPUT_FILE, "r") as infile:
        words = [word.strip() for word in infile.readlines()]

    valid_words = []

    for i in range(1000):
        word = words[i]
        if has_definition(word):
            valid_words.append(word)
            print(f"✔ Found: {word}")  # Show progress
        else:
            print(f"❌ Skipping: {word}")

        time.sleep(0.5)  # Delay to avoid rate limits

    # Save filtered words
    with open(OUTPUT_FILE, "w") as outfile:
        outfile.write("\n".join(valid_words))

    print(f"\n✅ Filtering complete! {len(valid_words)} words saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    filter_words()
