#!/usr/bin/env python
#
# Script to receive syslog message containing Json Paylod wiht temp data and write it on dynamodb
# 
# Start rtl_433:
#       rtl_433 -C si -F syslog:127.0.0.1:1433
# then start this script

from __future__ import print_function

import json
from logging import error
import boto3
import time
import datetime
import os

# arn:aws:dynamodb:us-east-2:501205572558:table/temp
def put_temp(data, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('temp_transmitter')

        response = table.put_item(Item=data)
    except:
        return None

    return response

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
    PushData("./tempread/")