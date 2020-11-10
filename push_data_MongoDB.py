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

from pymongo import MongoClient

mongoServer = "192.168.0.8"
sleepTime = 60

# Function to loop in each 60 seconds to get new reading and push to a dynamodb
def PushData(path):
    print("Waiting for more data")

    while True:
        time.sleep(sleepTime)
        print("Start Processing: " + str(datetime.datetime.now()))
        client = MongoClient(mongoServer, 27017)

        db = client.tempdb
        tempreadings = db.tempreadings

        for filename in filter(lambda x: x.endswith('.json'), os.listdir(path)):
            f = open(path + filename, "r")
            try:
                payload = json.loads(f.read())
            except:
                payload = None
                print("Bad content in file " + filename)
                os.rename(path + filename, path + filename + ".err")
            f.close()

            if payload is not None:
                '''
                %Y: Year (4 digits)
                %m: Month
                %d: Day of month
                %H: Hour (24 hour)
                %M: Minutes
                %S: Seconds
                %f: Microseconds
                '''
                payload['time'] = datetime.datetime.strptime(payload['time'], '%Y-%m-%d %H:%M:%S')

                tempreading_id = tempreadings.insert_one(payload)

                if tempreading_id.acknowledged:
                    print(str(tempreading_id.inserted_id) + " " + payload["transmitter"] + " " + payload["time"].strftime('%Y-%m-%d %H:%M:%S'))
                    os.remove(path + filename)
                else:
                    print("Object not inserted: " + path + filename)
        print("End processing " + str(datetime.datetime.now()))
        client.close()

if __name__ == "__main__":
    path = "./tempread/"
    PushData(path)
