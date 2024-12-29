#include <WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>

const char* SSID = "Nemtenta";
const char* PASSWORD = "@Reborn10";
const char* mqtt_server = "192.168.159.158";
const int mqtt_port = 1883;
const char* mqtt_username = "tccunip";
const char* mqtt_password = "123";
const char* topic = "sensor/ultrasonic";

WiFiClient wifiClient;
PubSubClient MQTTclient(wifiClient);

const int trigPin = 5;
const int echoPin = 18;
#define SOUND_SPEED 0.034
long duration;
float distanceCm;

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Connect to Wi-Fi
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to MQTT
  MQTTclient.setServer(mqtt_server, mqtt_port);
  while (!MQTTclient.connected()) {
    Serial.println("Connecting to MQTT...");
    if (MQTTclient.connect("ESP32Client", mqtt_username, mqtt_password)) {
      Serial.println("Connected");
    } else {
      Serial.println("failed, rc=");
      Serial.println(MQTTclient.state());
      delay(2000);
    }
  }
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED / 2;

  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);

  // Publish the distance to the MQTT topic
  String msg = "{\"distance\": " + String(distanceCm) + "}";
  MQTTclient.publish(topic, msg.c_str());

  if (distanceCm < 20) {
    delay(10000); // Delay for 10 seconds
  } else {
    delay(1000); // Default delay between measurements
  }
}
