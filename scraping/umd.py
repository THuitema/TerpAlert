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


class Menu:
    def __init__(self, dining_halls: [DiningHall]):
        self.dining_halls = dining_halls
        self.discovered_items = []  # type string
        self.item_list = []  # type Item

    def create_menu(self):
        for dining_hall in self.dining_halls:  # iterate through dining halls
            for item in dining_hall.menu:  # iterate through each menu item
                # if item has already been seen, add current dining hall to its list
                if item in self.discovered_items:
                    for obj in self.item_list:
                        if obj.name == item:
                            obj.dining_halls.append(dining_hall.name)
                            break

                else:  # new item
                    self.discovered_items.append(item)
                    item_obj = Item(item)
                    item_obj.dining_halls.append(dining_hall.name)
                    self.item_list.append(item_obj)
        print("Number of unique items: {0}".format(len(self.item_list)))

    def __str__(self):
        out = ''
        for item in self.item_list:
            out += str(item) + '\n'
        return out


class Item:
    def __init__(self, name):
        self.name = name
        # self.atYahentamitsi = False
        # self.atSouth = False
        # self.at251 = False
        self.dining_halls = []

    # def __build_list(self):
    #     if self.atYahentamitsi:
    #         self.dining_halls.append('Yahentamitsi')
    #     if self.atSouth:
    #         self.dining_halls.append('South')
    #     if self.at251:
    #         self.dining_halls.append('251')

    def __str__(self):
        # self.__build_list()
        out = '{0} at '.format(self.name)
        out += ', '.join(self.dining_halls)
        return out




