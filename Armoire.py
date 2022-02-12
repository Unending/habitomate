# API details: https://habitica.com/#/options/settings/api
# API docs: https://habitica.com/apidoc/

import requests
import configparser
from utils import rateLimit

config = configparser.RawConfigParser()
config.read("config.ini")

HABITICA_USER = config.get("AUTH", "HABITICA_USER")
HABITICA_TOKEN = config.get("AUTH", "HABITICA_TOKEN")
auth_headers = {"x-api-user": HABITICA_USER, "x-api-key": HABITICA_TOKEN}


def emptyArmoire():
    r = requests.get("https://habitica.com/api/v3/user", headers=auth_headers)
    return r.json()["data"]["flags"]["armoireEmpty"]
    rateLimit(r)


while emptyArmoire() is False:
    r = requests.post("https://habitica.com/api/v3/user/buy-armoire", headers=auth_headers)
    print(r.json()['message'])
    rateLimit(r)
