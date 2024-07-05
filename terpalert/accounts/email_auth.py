import requests
import os
import json

MAILGUN_API = os.environ['MAILGUN_API']


def send_verification_email(to_email: str, token: str):
    from_email = os.environ['MAILGUN_EMAIL']
    template = "email verification"
    verification_url = 'https://terpalert.xyz/accounts/verify-email-confirm/' + token

    return requests.post(
        url=os.environ['MAILGUN_URL'],
        auth=("api", MAILGUN_API),
        data={"from": from_email,
              "to": [to_email],
              "subject": "Verify your account",
              "template": template,
              # "t:variables": '{"alerts": ' + json.dumps(verification_url) + '}'
              })

    # return requests.post(
    #     os.environ['MAILGUN_URL'],
    #     auth=("api", MAILGUN_API),
    #     data={"from": from_email,
    #           "to": [to_email],
    #           "subject": "Verify email",
    #           "template": template,
    #           "t:variables": '{"verification_url": ' + verification_url + '}'
    #           }
    # )
