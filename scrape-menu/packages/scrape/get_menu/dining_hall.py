from datetime import date
import requests
from bs4 import BeautifulSoup
from db import db_select, db_write
from send_email import send_simple_message, send_alert

# Constants for web scraping
BASE_URL = "https://nutrition.umd.edu"
MENU_TAG = "a"
MENU_CLASS = "menu-item-name"


class DiningHall:
    """
    Stores information pertaining to a dining hall and functionality to web scrape menu data

    Attributes
    __________
    name : str
        name of the dining hall
    location_num : int
        identifier used by the dining hall website
    menu: set[str]
        contains items in the menu of the dining hall

    Methods
    _________
    get_url()
        Returns the url to the current dining hall's menu for today
    scrape_menu()
        Returns a set of each menu item
    """

    def __init__(self, name: str, location_num: int):
        """
        Initializes the DiningHall object and generates menu
        :param name: name of the dining hall
        :param location_num: identifier used by the dining hall website
        """
        self.name = name
        self.location_num = location_num
        self.url = self.get_url()
        self.menu = self.scrape_menu()

    def get_url(self) -> str:
        month = date.today().month
        day = date.today().day
        year = date.today().year

        return BASE_URL + "/?locationNum=" + str(self.location_num) + "&dtdate=" + str(month) + "/" + str(
            day) + "/" + str(year)

    def scrape_menu(self) -> set[str]:
        # Set up web scraper
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        items = set()

        # Iterate through each menu item found in webpage, add to items set
        for line in soup.find_all(MENU_TAG, class_=MENU_CLASS):
            items.add(line.text)

        return items


class Menu:
    """
    Represents the combined menu of all dining halls and interacts with database

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

    def __init__(self, dining_halls):
        """
        Initializes the Menu object

        :param dining_halls: list of DiningHall objects
        """
        self.dining_halls = dining_halls
        self.total_menu = {}
        self.users_to_alert = {}

    def create_menu(self):
        """
        Combines menus from each dining hall into one, storing result in total_menu
        """
        for dining_hall in self.dining_halls:
            for item in dining_hall.menu:
                if item in self.total_menu:
                    # if item has already been seen, add current dining hall to its list
                    self.total_menu[item].dining_halls.append(dining_hall.name)
                else:
                    # otherwise, create new Item object and initialize its list with current dining hall
                    self.total_menu[item] = Item(item)
                    self.total_menu[item].dining_halls = [dining_hall.name]

    def update_db_menu(self, conn):
        """
        Insert new menu items to Menu table and all items to Daily Menu table
        :param conn: PostgreSQL database connection
        """

        for key in self.total_menu.keys():
            # Insert new items to Menu table
            menu_insert_query = '''
                INSERT INTO accounts_menu (item)
                SELECT %s
                WHERE NOT EXISTS (SELECT * FROM accounts_menu WHERE item=%s)
            '''
            db_write(conn, menu_insert_query, key, key)

            # Insert all items to Daily Menu table
            at_y = 'Yahentamitsi' in self.total_menu[key].dining_halls
            at_south = 'South' in self.total_menu[key].dining_halls
            at_251 = '251' in self.total_menu[key].dining_halls

            # Get foreign key for menu item
            get_menu_item_query = '''
                SELECT * 
                FROM accounts_menu
                WHERE item=%s
            '''

            rows = db_select(conn, get_menu_item_query, key)
            menu_item_id = rows[0][0]

            daily_menu_insert_query = '''
                INSERT INTO accounts_dailymenu 
                    (menu_item_id, date, yahentamitsi_dining_hall, south_dining_hall, two_fifty_one_dining_hall)
                VALUES
                    (%s, %s, %s, %s, %s)
            '''

            db_write(conn, daily_menu_insert_query, menu_item_id, date.today(), at_y, at_south, at_251)

        return {'Completed': True}

    def get_alerts(self, conn):
        """
        Appends to users_to_alert users with alerts for the current menu
        :param conn: PostgreSQL database connection
        :return dictionary with key = user id, value = list of alerts
        """
        for item_name, item_obj in self.total_menu.items():
            item_name = item_name.replace("'", "''")

            # Returns rows from Profile table that have alerts for current item
            get_alerts_query = '''
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

            rows = db_select(conn, get_alerts_query, item_name)

            # Append users & alerts to users_to_alert dict
            for row in rows:
                user_id = row[0]
                email = str(row[3])
                receive_email_alerts = row[8]  # == 'True'

                if user_id in self.users_to_alert:
                    self.users_to_alert[user_id].alerts.append(item_obj)
                else:
                    self.users_to_alert[user_id] = User(row, email, receive_email_alerts)
                    self.users_to_alert[user_id].alerts = [item_obj]

        return self.users_to_alert

    def alert_users(self):
        """
        Email users that have alerts for the current day menu
        """
        alerted_emails = []
        for user_id, user_obj in self.users_to_alert.items():
            if user_obj.receive_email_alerts:
                send_alert('thuitema35@gmail.com', user_obj.get_alert_list())
                alerted_emails.append(user_obj.email)

        return alerted_emails

    def __str__(self):
        """
        Returns each item from menu, along with which dining halls are serving them

        :return: str
        """
        out = ''
        for item_name, obj in self.total_menu.items():
            out += str(obj) + '\n'
        return out


class Item:
    """
    Represents a menu item and dining halls associated with it

    Attributes
    __________
    name : str
        name of the item
    dining_halls : [str]
        names of the dining halls at which the item is being served
    """

    def __init__(self, name: str):
        """
        Initializes Item object

        :param name: str
        """
        self.name = name
        self.dining_halls = []

    def __str__(self):
        """
        Returns item name, along with which dining halls are serving it

        :return: str
        """
        out = '{0} at '.format(self.name)
        out += ', '.join(self.dining_halls)
        return out


class User:
    """
    Represents a User of the app

    Attributes
    __________
    info : object
        any information pertaining to user that is returned by database
    alerts : [Item]
        list of Item objects that the user should receive an alert for

    """

    def __init__(self, info: object, email: str, receive_email_alerts: bool):
        """
        Initializes User object

        :param info: any information pertaining to user, returned by database
        """
        self.info = info
        self.email = email
        self.alerts = []
        self.receive_email_alerts = receive_email_alerts

    def get_alert_list(self):
        alert_list = []
        for alert in self.alerts:
            alert_list.append(str(alert))

        return alert_list

    def __str__(self):  # use this to alert user by email/sms later?
        """
        Returns the alert(s) for the user

        :return: str
        """
        out = 'Alert(s) for {0}\n'.format(self.email)
        # Calls __str__() of each Item object in alerts
        for alert in self.alerts:
            out += '\t{0}\n'.format(str(alert))
        return out