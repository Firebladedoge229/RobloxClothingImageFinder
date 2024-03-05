import re
import time
import requests
import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser(description="Roblox Clothing Image Finder")
    parser.add_argument("-i", "--id", type=int, help="Sets the Clothing Id")
    parser.add_argument("-s", "--silent", action="store_true", help="Enables silent mode")
    parser.add_argument("-w", "--wait", type=float, default=1, help="Sets the time to wait between requests")
    return parser.parse_args()

args = get_args()

if not any(vars(args).values()):
    print("Please provide arguments. Use -h or --help for more information.")
    sys.exit()

shirt = args.id
silent_mode = args.silent
wait_time = args.wait

oldId = shirt
imageId = None

html = None

try:
    html = int(re.search(r'data-group-last-edited-by-id="(\d+)"', requests.get(f"https://www.roblox.com/catalog/{str(shirt)}").text).group(1))
except:
    pass

creator = None
isPlayer = html is None

if isPlayer:
    try:
        creator = int(requests.get(f"https://economy.roblox.com/v2/assets/{shirt}/details").json()["Creator"]["Id"])
    except KeyError:
        print("Please provide arguments. Use -h or --help for more information.")
        sys.exit()
else:
    creator = html

while imageId is None:
    try:
        if not silent_mode:
            print(f"Searching {str(oldId - 1)}..")
        request = requests.get(f"https://economy.roblox.com/v2/assets/{oldId - 1}/details")
        if request.status_code == 200:
            request = request.json()
            clothingCreator = int(request["Creator"]["Id"])
            if not silent_mode:
                print(f"{creator} v {clothingCreator}")
            if clothingCreator == creator:
                if silent_mode:
                    print(str(oldId - 1))
                else:
                    print(f"Found Image: {str(oldId - 1)}")
                imageId = oldId - 1
        else:
            print(request.status_code)
            break
    except Exception as exception:
        print(exception)
    oldId -= 1
    time.sleep(wait_time)
