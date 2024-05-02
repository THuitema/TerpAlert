import requests
from bs4 import BeautifulSoup


def build_url(base_url, location_num):
    # replace date vars with generating the current date
    month = 5
    day = 1
    year = 2024
    return base_url + "/?locationNum=" + str(location_num) + "&dtdate=" + str(month) + "/" + str(day) + "/" + str(year)


def process_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    menu_items = soup.find_all("a", class_="menu-item-name")  # list of "a" tags w/ class "menu-item-name"
    for item in menu_items:
        print(item.text)

