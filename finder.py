import re
import time
import requests
import http.client

shirt = int(input("Enter Clothing Id: "))

oldId = shirt
imageId = None

creator = int(requests.get(f"https://economy.roblox.com/v2/assets/{shirt}/details").json()["Creator"]["Id"])

retry_count = 0

while imageId == None and retry_count < 10:
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
        elif 400 <= request.status_code < 600:
            print(f"Retrying.. [{retry_count+1}/10]")
            retry_count += 1
            time.sleep(1)
        else:
            print(f"{http.client.responses[request.status_code]}: {request.status_code}")
            break
    except Exception as exception:
        print(exception)
    if isinstance(request, dict):
        oldId -= 1
    time.sleep(1)

if retry_count >= 10:
    print("Max retries reached. Exiting...")
