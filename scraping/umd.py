import requests
from bs4 import BeautifulSoup
from db import db_select

BASE_URL = "https://nutrition.umd.edu"
MENU_TAG = "a"
MENU_CLASS = "menu-item-name"


class DiningHall:
    def __init__(self, name, location_num):
        self.name = name
        self.location_num = location_num
        self.__url = self.__create_url()
        self.menu = self.__get_menu()
        # self.__menu_requested = False

    def __create_url(self):
        month = 5  # make these dynamic later
        day = 2
        year = 2024
        return BASE_URL + "/?locationNum=" + str(self.location_num) + "&dtdate=" + str(month) + "/" + str(
            day) + "/" + str(year)

    def __get_menu(self):
        page = requests.get(self.__url)
        soup = BeautifulSoup(page.content, "html.parser")

        items = set()
        for line in soup.find_all(MENU_TAG, class_=MENU_CLASS):
            items.add(line.text)

        return items

    # def print_menu(self):
    #     for item in self.menu:
    #         print(item)
    #
    # def menu_contains(self, item: str, partial_check: bool) -> bool:
    #     if not partial_check:
    #         return item in self.menu
    #
    #     for entry in self.menu:
    #         if item in entry:
    #             return True
    #
    #     return False
    #
    # def get_items_by_keyword(self, item: str) -> [str]:
    #     items = list()
    #     for entry in self.menu:
    #         if item in entry:
    #             items.append(entry)
    #
    #     return items
    #
    def check_for_alerts(self, conn):  # , fields, table, conditions
        for item in self.menu:
            item = item.replace("'", "''")  # Replace single quotes w/ double quotes (required for SQL)
            query = '''
                SELECT DISTINCT "Users".id, "Users".email, "Keyword".keyword
                FROM "Users"
                INNER JOIN "Keyword"
                ON "Users".id IN (
                    SELECT user_id
                    FROM "Keyword"
                    WHERE keyword = %s
                )
                WHERE "Keyword".keyword = %s
            '''
            # condition = "keyword = '{0}'".format(item)
            rows = db_select(conn, query, item, item)  # fields='*', table='Keyword', conditions=condition
            for row in rows:
                print("User {0}: alert for {1} at {2} dining hall".format(row[0], row[2], self.name))


'''
scrape menu for each dining hall, store in (three?) SET(s?)
	for each dining hall:
		for each item in menu:
			get rows in Keyword where keyword = item
			for each row:
				print(user id and phone# (from Users), keyword, dining hall)
	
'''
