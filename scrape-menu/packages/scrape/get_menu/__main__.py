from datetime import date
import requests
from bs4 import BeautifulSoup
import os
from db import connect
from dining_hall import DiningHall, Menu

# Constants for dining hall info
SOUTH = "South"
YAHENTAMITSI = "Yahentamitsi"
TWO_FIFTY_ONE = "251"
HALLS = {SOUTH: 16, YAHENTAMITSI: 19, TWO_FIFTY_ONE: 51}


def main(args):
    return {"conn: ": str(connect())}
    # the_y = DiningHall(name=YAHENTAMITSI, location_num=HALLS[YAHENTAMITSI])
    # south = DiningHall(name=SOUTH, location_num=HALLS[SOUTH])
    # two_fifty_one = DiningHall(name=TWO_FIFTY_ONE, location_num=HALLS[TWO_FIFTY_ONE])
    #
    # menu = Menu([the_y, south, two_fifty_one])
    # menu.create_menu()
    # return {'Total Menu': str(menu)}




