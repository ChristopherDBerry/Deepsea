#!/usr/bin/env python3

import requests
import time
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', '--delay', type=int, default=1000, help='Delay in ms between requests')
parser.add_argument('-f', '--file', type=str, default='DBdataset.csv', help='File to read data from')
parser.add_argument('-u', '--url', type=str, default="http://web:8000/api/sensor/upload-sensor-data/", help='File to read data from')
args = parser.parse_args()

url = args.url
headers = {'Content-type': 'application/json'}

with open(args.file) as f:
    lines = f.readlines()

for line in lines:
    data = {'sensors': line}
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 201:
        print(f"Successfully sent data: {line}")
    else:
        print(f"Error sending data: {line}")
    time.sleep((args.delay / 1000.0))