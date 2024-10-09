import random
import requests


def get_words_from_service():
    url = "https://agilec.cs.uh.edu/words"
    
    return requests.get(url).text


def get_word_list():
    words_text = get_words_from_service()
    
    if not words_text:
        raise ValueError("No words found in response")
    
    return words_text.splitlines()


def shuffle_word_list(word_list):
    random.shuffle(word_list)


def choose_random_index(remaining_indices):
    return random.choice(list(remaining_indices))


def get_a_random_word(word_list):
    if not hasattr(get_a_random_word, "chosen_indices"):
        get_a_random_word.chosen_indices = set()
        shuffle_word_list(word_list)

    remaining_indices = set(range(len(word_list))) - get_a_random_word.chosen_indices

    if not remaining_indices:
        raise ValueError("All words have been chosen")

    chosen_index = choose_random_index(remaining_indices)
    get_a_random_word.chosen_indices.add(chosen_index)

    return word_list[chosen_index]