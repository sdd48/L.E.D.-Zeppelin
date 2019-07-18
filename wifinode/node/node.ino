#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 15

#define SSID "LAN Solo"
#define PASS "aaronisawesome"
#define PORT 5120
#define MDNS_NAME "LEDZeppelin"

#define MAX_LEDS 600
#define BUF_SIZE (MAX_LEDS*3)

// Watchdog timeout
#define WDT_MS 2000

struct UpdatePacket {
  uint32_t numLeds;
  uint8_t rgb[MAX_LEDS][3];
};

UpdatePacket *incoming = nullptr; //heap alloc
Adafruit_NeoPixel *strip = nullptr;
WiFiUDP Udp;


void setup() {
  // Heap alloc our buffer first
  incoming = new UpdatePacket();
  // put your setup code here, to run once:
  ESP.wdtEnable(WDT_MS);
  Serial.begin(115200);

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
  
  if (recvPacket(*incoming)) {
    // receive incoming UDP packets
    // If the packet size is incorrect, we need to create a new strip object
    if (!strip || strip->numPixels() != incoming->numLeds) {
      delete strip;
      strip = new Adafruit_NeoPixel(incoming->numLeds, LED_PIN, NEO_GRB + NEO_KHZ800);
      strip->begin();
//    }
//    Serial.println(ESP.getFreeHeap());
//    Serial.println(ESP.getMaxFreeBlockSize());
//    Serial.println(ESP.getHeapFragmentation());

    for (int i=0; i < MAX_LEDS; i++) {
      strip->setPixelColor(i, incoming->rgb[i][0], incoming->rgb[i][1], incoming->rgb[i][2]);
    }
    strip->show();
  }

}

bool recvPacket(UpdatePacket &packet) {
  int packetSize = 0;
  int len = 0;
  do {
    packetSize = Udp.parsePacket();
    if (packetSize > BUF_SIZE) { // Not enough room
      Serial.println("Too large of packet recieved");
    } else if (packetSize) {
      len = Udp.read(packet.rgb[0], BUF_SIZE);
      //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      //int len = Udp.read(incoming, BUF_SIZE);
      //Serial.printf("UDP packet contents: %s\n", incoming);
      packet.numLeds = len / 3;
    }
  } while (packetSize);

  return len;
}
