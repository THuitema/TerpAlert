import requests
import os

MAILGUN_API = os.environ['MAILGUN_API']


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/terpalert.xyz/messages",
        auth=("api", MAILGUN_API),
        data={"from": "Excited User <mailgun@terpalert.xyz>",
              "to": ["thuitema35@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness! From, TerpAlert"})
