import os
import threading
import requests
import json

from requests import RequestException


class ApiCall:

    def __init__(self, url):
        self.response = None
        self.url = url

    def init_call(self, url: str):
        # print(f'{threading.current_thread().name}')
        try:
            r = requests.get(url)
            self.response = r.content
        except RequestException as ex:
            print('Something went wrong: ', ex)

    def data_parsing(self):

        self.make_thread()
        data = json.loads(self.response)

        for item in data:
            name = item['name']
            image_url = item['image-url']
            self.url = image_url
            self.make_thread()
            make_images(name, self.response)

    def make_thread(self):
        th = threading.Thread(target=self.init_call, args=(self.url,), name="thread_init_call")
        th.start()
        th.join()


def make_images(name: str, image: bytes):
    if not os.path.exists('images'):
        try:
            os.makedirs('images')
        except Exception as ex:
            print(ex)
    with open(f'images/{name}.jpg', 'wb') as file:
        file.write(image)


if __name__ == "__main__":
    # print(f'{threading.current_thread().name}')
    call = ApiCall("https://raw.githubusercontent.com/AraratAlexanyan/Json/master/list.json")
    call.data_parsing()
