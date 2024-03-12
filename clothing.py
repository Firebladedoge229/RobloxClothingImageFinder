import re
import sys
import argparse
import requests
import http.client

def get_args():
    parser = argparse.ArgumentParser(description="Roblox Clothing Image Finder")
    parser.add_argument("-i", "--id", type=int, help="Sets the Clothing Id")
    return parser.parse_args()

args = get_args()

if not any(vars(args).values()):
    print("Please provide arguments. Use -h or --help for more information.")
    sys.exit()

shirt = args.id

id = requests.get(f"https://assetdelivery.roblox.com/v1/assetId/{shirt}")
if id.status_code == 200:
    try:
        id = id.json()["location"]
        shirtRequest = requests.get(id)
        shirt = re.search(r"http://www\.roblox\.com/asset/\?id=(\d+)", shirtRequest.text).group(1)
        print(shirt)
    except Exception as exception:
        exception = str(exception).replace("'", '"')
        if "location" in exception:
            print(f"\033[31mError: \033[0m{exception}.\033[31m Are you sure the Clothing Id is valid?\033[0m")
        elif shirtRequest and shirtRequest.status_code != 200:
            print(f"\033[31mError while sending clothing request: \033[0m{exception}")
        else:
            print(f"\033[31mError: \033[0m{exception}")
else:
    print(f"\033[31m{http.client.responses[id.status_code]}: \033[0m{id.status_code}")
