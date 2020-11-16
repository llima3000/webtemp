import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
import os
from decimal import *

path = "/opt/temp_dynamodb/tempread/"

def get_temp_list(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('temp_transmitter')
    
    try:
        scan = table.scan()

    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    
    with table.batch_writer() as batch:
        for each in scan['Items']:
            payload = each #json.loads(item)
            payload["temperature_C"] = int(each["temperature_C"])
            if "humidity" in payload:
                payload["humidity"] = int(each["humidity"])
            filename = payload["transmitter"] + "-" + payload["time"].replace(":","-").replace(" ","-") + ".json"
            f = open(path + filename, "w")
            f.write(json.dumps(payload))
            f.close()

            batch.delete_item(
                Key={
                    'transmitter': each['transmitter'],
                    'time': each['time']
                })
            print("exported: ", filename, each['transmitter'], each['time'])

if __name__ == "__main__":
    try:
        os.mkdir(path)
    except:
        pass
    for i in range(10):
        result = get_temp_list()