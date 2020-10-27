#!/usr/bin/env python3
#
# Script to read json data from files and push to a dynamodb table
# delete the file if the push was ok

from __future__ import print_function

import json
from logging import error
import boto3
import time
import datetime
import os

# Function to push data to a dynamoDB table
def put_temp(data, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('temp_transmitter')

        response = table.put_item(Item=data)
    except:
        return None

    return response

# Function to loop in each 60 seconds to get new reading and push to a dynamodb
def PushData(path):
    while True:
        time.sleep(60)
        print(datetime.datetime.now())
        print("Processing files in: " + path)

        for filename in filter(lambda x: x.endswith('.json'), os.listdir(path)):
            f = open(path + filename, "r")
            try:
                payload = json.loads(f.read())
            except:
                payload = None
                print("Bad content in  file " + filename)
                os.rename(path + filename, path + filename + ".err")
            f.close()

            if payload is not None:
                dynameDBResp = put_temp(payload)
                if dynameDBResp['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(payload)
                    os.remove(path + filename)
                else:
                    print(dynameDBResp)
        print("End processing\n")

if __name__ == "__main__":
    path = "./tempread/"
    try:
        os.mkdir(path)
    except:
        pass
    PushData(path)