"""
Routes for the flask application.
"""
from datetime import datetime

from SensorInterfacing import app
from flask import Flask, jsonify, request,Blueprint
import atexit
import sched
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from firebase import firebase
firebase = firebase.FirebaseApplication('https://sensorinterfacing.firebaseio.com/', None)

import SensorInterfacing.sensors as sensors


# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

os.environ['TZ']= 'Europe/Paris'
# app = Flask(__name__)

manager = sensors.Manager()

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(manager.checkSensorTTL,'interval',seconds=1)
# sched.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: sched.shutdown())


@main_bp.route("/")
def home():
  # result = firebase.get('/sensors', None)
  # return str(result)
  location = "TestName"
  date = "240820-1220"
  data = {date: {"humidity":40,"temperature":22}}
  # data =  {"humidity":40,"temperature":22}

  firebase.put("/sensors",data=data,name=location)
  # firebase.put("/sensors/Bedroom",data=data,name=date)

  return "ok"


@main_bp.route('/sensor',methods=["POST"])
def sensor():
    data = request.get_json()
    if data["connection"]=="start":
        # Start a connection with a new sensor
        manager.addSensor(data)
    elif data["connection"]=="continue":
        manager.updateTTL(data)
    return "OK"


@main_bp.route('/values',methods=["POST"])
def postValue():
    # Get the value from the sensor and store it in a database
    data = request.get_json()

    # # Check if the sensor is already in the list of connected device
    # if not manager.isInSensorList(data["id"]):
    #     return 'Error, sensor not in the list of connected device'
    # else :
    #     print("data :",data)
    #     return "OK"

    result = firebase.get('/sensors', None)

    try:
        if result[data["name"]]:
            print("Add records")
            addValueDB(data)
    except KeyError as e:
        print("create entry and add the first record")
        createEntryDB(data)
    return "OK"



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
