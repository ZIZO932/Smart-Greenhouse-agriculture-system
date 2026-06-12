#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "04_el_top";
const char* password = "Medo12345##";

const char* mqtt_server = "192.168.0.169";

WiFiClient espClient;
PubSubClient client(espClient);

#define LED_PIN 2

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message: ");
  Serial.println(message);

  if (message == "ON") {
    digitalWrite(LED_PIN, HIGH);
  } 
  else if (message == "OFF") {
    digitalWrite(LED_PIN, LOW);
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    Serial.print("Connecting MQTT...");

    if (client.connect("ESP32_LED")) {
      Serial.println("Connected");

      client.subscribe("esp32/led");
    } else {
      Serial.print("Failed, rc=");
      Serial.println(client.state());
      delay(2000);
      return;
    }
  }

  client.loop();
}