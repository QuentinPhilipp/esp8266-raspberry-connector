from dotenv import load_dotenv
import os
from firebase import firebase
from networkAnalyzer import *
import requests
import json
import time

load_dotenv()
FIREBASE_URL = os.environ.get("FIREBASE_URL", None)
firebase = firebase.FirebaseApplication(FIREBASE_URL, None)


devicesIP = ["192.168.1.18"]


# Get device connected to network using ARP table
# devices = getArp()
# print(devices)
#
# for device in devices:
#     # Request /check to see if it's a sensor
#     try:
#         r = requests.get("http://"+device["LAN_IP"]+"/check",timeout=1)
#         if r.status_code==200:
#             print("Found device",r.json()["device_name"],"on IP : ",device["LAN_IP"])
#     except Exception as e:
#         print("Nothing on IP :",device["LAN_IP"])

class Sensor(object):
    """docstring for Sensor."""

    def __init__(self, name):
        super(Sensor, self).__init__()
        self.name = name
        self._value = 0

    def setValue(self,value):
        if value>0:
            self._value = value

    def getValue(self):
        return self._value

class Device(object):
    """docstring for Device."""

    def __init__(self, ip, name):
        super(Device, self).__init__()
        self.ip = ip
        self.name = name
        self.sensors = []

    def addSensor(self, sensor):
        self.sensors.append(sensor)


deviceList = []

while True:

    # Check if all the devices are connected
    for deviceIP in devicesIP:
        try:
            r = requests.get("http://"+deviceIP+"/check",timeout=1)
            if r.status_code==200:
                data = r.json()
                stored = any(device.name == data["device_name"] for device in deviceList)

                if not stored:
                    dev = Device(deviceIP,data["device_name"])
                    for sensorName in data["sensors"]:
                        newSensor = Sensor(sensorName)
                        dev.addSensor(newSensor)
                    deviceList.append(dev)
                else :
                    print("Sensors already in the list")
        except Exception as e:
            print("Error while loading devices")

    print("Device list :",deviceList)


    # For each device, request the data for all sensors
    for device in deviceList:
        print("## Requesting for device",device.name,"##")
        for sensor in device.sensors:
            print(" ~ Request sensor",sensor.name)
            try:
                r = requests.get("http://"+device.ip+"/"+sensor.name)
                if r.status_code==200:
                    data = r.json()
                    if data["device_name"]==device.name and data["metric_name"]==sensor.name:
                        sensor.setValue(float(r.json()["value"]))
                    else :
                        print("Error! Data not corresponding to request")
                    print(" ~ Request sensor",sensor.name,"done")
                else:
                    print("Error! Status code != 200")
            except Exception as e:
                raise

    # Store the data

    # Sleep until next measures
    time.sleep(15)




def addValueDB(data):
    now = datetime.now() # current date and time.
    date_time = now.strftime("%m-%d-%Y_%H:%M:%S")
    location = "sensors/"+data["name"]
    newData = {}

    for sensor in data["values"]:
        newData[sensor["metric"]]=sensor["value"]
    firebase.put(location,data=newData,name=date_time)


def createEntryDB(data):
    now = datetime.now() # current date and time.
    date_time = now.strftime("%m-%d-%Y_%H:%M:%S")
    name = data["name"]
    newData = {}
    for sensor in data["values"]:
        newData[sensor["metric"]]=sensor["value"]

    toSend = {date_time: {"humidity":40,"temperature":22}}
    firebase.put("/sensors",data=toSend,name=name)
