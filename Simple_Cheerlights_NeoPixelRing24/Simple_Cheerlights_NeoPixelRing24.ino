// Cheerlights NeoPixel Ring
// Adafruit Feather HUZZAH32 (ESP32) + NeoPixel Ring 24
// This sketch connects to the ThingSpeak channel 1417 to fetch the current Cheerlights color
// You can learn more about Cheerlights here: https://cheerlights.com/learn/
// April 25, 2025 

#include <Adafruit_NeoPixel.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "XXXXXXXXXXXXX";
const char* password = "XXXXXXXXXXXX";

#define PIN        15          // GPIO15 on HUZZAH32
#define NUMPIXELS  24          // 24-pixel NeoPixel Ring

Adafruit_NeoPixel strip(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

String lastColor = "";

void setup() {
  Serial.begin(115200);
  strip.begin();
  strip.setBrightness(128); // Half brightness
  strip.show(); // Turn off all LEDs

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    rainbowCycle(5); // Show rainbow if WiFi is not connected
    return;
  }

  HTTPClient http;
  http.begin("http://api.thingspeak.com/channels/1417/field/1/last.txt");
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    String color = http.getString();
    color.trim();

    if (color != lastColor) {
      Serial.println("New color: " + color);
      uint32_t colorValue = getColorValue(color);

      theaterChase(colorValue, 100);
      setAllPixels(colorValue);
      lastColor = color;
    }
  } else {
    Serial.println("Failed to fetch color!");
  }

  http.end();
  delay(10000); // Check every 10 seconds
}

void setAllPixels(uint32_t color) {
  for (int i = 0; i < NUMPIXELS; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

void theaterChase(uint32_t color, int wait) {
  for (int cycle = 0; cycle < 9; cycle++) { // Run 9 theater chase cycles
    for (int q = 0; q < 3; q++) {
      for (int i = 0; i < NUMPIXELS; i++) {
        if (i % 3 == q) {
          strip.setPixelColor(i, color);
        } else {
          strip.setPixelColor(i, 0); // Off
        }
      }
      strip.show();
      delay(wait);
    }
  }
}

void rainbowCycle(int wait) {
  for (int j = 0; j < 256; j++) {
    for (int i = 0; i < NUMPIXELS; i++) {
      strip.setPixelColor(i, Wheel((i * 256 / NUMPIXELS + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

uint32_t getColorValue(String color) {
  color.toLowerCase();
  if (color == "red") return strip.Color(255, 0, 0);
  if (color == "green") return strip.Color(0, 255, 0);
  if (color == "blue") return strip.Color(0, 100, 255);
  if (color == "cyan") return strip.Color(0, 255, 255);
  if (color == "magenta") return strip.Color(255, 0, 255);
  if (color == "yellow") return strip.Color(255, 255, 0);
  if (color == "white") return strip.Color(255, 255, 255);
  if (color == "purple") return strip.Color(70, 0, 130);
  if (color == "orange") return strip.Color(255, 165, 0);
  if (color == "pink") return strip.Color(255, 192, 203);
  if (color == "warmwhite") return strip.Color(255, 223, 196);
  if (color == "oldlace") return strip.Color(253, 245, 230);
  if (color == "blueviolet") return strip.Color(138, 43, 226);
  return strip.Color(0, 0, 0); // Off if unknown
}