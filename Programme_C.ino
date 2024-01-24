#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <SD.h>
#include <ArduinoJson.h> 

#define SCREEN_WIDTH 128  
#define SCREEN_HEIGHT 64  

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Declaration pour BME280 sensor
Adafruit_BME280 bme;

float Temperature_moyenne = 0.0;
float Humidite_moyenne = 0.0;
float Pression_moyenne = 0.0;
int Compteur = 0;

void setup() {
  Serial.begin(115200);

  Wire.pins(0, 2);
  Wire.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  if (!bme.begin(0x76)) {  // BME280 address may vary, use 0x76 or 0x77
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


  display.clearDisplay();
  //pour définir le curseur (ici x = 0 et y = 10) pour que sur l'écran ca commence a afficher a partir de (0,10)
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


  delay(5000);

 
  Compteur++;
  Temperature_moyenne += temperature;
  Humidite_moyenne += humidite;
  Pression_moyenne += Pression;

  if (Compteur == 6) { 
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


  Temperature_moyenne = 0.0;
  Humidite_moyenne = 0.0;
  Pression_moyenne = 0.0;
  Compteur = 0;


  createJSONFile();
}

void createJSONFile() {
  // une class pour allouer mémoire basé sur la taille 1024
  DynamicJsonDocument doc(1024);

  // Add data to the JSON document
  doc["Temperature_moyenne"] = Temperature_moyenne;
  doc["Humidite_moyenne"] = Humidite_moyenne;
  doc["Pression_moyenne"] = Pression_moyenne;
  doc["Temperature"] = Temperature_moyenne;
  doc["Humidite"] = Humidite;
  doc["Pression"] = Pression;


  // Convertir le data de json en string (lisible)
  String jsonString;
  serializeJson(doc, jsonString);

  // Open a file on the SD card
  File file = SD.open("sensor_data.json", FILE_WRITE);


  if (file) {
    file.println(jsonString);
    file.close();
    Serial.println("Fichier JSON créé");
  } else {
    Serial.println("Erreur fichier JSON n'ouvre pas");
  }
}