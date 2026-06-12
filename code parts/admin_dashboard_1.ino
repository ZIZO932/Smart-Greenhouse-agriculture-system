#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ===== WIFI =====
const char* ssid = "04_el_top";
const char* password = "Medo12345##";

// ===== MQTT =====
const char* mqtt_server = "192.168.0.169";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// ===== SENSOR ARRAYS =====
int tempArr[] = {20,21,22,23,24,25};
int lightArr[] = {100,200,300,400,500};
int moistArr[] = {30,40,50,60};
int npkArr[] = {10,20,30,40,50};

unsigned long lastSend = 0;

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(300);
}

void connectMQTT() {
  while (!client.connected()) {
    client.connect("ESP32_SIM");
    delay(500);
  }
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) connectMQTT();
  client.loop();

  if (millis() - lastSend > 5000) {
    lastSend = millis();

    StaticJsonDocument<256> doc;

    doc["device_id"] = "SN_01";
    doc["temp"] = tempArr[random(6)];
    doc["light"] = lightArr[random(5)];
    doc["moisture"] = moistArr[random(4)];
    doc["npk_n"] = npkArr[random(5)];
    doc["npk_p"] = npkArr[random(5)];
    doc["npk_k"] = npkArr[random(5)];
    doc["rssi"] = WiFi.RSSI();

    char buffer[256];
    serializeJson(doc, buffer);

    Serial.println(buffer);
    client.publish("esp32/01/data", buffer);
  }
}