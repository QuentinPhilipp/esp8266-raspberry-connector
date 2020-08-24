import time


class Manager(object):
    """docstring for Manager."""

    def __init__(self,ip=0,port=5555):
        super(Manager, self).__init__()

        self.sensorsList = []
        self.ip = ip
        self.port = port



    def addSensor(self,data):

        existing = any(sensor.id == data['id'] for sensor in self.sensorsList)

        if existing:
            print("Sensor already in the list")
        else:
            ttl = time.time() + data["idle"]

            newSensor = Sensor(data['id'],ttl,data['name'])
            self.sensorsList.append(newSensor)
            print("Sensor added in the list")

    def updateTTL(self,data):
        for sensor in self.sensorsList:
            if sensor.id == data["id"]:
                sensor.idle=time.time()+data["idle"]
                print("Updated TTL of sensor ",sensor.id)
                break
        else :
            print("Sensor not in the list -> Adding the sensor in the list of connected sensor")
            self.addSensor(data)


    def checkSensorTTL(self):
        for sensor in self.sensorsList:
            if sensor.idle<time.time():
                self.sensorsList.remove(sensor)
                print("Remove sensor ",sensor.id)

    def isInSensorList(self,id):
        for sensor in self.sensorsList:
            if sensor.id == id:
                return True
        else:
            return False



class Sensor(object):
    """docstring for Sensor."""
    def __init__(self,id,idle=60,name="None"):
        super(Sensor, self).__init__()
        self.id = id
        self.idle= idle
        self.created=time.time()
        self.name = name
