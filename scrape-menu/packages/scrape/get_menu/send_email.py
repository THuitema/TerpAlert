import requests
import os
import json

MAILGUN_API = os.environ['MAILGUN_API']


def send_simple_message():
    from_email = "Excited User <" + os.environ['MAILGUN_EMAIL'] + ">"
    return requests.post(
        os.environ['MAILGUN_URL'],
        auth=("api", MAILGUN_API),
        data={"from": from_email,
              "to": ["thuitema35@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness! From, TerpAlert"})


def send_alert(to_email: str, alerts: list[str]):
    from_email = "TerpAlert <" + os.environ['MAILGUN_EMAIL'] + ">"
    template = "Alert email 2"
    return requests.post(
        os.environ['MAILGUN_URL'],
        auth=("api", MAILGUN_API),
        data={"from": from_email,
              "to": [to_email],
              "subject": "You have dining hall alerts!",
              "template": template,
              "t:variables": '{"alerts": ' + json.dumps(alerts) + '}'
              })
