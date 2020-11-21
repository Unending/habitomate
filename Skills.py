# API details: https://habitica.com/#/options/settings/api
# API docs: https://habitica.com/apidoc/

import requests
import ConfigParser
import time

from utils import *

config = ConfigParser.RawConfigParser()
config.read("config.ini")

HABITICA_USER = config.get("AUTH", "HABITICA_USER")
HABITICA_TOKEN = config.get("AUTH", "HABITICA_TOKEN")
auth_headers = {"x-api-user": HABITICA_USER, "x-api-key": HABITICA_TOKEN}
spellId = "fireball"


def getUP():
    r = requests.get(
        "https://habitica.com/api/v3/user", headers=auth_headers)
    rateLimit(r)
    return r


def getParty():
    r = requests.get(
        "https://habitica.com/api/v3/groups/party", headers=auth_headers)
    rateLimit(r)
    return r


def targetId():
    r = requests.get(
        "https://habitica.com/api/v3/tasks/user?type=dailys", headers=auth_headers)
    rateLimit(r)

    tasks = {}
    for task in r.json()["data"]:
        tasks["{_id}".format(**task)] = float("{value}".format(**task))

    return max(tasks, key=tasks.get)


userMana = float(getUP().json()["data"]["stats"]["mp"])
quest = getParty().json()["data"]["quest"]
quest_active = quest["active"]

def pendingDMG():
    return float(getUP().json()["data"]["party"]["quest"]["progress"]["up"])


def bossHP():
    return float(getParty().json()["data"]["quest"]["progress"]["hp"])


# QUEST CAST SPELLS
if quest_active and not quest["progress"]["collect"]:
    while (userMana >= 10 and (bossHP() - pendingDMG() > 0)):
        r = requests.post(
            "https://habitica.com/api/v3/user/class/cast/" + spellId + "?targetId=" + targetId(), headers=auth_headers)
        if r.status_code == 200:
            print("Casted spell \"" + spellId + "\"" + " (boss damage)")
            userMana -= 10
        if r.status_code >= 400:
            print("Failed to cast spell: " + r.json()["message"])
        rateLimit(r)
    print("Boss HP remaining: " + str(max(0, round((bossHP() - pendingDMG())))))

# MANA BURNOFF CAST SPELLS
maxMP = float(getUP().json()["data"]["stats"]["maxMP"])

while userMana > maxMP * 0.9:
    r = requests.post(
        "https://habitica.com/api/v3/user/class/cast/" + spellId + "?targetId=" + targetId(), headers=auth_headers)
    if r.status_code == 200:
        print("Casted spell \"" + spellId + "\"" + " (mana burnoff)")
        userMana -= 10
    if r.status_code >= 400:
        print("Failed to cast spell: " + r.json()["message"])
    rateLimit(r)

print("Mana remaining: " + str(round(userMana)))
