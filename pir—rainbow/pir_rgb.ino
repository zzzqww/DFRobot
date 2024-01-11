// Include the Adafruit NeoPixel library to control the LED strip
#include <Adafruit_NeoPixel.h>

// Define sensorPin to read input signal (e.g., from a button or sensor)
byte sensorPin = 2;   
// Define PIN_LED as the pin that sends control signals to the LED strip's Data Input (DI)
#define PIN_LED 13     
// Define NUM_LED as the number of LEDs in the strip
#define NUM_LED 1     

// Create an instance of the Adafruit_NeoPixel class to control the LED strip
Adafruit_NeoPixel RGB_Strip = Adafruit_NeoPixel(NUM_LED, PIN_LED, NEO_GRB + NEO_KHZ800);

void setup() {
  // Set the sensorPin as an INPUT
  pinMode(sensorPin,INPUT);
  // Initialize the NeoPixel strip
  RGB_Strip.begin();
  // Initialize all pixels to 'off'
  RGB_Strip.show();
  // Set the initial brightness of the strip to 0 (range is from 0 (darkest) to 255 (brightest))
  RGB_Strip.setBrightness(0);
  // Begin serial communication at a baud rate of 9600
  Serial.begin(9600);
}

void loop() {
  // Read the state of the sensorPin (0 or 1)
  byte state = digitalRead(sensorPin);

  // If the sensorPin reads LOW (0), turn off the LEDs
  if (state == 0) {
    RGB_Strip.setBrightness(0);
    RGB_Strip.show();
    // Print "off" to the serial monitor
    Serial.println("off");
  }
  // If the sensorPin reads HIGH (1), turn on the LEDs with a rainbow effect
  else if (state == 1) {
    RGB_Strip.setBrightness(128); // Set brightness to half
    rainbow(2);  // Call the rainbow function to create a rainbow effect
    // Print "on" to the serial monitor
    Serial.println("on");
  }
}

// Function to fill the strip with a solid color, one pixel at a time
void colorWipe(uint32_t c, uint16_t wait) {
  for (uint16_t i = 0; i < RGB_Strip.numPixels(); i++) {
    RGB_Strip.setPixelColor(i, c); // Set pixel's color (c)
    RGB_Strip.show(); // Update the strip with new color
    delay(wait); // Wait for 'wait' milliseconds
  }
}

// Function to create a rainbow effect that cycles through all pixels
void rainbow(uint8_t wait) {
  uint16_t i, j;

  for (j = 0; j < 256; j++) {
    for (i = 0; i < RGB_Strip.numPixels(); i++) {
      RGB_Strip.setPixelColor(i, Wheel((i + j) & 255)); // Calculate color and set it for each pixel
    }
    RGB_Strip.show(); // Update the strip with new colors
    delay(wait); // Wait for 'wait' milliseconds
  }
}

// Function that creates a color wheel, transitioning smoothly between RGB colors
uint32_t Wheel(byte WheelPos) {
  // Transition from red to green to blue and back to red
  if (WheelPos < 85) {
    return RGB_Strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    return RGB_Strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
    WheelPos -= 170;
    return RGB_Strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}
