import requests
import os
import json

MAILGUN_API = os.environ['MAILGUN_API']


def send_alert(to_email: str, alerts: list[str], token: str):
    """
    Sends alert email to user using the Mailgun API
    :param to_email: user's email
    :param alerts: list of user's alerts
    :param token: user's authentication token
    :return: JSON response from Mailgun API
    """
    from_email = "TerpAlert <" + os.environ['MAILGUN_EMAIL'] + ">"
    template = "Alert email 2"
    account_auth_url = 'https://terpalert.xyz/accounts/auth/' + token
    unsubscribe_url = 'https://terpalert.xyz/accounts/unsubscribe/' + token

    return requests.post(
        os.environ['MAILGUN_URL'],
        auth=("api", MAILGUN_API),
        data={"from": from_email,
              "to": [to_email],
              "subject": "You have dining hall alerts!",
              "template": template,
              "t:variables": '{"alerts": ' + json.dumps(alerts) + ', "account_auth_url": ' + json.dumps(
                  account_auth_url) + ', "unsubscribe_url": ' + json.dumps(unsubscribe_url) + '}'
              })
