# esp8266-raspberry-connector

This code allows to retrieve data from different ESP8266 to a Raspberry PI which manages the synchronization of the data and send it to a Firebase database.

## Connection
The boards and the RaspberryPI needs to be on the same local network.
You need to specify the IP address of each boards in the RaspberryPI config file.

## ESP8266
Each boards act as a web server where the RaspberryPI can request data. The routes are:

 - /check    This route is used to check if the server is still up and
   give the availables metrics.
 - /{{metricName}} Return the info corresponding to the requested data
