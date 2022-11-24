import json
from json import JSONDecodeError
from functools import wraps
import requests
from email_validator import validate_email, EmailNotValidError
from requests_file import FileAdapter


class User:

    def __init__(self, user_name, user_pass, user_email, user_age, user_phone) -> None:
        if self.validate_user_name(user_name):
            self.user_name = user_name
        self.user_password = user_pass
        if self.validate_email(user_email):
            self.user_email = user_email
        self.user_age = user_age
        self.user_phone = user_phone
        self.save_data()

    @staticmethod
    def validate_user_name(user_name):
        for i in user_name:
            if not i.isalpha():
                raise TypeError("User name can't contains digits or symbols")
        else:
            return True

    @staticmethod
    def validate_email(user_email: str):

        try:
            validate_email(user_email)
            return True
        except EmailNotValidError as e:
            print('Error, ', e)
            return False

    def save_data(self):

        file1 = open('data.json', 'a+')
        file1.close()

        with open('data.json') as data:
            try:
                user_list = json.load(data)
            except JSONDecodeError:
                user_list = []

        body = {'user_name': self.user_name, 'user_pass': self.user_password, 'user_email': self.user_email,
                'user_age': self.user_age, 'user_phone': self.user_phone}

        if user_list:
            for dct in user_list:
                if dct['user_phone'] == body['user_phone']:
                    break
            else:
                self.__save_data(user_list, body)
        else:
            user_list.append(body)
            self.__save_data(user_list, body)
            del user_list

    @staticmethod
    def __save_data(user_list, body):
        with open('data.json', 'w') as local_data:
            user_list.append(body)
            json.dump(user_list, local_data, indent=4)


user_1 = User('Ararat', '1234567', 'alexanyan.ararat1@gmail.com', 26, '+37493804450')
user_2 = User('Artur', '7654321', 'artur_32@yandex.com', 39, '+37425658441')
user_3 = User('Seroj', 'seroj_123', 'sergey333@gmail.com', 25, '+37401236547')


class PyRequest:
    def __init__(self):
        self.headers = []
        self.body = {}
        self.authorization = None
        self.user = None

    def local_login(self, username: str, password: str):

        with open('data.json') as data:
            try:
                self.headers = json.load(data)
            except JSONDecodeError:
                self.headers = []

        if self.headers:
            for item in self.headers:
                if item['user_name'] == username and item['user_pass'] == password:
                    self.user = item
                    self.body = self.user
                    self.authorization = True

    def login_required(func: callable) -> callable:

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            request_data = json.loads(args[0].text)
            for item, data_item in zip(self.headers, request_data):
                if item == data_item:
                    res = func(self, *args, **kwargs)
                    return res
                else:
                    raise Exception('401 Unauthorized request error')

        return wrapper

    @login_required
    def get_user_info(self, request: requests.get):
        if self.authorization:
            return self.body


p = PyRequest()
name = input('Enter your name')
password = input('Enter your password')
p.local_login(name, password)
s = requests.Session()
s.mount('file://', FileAdapter())

resp = s.get('file:///home/ararat/Desktop/python/basic_homeowrks/decorators/data.json')
print(p.get_user_info(resp))
