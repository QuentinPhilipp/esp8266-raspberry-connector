from flask import Flask, jsonify, request
import atexit
import sched
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler


import sensors




os.environ['TZ']= 'Europe/Paris'
app = Flask(__name__)

manager = sensors.Manager()

sched = BackgroundScheduler(daemon=True)
sched.add_job(manager.checkSensorTTL,'interval',seconds=1)
sched.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: sched.shutdown())

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/sensor',methods=["POST"])
def sensor():
    data = request.get_json()

    print(data)

    if data["connection"]=="start":
        # Start a connection with a new sensor
        print("New connection")
        manager.addSensor(data)
    elif data["connection"]=="continue":
        print("Continue connection")
    return "OK"


@app.route('/sensorList',methods=["GET"])
def sensorList():

    data = ""
    for sensor in manager.sensorList:
        data+="Sensor :"+sensor.id+" - "+sensor.id+"\n"
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5555,use_reloader=False)
