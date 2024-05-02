from soup import build_url, process_page
from umd import DiningHall

LOCATION_NUMS = {"SOUTH": 16, "YAHENTAMITSI": 19, "251": 51}

def main():
    # url = build_url(base_url=BASE_URL, location_num=LOCATION_NUMS["251"])
    # process_page(url)
    the_y = DiningHall(name="Yahentamitsi", location_num=LOCATION_NUMS["YAHENTAMITSI"])
    south = DiningHall(name="South", location_num=LOCATION_NUMS["SOUTH"])
    two_fifty_one = DiningHall(name="251", location_num=LOCATION_NUMS["251"])
    # the_y.print_menu()
    print("Does the Y have orange chicken? " + str(the_y.menu_contains(item="Orange Tempura Chicken")))
    print("Does South have steak? " + str(south.menu_contains(item="Steak")))
    print("Does 251 have Avocado Toast? " + str(two_fifty_one.menu_contains(item="Avocado Toast")))


if __name__ == "__main__":
    main()
