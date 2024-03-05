import re
import time
import requests

shirt = int(input("Enter Clothing Id: "))

oldId = shirt
imageId = None

html = None

try:
    html = int(re.search(r'data-group-last-edited-by-id="(\d+)"', requests.get(f"https://www.roblox.com/catalog/{str(shirt)}").text).group(1))
except:
    pass

creator = None
isPlayer = html == None

if isPlayer:
    creator = int(requests.get(f"https://economy.roblox.com/v2/assets/{shirt}/details").json()["Creator"]["Id"])
else:
    creator = html

while imageId == None:
    try:
        print(f"Searching {str(oldId - 1)}..")
        request = requests.get(f"https://economy.roblox.com/v2/assets/{oldId - 1}/details")
        if request.status_code == 200:
            request = request.json()
            clothingCreator = int(request["Creator"]["Id"])
            print(f"{creator} v {clothingCreator}")
            if clothingCreator == creator:
                print(f"Found Image: {str(oldId - 1)}")
                imageId = oldId - 1
        else:
            print(request.status_code)
            break
    except Exception as exception:
        print(exception)
    oldId -= 1
    time.sleep(1)