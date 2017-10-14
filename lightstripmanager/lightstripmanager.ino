#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#include <PacketSerial.h>
//https://github.com/bakercp/PacketSerial

#define PIN 6
#define MAX_LEDS 128
#define DECODE_BUF (3*MAX_LEDS)
#define RECV_BUF_SIZE 512

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);
PacketSerial_<SLIP, SLIP::END, RECV_BUF_SIZE> serial;

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code


  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  serial.setPacketHandler(&onPacket);
  serial.begin(115200);
}


void loop() {
  serial.update();
  
  strip.setPixelColor(11, 255, 0, 255);
}


void onPacket(const uint8_t* buffer, size_t size)
{
  // Make a temporary buffer.
  uint8_t tmp[size]; 
  
  // Copy the packet into our temporary buffer.
  memcpy(tmp, buffer, size); 
  
  // Reverse our temporaray buffer.
  reverse(tmp, size);
  
  // Send the reversed buffer back.
  // The send() method will encode the buffer
  // as a packet, set packet markers, etc.
  serial.send(tmp, size);
}
