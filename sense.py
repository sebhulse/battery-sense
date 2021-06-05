from time import localtime, strftime
from os import getenv
from requests import post
import json
from dotenv import load_dotenv
from psutil import sensors_battery
import sys

# get env variables for Notion - requires a .env file with NOTION_AUTH (auth key) and NOTION_DB (database id) in
battery = sensors_battery()
load_dotenv('.env')
NOTION_AUTH = getenv('NOTION_AUTH')
NOTION_DB = getenv('NOTION_DB')

# get values to push to database
percent = battery.percent / 100
secsleft = battery.secsleft
plugged = battery.power_plugged
time = strftime("%a, %d %b %Y %H:%M:%S", localtime())

if percent == 1.0:
    sys.exit('100% battery')


# converts seconds to hours:minutes:seconds
def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


if plugged:
    plugged = 'Yes'
else:
    plugged = 'No'

# if plugged in, seconds left = 0
if secsleft < 0:
    secsleft = 0

# create new page in notion database
url = 'https://api.notion.com/v1/pages'
# properties of database: 'Name': local time, 'Percent': battery percent, 'Time Left': estimated time left on battery in hh:mm:ss, 'Plugged In': plugged in to power status
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
# auth, notion version and content type
headers = {'Authorization': 'Bearer ' + NOTION_AUTH,
           'Notion-Version': '2021-05-13',
           'Content-Type': 'application/json'}
# try pushing to database for 5s
try:
    r = post(url, data=json.dumps(body), headers=headers, timeout=5)
    if r.status_code == 200:
        print("Success")
    else:
        print("Error", r.status_code)
except:
    print("Error pushing to notion")
