import os
import requests
import string
import json
from bs4 import BeautifulSoup
from tqdm import tqdm


DICTIONARY_URL = "https://latin-dictionary.net/list/letter/"


def redownload_data():
    latin_words = {}
    alphabet = string.ascii_lowercase
    total_letters = len(alphabet)

    with tqdm(total=total_letters, desc="Progress", unit="letter") as progress_bar:
        for letter in alphabet:
            req = requests.get(DICTIONARY_URL + letter)
            soup = BeautifulSoup(req.text, "html.parser")
            word_set = set()

            word_items = soup.find_all('li', class_='word')

            for item in word_items:
                word = item.find('a').text.split(',')[0].strip()
                word_set.add(word)

            latin_words[letter] = word_set
            progress_bar.update(1)

    if not os.path.exists('data'):
        os.makedirs('data')

    for letter, word_set in latin_words.items():
        word_list = sorted(list(word_set), key=str.lower)
        data = {
            'letter': letter,
            'words': word_list
        }
        filename = f'data/{letter}.json'
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    print("Data redownloaded successfully!")


def browse_saved_data():
    letter = input("Enter a letter: ").lower()
    min_length = int(input("Enter the minimum word length: "))
    max_length = int(input("Enter the maximum word length: "))

    filename = f"data/{letter}.json"
    if not os.path.isfile(filename):
        print(f"No saved data found for the letter '{letter}'.")
        return

    with open(filename, 'r') as file:
        data = json.load(file)
        word_list = data['words']

    filtered_words = [
        word for word in word_list if min_length <= len(word) <= max_length]

    for word in filtered_words:
        print(word)


if __name__ == "__main__":
    while True:
        print("Options:")
        print("1. Redownload all data")
        print("2. Browse saved data")
        print("3. Exit")

        option = input("Select an option (1, 2, or 3): ")

        if option == "1":
            redownload_data()
        elif option == "2":
            browse_saved_data()
        elif option == "3":
            break
        else:
            print("Invalid option. Please select either 1, 2, or 3.")
