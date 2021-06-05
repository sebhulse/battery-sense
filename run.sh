#!/bin/bash
# cronjob every 2 minutes:
# */2 * * * * bash /<insert_path_here>/battery-sense/run.sh

cd /<insert_path_here>/battery-sense

pip3 install --upgrade pip --user
pip3 install requests --user
pip3 install python-dotenv --user
pip3 install psutil --user

/usr/bin/python3 sense.py
