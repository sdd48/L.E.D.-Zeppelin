#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 15

#define SSID "LAN Solo"
#define PASS "aaronisawesome"
#define PORT 5120
#define MDNS_NAME "LEDZeppelin"

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
  if (MDNS.begin(MDNS_NAME)) {
    Serial.println("MDNS responder started");
  }
  
  Udp.begin(PORT);
}

void loop() {
  ESP.wdtFeed();
  MDNS.update();
  // We keep reading until there is nothing left
  int packetSize = 0;
  int len = 0;
  do {
    packetSize = Udp.parsePacket();
    if (packetSize) {
      len = Udp.read(incoming, BUF_SIZE);
      Serial.println("Got packet");
    }
  } while (packetSize);
  

  if (len == BUF_SIZE) //got Update
  {
    // receive incoming UDP packets
    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    //int len = Udp.read(incoming, BUF_SIZE);
    //Serial.printf("UDP packet contents: %s\n", incoming);
    Serial.println(ESP.getFreeHeap());
    Serial.println(ESP.getMaxFreeBlockSize());
    Serial.println(ESP.getHeapFragmentation());
    delay(1);
    for (int i=0; i < NUM_LEDS; i++) {
      strip.setPixelColor(i, incoming[3*i], incoming[3*i+1], incoming[3*i+2]);
    }
    strip.show();
  }
  yield();

}
