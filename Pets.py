# API details: https://habitica.com/#/options/settings/api
# API docs: https://habitica.com/apidoc/

import requests
import ConfigParser
from utils import *

config = ConfigParser.RawConfigParser()
config.read("config.ini")

HABITICA_USER = config.get("AUTH", "HABITICA_USER")
HABITICA_TOKEN = config.get("AUTH", "HABITICA_TOKEN")
auth_headers = {"x-api-user": HABITICA_USER, "x-api-key": HABITICA_TOKEN}

r = requests.get("https://habitica.com/api/v3/user", headers=auth_headers)
hatchingPotionsInventory = r.json()["data"]["items"]["hatchingPotions"]
petsInventory = r.json()["data"]["items"]["pets"]
eggsInventory = r.json()["data"]["items"]["eggs"]
foodInventory = r.json()["data"]["items"]["food"]
mountsInventory = r.json()["data"]["items"]["mounts"]
foodPreferenceList = {"Base": "Meat", "White": "Milk", "Desert": "Potatoe", "Red": "Strawberry", "Shade": "Chocolate", "Skeleton": "Fish", "Zombie": "RottenMeat", "CottonCandyBlue": "CottonCandyBlue", "CottonCandyPink": "CottonCandyPink", "Golden": "Honey"}
action = True


petTypeList = {}
for pets in petsInventory:
    petType = pets.split("-")[0]
    if petsInventory.get(pets) >= 5:
        if petType in petTypeList:
            petTypeList[petType] += 1
        else:
            petTypeList[petType] = 1


for egg in eggsInventory:
    for hatchingPotion in hatchingPotionsInventory:
        pet = egg + "-" + hatchingPotion

        # WHEN HATCHABLE
        if eggsInventory.get(egg) > 0 and hatchingPotionsInventory.get(hatchingPotion) > 0:
            # HATCH PETS
            if pet not in petsInventory or petsInventory.get(pet) == -1:
                r = requests.post(
                    "https://habitica.com/api/v3/user/hatch/" + egg + "/" + hatchingPotion,
                    headers=auth_headers)
                if r.status_code == 200:
                    print(hatchingPotion + " " + egg + " hatched!")
                    eggsInventory[egg] -= 1
                    hatchingPotionsInventory[hatchingPotion] -= 1
                    petsInventory[pet] = "5"
                    if egg in petTypeList:
                        petTypeList[egg] += 1
                    else:
                        petTypeList[egg] = 1
                if r.status_code >= 400:
                    print("Failed to hatch " + hatchingPotion + " " + egg + ": " + r.json()["message"])
                rateLimit(r.headers)

            # FEED PETS
            if petTypeList[egg] >= 10:
                for food in foodInventory:
                    if pet not in mountsInventory and foodInventory.get(food) > 0 and 0 < petsInventory.get(pet) < 50:
                        if hatchingPotion in foodPreferenceList:
                            feed = foodPreferenceList.get(hatchingPotion)
                            foodList = food.split("_")
                            if len(foodList) > 1 and foodList[1] == hatchingPotion:
                                feed = food
                        else:
                            feed = max(foodInventory, key=foodInventory.get)
                        r = requests.post(
                            "https://habitica.com/api/v3/user/feed/" + pet + "/" + feed,
                            headers=auth_headers)
                        if r.status_code == 200:
                            rData = r.json()["data"]
                            print(hatchingPotion + " " + egg + " fed with " + feed + ". Current value: " + str(rData))
                            foodInventory[feed] -= 1
                            petsInventory[pet] = rData
                            petTypeList[egg] -= 1
                            if rData == -1:
                                mountsInventory[pet] = "true"
                        if r.status_code >= 400:
                            print("Failed to feed " + hatchingPotion + " " + egg + ": " + r.json()["message"])
                        rateLimit(r.headers)
