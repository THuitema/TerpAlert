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
        self.discovered_users = []
        self.total_menu = {}  # item name mapping to Item obj
        self.users_to_alert = {}  # user_id mapping to User obj

    def create_menu(self):
        for dining_hall in self.dining_halls:  # iterate through dining halls
            for item in dining_hall.menu:  # iterate through each menu item
                # if item has already been seen, add current dining hall to its list
                if item in self.total_menu:
                    self.total_menu[item].dining_halls.append(dining_hall.name)
                else:
                    self.total_menu[item] = Item(item)
                    self.total_menu[item].dining_halls = [dining_hall.name]

    def check_for_alerts(self, conn):
        for item_name, obj in self.total_menu.items():
            item_name = item_name.replace("'", "''")  # replaces single quotes w/ double quotes (SQL req.)

            query = '''
                SELECT *
                FROM "Users"
                WHERE id IN (
                    SELECT user_id
                    FROM "Keyword"
                    WHERE keyword = %s
                )
            '''
            rows = db_select(conn, query, item_name)

            for row in rows:
                user_id = row[0]
                if user_id in self.users_to_alert:
                    self.users_to_alert[user_id].alerts.append(obj)
                else:
                    self.users_to_alert[user_id] = User(row)
                    self.users_to_alert[user_id].alerts = [obj]

    def alert_users(self):
        out = ''
        for user_id, obj in self.users_to_alert.items():
            out += str(obj) + '\n'
        print(out)

    def print_item(self, item):
        out = '{0} at '.format(item)
        out += ', '.join(self.total_menu[item])
        return out

    def __str__(self):
        out = ''
        for item_name, obj in self.total_menu.items():  # item_list
            out += str(obj) + '\n'
        return out


class Item:
    def __init__(self, name):
        self.name = name
        self.dining_halls = []

    def __str__(self):
        out = '{0} at '.format(self.name)
        out += ', '.join(self.dining_halls)
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


