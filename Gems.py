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

returnMessage = "+1 Gem"

while returnMessage == "+1 Gem":
    r = requests.post("https://habitica.com/api/v3/user/purchase/gems/gem", headers=auth_headers)
    returnMessage = r.json()['message']
    print(returnMessage)
    rateLimit(r)
