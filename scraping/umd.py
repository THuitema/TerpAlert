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

    def __create_url(self):
        month = 5  # make these dynamic later
        day = 4
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


class Menu:
    def __init__(self, dining_halls: [DiningHall]):
        self.dining_halls = dining_halls
        self.discovered_items = []  # type string
        self.item_list = []  # type Item
        self.users_to_alert = []  # type User
        self.discovered_users = []

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

    def check_for_alerts(self, conn):
        for item in self.item_list:
            name = item.name.replace("'", "''")  # replace single quotes w/ double quotes (SQL req.)
            query = '''
                SELECT *
                FROM "Users"
                WHERE id IN (
                    SELECT user_id
                    FROM "Keyword"
                    WHERE keyword = %s
                )
            '''
            rows = db_select(conn, query, name)

            for row in rows:
                if row in self.discovered_users:
                    for obj in self.users_to_alert:
                        if obj.info == row:
                            obj.alerts.append(item)
                else:
                    self.discovered_users.append(row)
                    user = User(row)
                    user.alerts.append(item)
                    self.users_to_alert.append(user)

    def alert_users(self):
        out = ''
        for user in self.users_to_alert:
            out += str(user) + '\n'
        print(out)

    def __str__(self):
        out = ''
        for item in self.item_list:
            out += str(item) + '\n'
        return out


class User:
    def __init__(self, info):
        self.info = info
        self.alerts = []

    def __str__(self):  # use this to alert user by email/sms later?
        out = 'Alert(s) for {0}\n'.format(self.info)
        for alert in self.alerts:
            out += '\t{0}\n'.format(str(alert))
        return out


class Item:
    def __init__(self, name):
        self.name = name
        self.dining_halls = []

    def __str__(self):
        out = '{0} at '.format(self.name)
        out += ', '.join(self.dining_halls)
        return out
