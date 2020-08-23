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
            print(ttl)
            self.sensorsList.append(newSensor)
            print("Sensor added in the list")

    def checkSensorTTL(self):
        for sensor in self.sensorsList:
            print(time.time())
            if sensor.idle<time.time():
                self.sensorsList.remove(sensor)
                print("Remove one sensor")

        print("Sensor List :",self.sensorsList)



class Sensor(object):
    """docstring for Sensor."""

    def __init__(self,id,idle,name):
        super(Sensor, self).__init__()
        self.id = id
        self.idle= idle
        self.created=time.time()
        self.name = name
