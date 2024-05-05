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

        self.total_menu = {}

    def create_menu(self):
        for dining_hall in self.dining_halls:  # iterate through dining halls
            for item in dining_hall.menu:  # iterate through each menu item
                # if item has already been seen, add current dining hall to its list
                if item in self.total_menu:
                    self.total_menu[item].append(dining_hall.name)
                else:
                    self.total_menu[item] = [dining_hall.name]

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

    def print_item(self, item):
        out = '{0} at '.format(item)
        out += ', '.join(self.total_menu[item])
        return out

    def __str__(self):
        # out = ''
        # for item in self.item_list:
        #     out += str(item) + '\n'
        # return out
        out = ''
        for item in self.total_menu:
            out += self.print_item(item) + '\n'
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
