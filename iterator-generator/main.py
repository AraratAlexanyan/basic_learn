# --------------- Password Generator ---------------
import json
import random

import requests


def pass_generator(length):
    upper = [chr(x) for x in range(65, 91)]
    lower = [chr(x) for x in range(97, 123)]
    digit = [chr(x) for x in range(48, 58)]
    password = ''

    for _ in range(length + 1):
        password += random.choice(upper + lower + digit)
    yield password


print(next(pass_generator(7)))


# --------------- Quotes Generator ---------------

def quotes_api_generator():
    url = 'https://zenquotes.io/api/random'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as r_ex:
        print('Something went wrong', r_ex)
        return

    if r.status_code == 200:
        try:
            response = r.content
        except Exception as ex:
            print('Error...', ex)
            return
        data = json.loads(response)
        yield data[0]['q']


print(next(quotes_api_generator()))

