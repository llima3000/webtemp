#!/usr/bin/env python3
#
from __future__ import print_function

import socket
import json

UDP_IP = "0.0.0.0"
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

                # write the info into one file
                filename = payload["transmitter"] + "-" + payload["time"].replace(":","-").replace(" ","-") + ".json"
                f = open("./tempread/" + filename, "w")
                f.write(json.dumps(payload))
                f.close()
                print(filename)

            else:
                print(data["model"])

        except KeyError:
            print("Key Error")

        except ValueError:
            print("Value Error")


if __name__ == "__main__":
    rtl_433_listen()