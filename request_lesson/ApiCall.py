import requests
import os
import json

# temp = 'https://raw.githubusercontent.com/AraratAlexanyan/Json/master/list.json'


class ApiCall:

    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def make_call(self, base_url: str):

        try:
            r = requests.get(base_url)
        except Exception as ex:
            print('Something went wrong: \n' + ex)
        else:
            response = r.content
            return response

    def load_images(self):

        json_data = json.loads(self.make_call(self.base_url))

        for item in json_data:
            name = item['name']
            image_url = item['image-url']

            if image_url.endswith('.jpg') or image_url.endswith('.jpeg'):
                dir_type = 'jpg'
            elif image_url.endswith('.png'):
                dir_type = 'png'

            image_data = self.make_call(image_url)

            self.make_images(image_data, name, dir_type)

    def make_images(self, image_data, name, dir_type):

        path = f'{dir_type}/{name}.{dir_type}'

        try:
            os.mkdir(dir_type)
        except FileExistsError:
            pass

        with open(path, 'wb') as image:
            image.write(image_data)


# test
url = "https://raw.githubusercontent.com/AraratAlexanyan/Json/master/list.json"

api = ApiCall(url)

api.load_images()
