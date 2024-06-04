import requests
from bs4 import BeautifulSoup
from db import db_select, db_write
from datetime import date

# Constants for web scraping
BASE_URL = "https://nutrition.umd.edu"
MENU_TAG = "a"
MENU_CLASS = "menu-item-name"


class DiningHall:
    """Stores information pertaining to a dining hall and functionality to web scrape menu data

    Attributes
    __________
    name : str
        name of the dining hall
    location_num : int
        identifier used by the dining hall website
    menu: set[str]
        contains items in the menu of the dining hall
    """

    def __init__(self, name: str, location_num: int):
        """Initializes the DiningHall object and generates menu
        :param name: name of the dining hall
        :param location_num: identifier used by the dining hall website
        """
        self.name = name
        self.location_num = location_num
        self.__url = self.__create_url()
        self.menu = self.__get_menu()

    def __create_url(self) -> str:
        """Returns the url to the menu of the dining hall, on the specified date

        :return: str, the url
        """
        month = date.today().month
        day = date.today().day
        year = date.today().year
        return BASE_URL + "/?locationNum=" + str(self.location_num) + "&dtdate=" + str(month) + "/" + str(
            day) + "/" + str(year)

    def __get_menu(self) -> set[str]:
        """Scrapes each menu item from the dining hall website

        :return: set containing each menu item from the dining hall website
        """
        # Set up web scraper
        page = requests.get(self.__url)
        soup = BeautifulSoup(page.content, "html.parser")

        items = set()

        # Iterate through each menu item found in webpage, add to items set
        for line in soup.find_all(MENU_TAG, class_=MENU_CLASS):
            items.add(line.text)

        return items


class Menu:
    """Represents the combined menu of all dining halls and interacts with database

    Attributes
    __________
    dining_halls : [DiningHall]
        list of DiningHall objects
    total_menu : {str : Item}
        dictionary mapping menu items to Item objects
    users_to_alert : {int : User}
        dictionary mapping user_ids to User objects

    Methods
    _________
    create_menu()
        Combines menus from each dining hall into one, storing result in total_menu
    check_for_alerts(conn)
        Checks with database if there are users to alert, storing result in users_to_alert
    alert_users()
        Notifies users that have alerts
    """
    def __init__(self, dining_halls: [DiningHall]):
        """Initializes the Menu object

        :param dining_halls: list of DiningHall objects
        """
        self.dining_halls = dining_halls
        self.total_menu = {}
        self.users_to_alert = {}

    def create_menu(self):
        """Combines menus from each dining hall into one, storing result in total_menu"""
        for dining_hall in self.dining_halls:
            for item in dining_hall.menu:
                if item in self.total_menu:
                    # if item has already been seen, add current dining hall to its list
                    self.total_menu[item].dining_halls.append(dining_hall.name)
                else:
                    # otherwise, create new Item object and initialize its list with current dining hall
                    self.total_menu[item] = Item(item)
                    self.total_menu[item].dining_halls = [dining_hall.name]

    def check_for_alerts(self, conn):
        """Checks with database if there are users to alert, storing result in users_to_alert

        :param conn: psycopg2.extensions.connection
        """
        for item_name, obj in self.total_menu.items():
            item_name = item_name.replace("'", "''")  # replaces single quotes w/ double quotes (SQL req.)

            # Get users from database that want to be alerted to the current item
            # TODO: update this method to the correct tables
            query = '''
                SELECT *
                FROM accounts_profile
                WHERE id IN (
                    SELECT user_id
                    FROM accounts_alert
                    WHERE menu_item_id in (
                        SELECT id
                        FROM accounts_menu
                        WHERE item=%s
                    )
                )
            '''

            rows = db_select(conn, query, item_name)  # Perform database operation

            for row in rows:  # Iterate through database rows returned
                user_id = row[0]
                if user_id in self.users_to_alert:
                    # if user has already been seen, add alert to their list
                    self.users_to_alert[user_id].alerts.append(obj)
                else:
                    # otherwise, create new User object and initialize its list with current alert
                    self.users_to_alert[user_id] = User(row)
                    self.users_to_alert[user_id].alerts = [obj]

    def alert_users(self):
        """Notifies users that have alerts"""
        # TODO: notify users via their contact info, instead of the python console
        out = ''
        # Calls __str__() for each User object in users_to_alert
        for user_id, obj in self.users_to_alert.items():
            out += str(obj) + '\n'
        print(out)

    def update_db_menu(self, conn):
        """Insert new menu items to Menu table in database

        :param conn: psycopg2.extensions.connection
        """
        for key in self.total_menu.keys():
            query = '''
                INSERT INTO accounts_menu (item)
                SELECT %s
                WHERE NOT EXISTS (SELECT * FROM accounts_menu WHERE item=%s)
            '''
            db_write(conn, query, key, key)

    def __str__(self):
        """Returns each item from menu, along with which dining halls are serving them

        :return: str
        """
        out = ''
        # Calls the __str__() for each Item in total_menu
        for item_name, obj in self.total_menu.items():  # item_list
            out += str(obj) + '\n'
        return out


class Item:
    """Represents a menu item and dining halls associated with it

    Attributes
    __________
    name : str
        name of the item
    dining_halls : [str]
        names of the dining halls at which the item is being served
    """
    def __init__(self, name: str):
        """Initializes Item object

        :param name: str
        """
        self.name = name
        self.dining_halls = []

    def __str__(self):
        """Returns item name, along with which dining halls are serving it

        :return: str
        """
        out = '{0} at '.format(self.name)
        out += ', '.join(self.dining_halls)
        return out


class User:
    """Represents a User of the app

    Attributes
    __________
    info : object
        any information pertaining to user that is returned by database
    alerts : [Item]
        list of Item objects that the user should receive an alert for

    """
    def __init__(self, info: object):
        """Initializes User object

        :param info: any information pertaining to user, returned by database
        """
        self.info = info
        self.alerts = []

    def __str__(self):  # use this to alert user by email/sms later?
        """Returns the alert(s) for the user

        :return: str
        """
        out = 'Alert(s) for {0}\n'.format(self.info)
        # Calls __str__() of each Item object in alerts
        for alert in self.alerts:
            out += '\t{0}\n'.format(str(alert))
        return out


