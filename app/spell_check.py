import requests


def check_spelling(text):
    response = requests.post(
        "https://speller.yandex.net/services/spellservice.json/checkText",
        data={"text": text},
    )
    corrections = response.json()
    for correction in corrections:
        text = text.replace(correction["word"], correction["s"][0])
    return text
