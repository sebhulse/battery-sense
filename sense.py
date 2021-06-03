from time import localtime, strftime
from os import getenv
from requests import post
import json
from dotenv import load_dotenv
from psutil import sensors_battery

battery = sensors_battery()
load_dotenv('.env')
NOTION_AUTH = getenv('NOTION_AUTH')
NOTION_DB = getenv('NOTION_DB')

percent = battery.percent / 100
secsleft = battery.secsleft
plugged = battery.power_plugged
time = strftime("%a, %d %b %Y %H:%M:%S", localtime())


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


if plugged:
    plugged = 'Yes'
else:
    plugged = 'No'

if secsleft < 0:
    secsleft = 0

url = 'https://api.notion.com/v1/pages'
body = {
    "parent": {"database_id": NOTION_DB},
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": time
                    }
                }
            ]
        },
        "Percent": {
            "number": percent
        },
        "Time Left": {
            "rich_text": [
                {
                    "text": {
                        "content": secs2hours(secsleft)
                    }
                }
            ]
        },
        "Plugged In": {
            "rich_text": [
                {
                    "text": {
                        "content": plugged
                    }
                }
            ]
        }
    }
}
headers = {'Authorization': 'Bearer ' + NOTION_AUTH,
           'Notion-Version': '2021-05-13', 'Content-Type': 'application/json'}
try:
    r = post(url, data=json.dumps(body), headers=headers, timeout=5)
    if r.status_code == 200:
        print("Success")
    else:
        print("Error", r.status_code)
except:
    print("Error pushing to notion")
