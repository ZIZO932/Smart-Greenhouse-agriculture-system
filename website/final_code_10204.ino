#include <Wire.h>
#include <BH1750.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid     = "04_el_top";
const char* password = "Medo12345##";

const char* mqtt_server = "192.168.0.169";
const int   mqtt_port   = 1883;

#define ONE_WIRE_BUS  4
#define MOISTURE_PIN  34

#define RELAY_WATER       15
#define RELAY_NITROGEN    32
#define RELAY_PHOSPHORUS  33
#define RELAY_POTASSIUM   25
#define RELAY_PELTIER     26
#define RELAY_PELTIER_FAN 27
#define RELAY_LIGHT       14
#define RELAY_AIR_FAN     12

const int RELAY_PINS[8] = {
  RELAY_WATER, RELAY_NITROGEN, RELAY_PHOSPHORUS, RELAY_POTASSIUM,
  RELAY_PELTIER, RELAY_PELTIER_FAN, RELAY_LIGHT, RELAY_AIR_FAN
};

bool relayStates[8] = {false};

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);
BH1750 lightMeter;

WiFiClient espClient;
PubSubClient mqttClient(espClient);

int dryValue = 3200;
int wetValue = 1500;

float currentTemp = 0.0;
float currentLight = 0.0;
int currentMoisture = 0;
float fakeN = 50.0, fakeP = 40.0, fakeK = 40.0;

float pidTempOutput = 0.0;
float pidMoistOutput = 0.0;
bool autoMode = true;

float lightOnThresh = 50.0;
float lightOffThresh = 400.0;

struct PlantProfile {
  const char* name;
  float tempSetpoint;
  float moistSetpoint;
  float lightOn;
  float lightOff;
  float npkN_peak;
  float npkP_peak;
  float npkK_peak;
};

const PlantProfile PLANT_BASIL  = { "basil", 25.0, 50.0, 30.0, 500.0, 50.0, 40.0, 40.0 };
const PlantProfile PLANT_STEVIA = { "stevia", 25.0, 55.0, 30.0, 500.0, 30.0, 40.0, 40.0 };

PlantProfile activePlant = PLANT_BASIL;
String activePlantName = "basil";

void applyPlantProfile(const PlantProfile& p) {
  activePlant = p;
  activePlantName = String(p.name);
  lightOnThresh = p.lightOn;
  lightOffThresh = p.lightOff;
  Serial.printf("[PLANT] Switched to %s  T:%.0f  M:%.0f  L:[%.0f-%.0f]\n",
                p.name, p.tempSetpoint, p.moistSetpoint, p.lightOn, p.lightOff);
}

#define SENSOR_INTERVAL 5000UL
#define MQTT_INTERVAL 5000UL
#define CONTROL_INTERVAL 60000UL
#define AIR_FAN_CYCLE 18000000UL
#define AIR_FAN_ON_TIME 900000UL
#define NPK_DOSE_CYCLE 86400000UL
#define NPK_N_SECONDS 10
#define NPK_P_SECONDS 8
#define NPK_K_SECONDS 8

const float NPK_N_PEAK = 50.0, NPK_N_MIN = 5.0;
const float NPK_P_PEAK = 40.0, NPK_P_MIN = 5.0;
const float NPK_K_PEAK = 40.0, NPK_K_MIN = 5.0;

unsigned long tSensor = 0;
unsigned long tPublish = 0;
unsigned long tControl = 0;
unsigned long tAirCycle = 0;
unsigned long tLastNpkDose = 0;

unsigned long waterPumpStart = 0;
unsigned long waterPumpLen = 0;
bool waterPumping = false;

unsigned long npkPhaseStart = 0;
int npkPhase = 0;
bool npkDosing = false;

#define RELAY_ON_STATE HIGH
#define RELAY_OFF_STATE LOW

void relayOn(int pin) {
  digitalWrite(pin, RELAY_ON_STATE);
  for (int i = 0; i < 8; i++) if (RELAY_PINS[i] == pin) { relayStates[i] = true; break; }
}

void relayOff(int pin) {
  digitalWrite(pin, RELAY_OFF_STATE);
  for (int i = 0; i < 8; i++) if (RELAY_PINS[i] == pin) { relayStates[i] = false; break; }
}

void allRelaysOff() {
  for (int i = 0; i < 8; i++) {
    digitalWrite(RELAY_PINS[i], RELAY_OFF_STATE);
    relayStates[i] = false;
  }
}

void peltierOn() {
  relayOn(RELAY_PELTIER);
  relayOn(RELAY_PELTIER_FAN);
}

void peltierOff() {
  relayOff(RELAY_PELTIER);
  relayOff(RELAY_PELTIER_FAN);
}

float readTemperature() {
  tempSensor.requestTemperatures();
  return tempSensor.getTempCByIndex(0);
}

float readLight() {
  return lightMeter.readLightLevel();
}

int readMoisture() {
  int raw = analogRead(MOISTURE_PIN);
  int percent = map(raw, dryValue, wetValue, 0, 100);
  return constrain(percent, 0, 100);
}

void updateFakeNPK() {
  fakeN = 150.0 + random(-10, 11) / 10.0;
  fakeP = 25.0 + random(-10, 11) / 10.0;
  fakeK = 190.0 + random(-10, 11) / 10.0;
}