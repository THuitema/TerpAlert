from soup import build_url, process_page

LOCATION_NUMS = {"SOUTH": 16, "YAHENTAMITSI": 19, "251": 51}
BASE_URL = "https://nutrition.umd.edu"


def main():
    url = build_url(base_url=BASE_URL, location_num=LOCATION_NUMS["251"])
    process_page(url)


if __name__ == "__main__":
    main()
