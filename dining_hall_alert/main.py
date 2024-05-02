from . import soup

LOCATION_NUMS = {"SOUTH": 16, "YAHENTAMITSI": 19, "251": 51}
BASE_URL = "https://nutrition.umd.edu"


def main():
    url = soup.build_url(base_url=BASE_URL, location_num=LOCATION_NUMS["SOUTH"])
    print(url)


