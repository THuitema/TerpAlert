import requests
import os
import json

MAILGUN_API = os.environ['MAILGUN_API']


def send_verification_email(to_email: str, token: str):
    """
    Sends account verification email to user using the Mailgun API
    :param to_email: user's email
    :param token: user's authentication token
    :return: JSON response from Mailgun API
    """
    from_email = "TerpAlert <" + os.environ['MAILGUN_EMAIL'] + ">"
    template = "email verification"
    verification_url = 'https://terpalert.xyz/accounts/verify-email-confirm/' + token

    return requests.post(
        url=os.environ['MAILGUN_URL'],
        auth=("api", MAILGUN_API),
        data={"from": from_email,
              "to": [to_email],
              "subject": "Verify your email",
              "template": template,
              "t:variables": '{"verification_url": ' + json.dumps(verification_url) + '}'
              })

