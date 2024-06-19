#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <WiFiNINA.h>

const char* ssid = "Mojo";
const char* password = "brilliancy";

String serverName = "127.0.0.1"; // IP address of your Flask server
String serverPath = "/upload";        // Flask upload route

const int serverPort = 5000;

const int timerInterval = 20000;      // Time (milliseconds) between each HTTP POST image
unsigned long previousMillis = 0;     // Last time image was sent

WiFiClient client;

void setup() {
  Serial.begin(115200);

  // Connect to WiFi network
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    delay(10000); // Wait 10 seconds to connect
  }
  Serial.println("Connected to WiFi");

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Code to receive the processed image from ESP32-CAM and send it to the server
  // Code for receiving image from ESP32-CAM goes here (not implemented in this example)

  // Assuming the processed image is stored in a variable named processedImage
  String processedImage = "Processed image data"; // Placeholder, replace with actual image data

  // Check if it's time to send the image
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= timerInterval) {
    sendPhoto(processedImage);
    previousMillis = currentMillis;
  }
}

void sendPhoto(String imageData) {
  if (client.connect(serverName.c_str(), serverPort)) {
    Serial.println("Connected to server");

    // Prepare HTTP POST request
    String postRequest = "POST " + serverPath + " HTTP/1.1\r\n" +
                         "Host: " + serverName + "\r\n" +
                         "Content-Type: application/x-www-form-urlencoded\r\n" +
                         "Content-Length: " + String(imageData.length()) + "\r\n\r\n" +
                         imageData;

    // Send the POST request
    client.print(postRequest);

    // Wait for server response
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.print(c); // Print response from server (optional)
      }
    }

    // Close the connection
    client.stop();
    Serial.println("Image sent to server");
  } else {
    Serial.println("Unable to connect to server");
  }
}
