#!/usr/bin/env python3
#
# Script to receive syslog message containing Json Paylod wiht temp data and write it on dynamodb
# 
# Start rtl_433:
#       rtl_433 -C si -F syslog:127.0.0.1:1433
# then start this script

from __future__ import print_function

import socket
import json
import boto3

UDP_IP = "127.0.0.1"
UDP_PORT = 1433

KEYS = [ "Nexus-TH",
         "Companion-WTR001",
         "Bresser-3CH"]

TRANSMITTERS = [ "Nexus-TH.90.2",
                 "Nexus-TH.101.1",
                 "Nexus-TH.254.3",
                 "Companion-WTR001",
                 "Bresser-3CH.133.3"]

def parse_syslog(line):
    """Try to extract the payload from a syslog line."""
    line = line.decode("ascii")  # also UTF-8 if BOM
    if line.startswith("<"):
        # fields should be "<PRI>VER", timestamp, hostname, command, pid, mid, sdata, payload
        fields = line.split(None, 7)
        line = fields[-1]
    return line

# Function to push data to dynamoDB
def put_temp(data, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('temp_transmitter')

        response = table.put_item(Item=data)
    except:
        return None

    return response


def rtl_433_listen():
    """Try to extract the payload from a syslog line."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        line, addr = sock.recvfrom(1024)

        try:
            line = parse_syslog(line)
            data = json.loads(line)
            transmitter = ""

            if "model" in data:
                transmitter = data["model"]
                if "id" in data:
                    transmitter += "." + str(data["id"])

                if "channel" in data:
                    transmitter += "." + str(data["channel"])

            if data["model"] in KEYS:
                #print(transmitter, data)
                payload = {
                            "model": data["model"],
                            "transmitter": transmitter,
                            "time": data["time"],
                            "temperature_C": int(data["temperature_C"]*100)
                          }
                if "humidity" in data:
                    payload["humidity"] = data["humidity"]
                #print(payload)

                dynameDBResp = put_temp(payload)
                if dynameDBResp['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(payload)
                else:
                    print(dynameDBResp)

            else:
                print(data["model"])

        except KeyError:
            pass

        except ValueError:
            pass


if __name__ == "__main__":
    rtl_433_listen()