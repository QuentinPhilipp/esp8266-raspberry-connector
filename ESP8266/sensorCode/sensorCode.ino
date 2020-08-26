#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>   // Include the WebServer library
#include "config.h"


char* device_name = "ROOM_1";
char *availableMetrics[] = {"temperature", "humidity"};


const char* ssid     = WIFI_SSID;         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = WIFI_PASSWORD;     // The password of the Wi-Fi network

ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

// Default server routes
void handleRoot();      // "/"
void handleNotFound();  //  404

// Custom server routes
void handshake();
void temperatureCallback();
void humidityCallback();

// Metrics measurements
double getTemperature();
double getHumidity();


void setup() {
  Serial.begin(9600);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');

  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid);
  Serial.println(" ...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nConnected to ");
  Serial.println(WiFi.SSID());              // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // Send the IP address of the ESP8266 to the computer

  if (MDNS.begin("esp8266")) { Serial.println("mDNS responder started"); }
  else { Serial.println("Error setting up MDNS responder!"); }


  // Setup routes
  server.on("/", handleRoot);               // Root request
  server.onNotFound(handleNotFound);        // 404 Error

  // Custom routes
  server.on("/check", handshake);
  server.on("/temperature", temperatureCallback);
  server.on("/humidity", humidityCallback);

  // Start the server
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();                    // Listen for HTTP requests from clients
}

void handleRoot() {
  server.send(200, "text/plain", "Hello world!");   // Send HTTP status 200 (Ok) and send some text to the browser/client
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}

void handshake(){
  String data = "{\"status\":\"OK\",\"device_name\":\"";
  data = data +device_name;
  data = data + "\"}";
  server.send(200, "json/application", data);
}

void temperatureCallback(){
  String data = "{\"status\":\"OK\",\"device_name\":\"";
  data = data +device_name;
  data = data + "\",\"metric_name\":\"temperature\",\"value\":\"";

  // Get the temperature
  double value = getTemperature();
  data.concat(value);

  data = data +  "\"}";
  server.send(200, "json/application", data);
}

void humidityCallback(){
  String data = "{\"status\":\"OK\",\"device_name\":\"";
  data = data +device_name;
  data = data + "\",\"metric_name\":\"humidity\",\"value\":\"";

  // Get the temperature
  double value = getTemperature();
  data.concat(value);

  data = data +  "\"}";
  server.send(200, "json/application", data);
}

double getTemperature(){
  return 28;
}

double getHumidity(){
  return 10;
}
