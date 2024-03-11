import re
import sys
import time
import argparse
import requests
import http.client

def get_args():
    parser = argparse.ArgumentParser(description="Roblox Clothing Image Finder")
    parser.add_argument("-i", "--id", type=int, help="Sets the Clothing Id")
    parser.add_argument("-s", "--silent", action="store_true", help="Enables silent mode")
    parser.add_argument("-w", "--wait", type=float, default=1, help="Sets the time to wait between requests")
    parser.add_argument("-r", "--retries", type=int, default=10, help="Sets the max amount of retries")
    return parser.parse_args()

args = get_args()

if not any(vars(args).values()):
    print("Please provide arguments. Use -h or --help for more information.")
    sys.exit()

shirt = args.id
silent_mode = args.silent
wait_time = args.wait
max_retries = args.retries

oldId = shirt
imageId = None

try:
    creator = int(requests.get(f"https://economy.roblox.com/v2/assets/{shirt}/details").json()["Creator"]["Id"])
except KeyError:
    print("Please provide arguments. Use -h or --help for more information.")
    sys.exit()

retry_count = 0

while imageId is None and retry_count < max_retries:
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
        elif 400 <= request.status_code < 600:
            print(f"Retrying.. [{retry_count+1}/{max_retries}]")
            retry_count += 1
            time.sleep(wait_time)
        else:
            print(f"{http.client.responses[request.status_code]}: {request.status_code}")
            break
    except Exception as exception:
        print(exception)
    if isinstance(request, dict):
        oldId -= 1
    time.sleep(wait_time)

if retry_count >= max_retries:
    print("Max retries reached. Exiting..")
