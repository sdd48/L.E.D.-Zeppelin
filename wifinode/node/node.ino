#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 15

#define SSID "LAN Solo"
#define PASS "aaronisawesome"
#define PORT 5120

#define NUM_LEDS 300
#define BUF_SIZE (NUM_LEDS*3)

// Watchdog timeout
#define WDT_MS 2000

uint8_t incoming[BUF_SIZE];

const char RESP_OKAY[] = "OKAY";
const char RESP_FAIL[] = "FAIL";

WiFiUDP Udp;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  ESP.wdtEnable(WDT_MS);
  Serial.begin(115200);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  WiFi.begin(SSID, PASS);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    ESP.wdtFeed();
    delay(500);
    Serial.print(".");

  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
  Udp.begin(PORT);
}

void loop() {
  ESP.wdtFeed();
  int packetSize = Udp.parsePacket();
  if (packetSize > 0) //got packet
  {
    // receive incoming UDP packets
    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incoming, BUF_SIZE);
    //Serial.printf("UDP packet contents: %s\n", incoming);
    delay(1);
    if (len == BUF_SIZE) {
      //Serial.println("got update");
      for (int i=0; i < NUM_LEDS; i++) {
        strip.setPixelColor(i, incoming[3*i], incoming[3*i+1], incoming[3*i+2]);
      }
      yield();
      strip.show();
    }
    
  }
  delay(1);

}


