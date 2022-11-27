import json
import os
import sys
from sqlite3 import Error
import sqlite3


class DataBaseHelper:

    def __init__(self):

        self.connection = None

        self.path = path = os.path.join(os.getcwd(), "data/")
        data_base = path + '/film_data.db'

        try:
            self.connection = sqlite3.connect(data_base)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)
            sys.exit()

        # self.__modify_db()

    def find_by_name(self, start_with: str):

        db_query = f"""SELECT * FROM film_data WHERE title LIKE '{start_with}%' """
        try:
            result = self.cursor.execute(db_query)
            return result.fetchall()
        except Error as e:
            print(e)
            sys.exit()

    def find_largest_duration(self, count=1):

        db_query = """SELECT * FROM film_data ORDER BY length desc"""
        try:
            res = self.cursor.execute(db_query)
            return res.fetchmany(count)
        except Error as e:
            print(e)
            sys.exit()

    def save_to_json(self):

        db_query = """SELECT * FROM film_data"""
        try:
            data = self.cursor.execute(db_query)
            table = data.fetchall()
        except Error as e:
            print(e)
            sys.exit()

        dict_list = []
        for item in table:
            dct = {'film_id': item[0], 'title': item[1], 'description': item[2],
                   'release_year': item[3], 'length': item[4], 'rate': item[5], 'special_features': item[6]}
            dict_list.append(dct)

        with open(self.path + 'data.json', 'w') as file:
            pass

        with open(self.path + 'data.json', 'a') as jsn:
            json.dump(dict_list, jsn, indent=4)

    # def __modify_db(self):
    #     update_r = """UPDATE film_data SET rate = 3 WHERE  rate='R'"""
    #     update_g = """UPDATE film_data SET rate = 4 WHERE  rate='G'"""
    #     update_pg = """UPDATE film_data SET rate = 5 WHERE  rate='PG'"""
    #     update_nc = """UPDATE film_data SET rate = 5 WHERE  rate='NC-17'"""
    #     update_pg13 = """UPDATE film_data SET rate = 1 WHERE  rate='PG-13'"""
    #     self.cursor.execute(update_r)
    #     self.cursor.execute(update_g)
    #     self.cursor.execute(update_pg)
    #     self.cursor.execute(update_nc)
    #     self.cursor.execute(update_pg13)
    #     self.connection.commit()

    def filter_to_table(self, year_start=2010, rate_start=3):

        select = f"""SELECT * FROM film_data WHERE rate >={rate_start} AND  release_year >={year_start}"""
        try:
            res = self.cursor.execute(select).fetchall()
        except Error as e:
            print(e)
            sys.exit()

        make_table = """CREATE TABLE IF NOT EXISTS filtered_table (                       
                        film_id integer PRIMARY KEY AUTOINCREMENT,
                        title text NOT NULL,
                        description text NOT NULL,
                        release_year integer NOT NULL,
                        length integer NOT NULL,
                        rate integer NOT NULL,
                        special_features text NOT NULL);"""

        try:
            self.cursor.execute(make_table)
        except Error as e:
            print(e)
            sys.exit()

        for item in res:
            insert_query = f"""INSERT INTO filtered_table(title, description, release_year, length, rate, special_features)
                                       VALUES (?,?,?,?,?,?);"""
            self.cursor.execute(insert_query, (item[1], item[2], item[3], item[4], item[5], item[6]))

        self.connection.commit()


t = DataBaseHelper()
t.filter_to_table()
t.save_to_json()

