import requests

def get_response(word):
    url = "http://agilec.cs.uh.edu/spellcheck?check="
    
    return requests.get(f"{url}{word}").text


def parse(word):
    if word == 'true': return True
    if word == 'false': return False
    raise ValueError("Did not receive true or false")


def is_spelling_correct(guess_word, get_response = get_response):
    response = get_response(guess_word)
    
    return parse(response)
