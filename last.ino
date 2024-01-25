#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Declaration for BME280 sensor
Adafruit_BME280 bme;

const long utcOffsetInSeconds = 3600;

char daysOfTheWeek[7][12] = {"Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"};

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

float Temperature_moyenne = 0.0;
float Humidite_moyenne = 0.0;
float Pression_moyenne = 0.0;
int Compteur = 0;

void calculateAndDisplayAverages();
void createJSONFile();

void setup() {
  Serial.begin(9600);
  Wire.pins(0, 2);
  Wire.begin();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.display();

  WiFi.begin("iPhone de Axel", "rivenisbae");

  display.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    display.print(".");
    display.display();
  }
  display.println();

  timeClient.begin();

  display.print("Connected, IP address: ");
  display.println(WiFi.localIP());
  display.display();

  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1)
      ;
  }

  delay(5000);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.display();
}

void loop() {
  float temperature = bme.readTemperature();
  float humidite = bme.readHumidity();
  float Pression = bme.readPressure() / 100.0F;
  timeClient.update();


  display.clearDisplay();
  display.setCursor(0, 0);
  display.print(daysOfTheWeek[timeClient.getDay()]);
  display.print(", ");
  display.print(timeClient.getHours());
  display.print(":");
  display.print(timeClient.getMinutes());
  display.print(":");
  display.println(timeClient.getSeconds());


  display.setCursor(0, 10);
  display.print("Temperature: ");
  display.print(temperature);
  display.print(" C");

  display.setCursor(0, 30);
  display.print("Humidity: ");
  display.print(humidite);
  display.print(" %");

  display.setCursor(0, 50);
  display.print("Pressure: ");
  display.print(Pression);
  display.print(" hPa");

  display.display();

  delay(1000);

  Compteur++;
  Temperature_moyenne += temperature;
  Humidite_moyenne += humidite;
  Pression_moyenne += Pression;

  if (Compteur == 20) {
    calculateAndDisplayAverages();
  }
}

void calculateAndDisplayAverages() {
  Temperature_moyenne /= Compteur;
  Humidite_moyenne /= Compteur;
  Pression_moyenne /= Compteur;

  display.clearDisplay();
  display.setCursor(0, 10);
  display.print("Avg Temp: ");
  display.print(Temperature_moyenne);
  display.print(" C");

  display.setCursor(0, 30);
  display.print("Avg Humidity: ");
  display.print(Humidite_moyenne);
  display.print(" %");

  display.setCursor(0, 50);
  display.print("Avg Pressure: ");
  display.print(Pression_moyenne);
  display.print(" hPa");

  display.display();

  delay(5000);

  createJSONFile();

  Temperature_moyenne = 0.0;
  Humidite_moyenne = 0.0;
  Pression_moyenne = 0.0;
  Compteur = 0;
}

void createJSONFile() {
  JsonDocument doc;

  doc["Temperature"] = Temperature_moyenne;
  doc["Humidite"] = Humidite_moyenne;
  doc["Pression"] = Pression_moyenne;

  String jsonString;
  serializeJson(doc, jsonString);

  WiFiClient client;
  HTTPClient http;
  http.begin(client, "http://172.20.10.2:5000/writejson");
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("HTTP Request failed. Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();

}