# LED Music Display

## Supplies: 

-[Microcontroler, ESP8266](https://www.amazon.com/HiLetgo-Internet-Development-Wireless-Micropython/dp/B010O1G1ES/ref=asc_df_B010O1G1ES/?tag=hyprod-20&linkCode=df0&hvadid=309818716690&hvpos=1o1&hvnetw=g&hvrand=11462262898223770340&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9005070&hvtargid=aud-643565131866:pla-361876718784&psc=1)

-[Lights, WS2812B](http://www.ebay.com/itm/WS2812B-5050-RGB-LED-Strip-5M-150-300-Leds-144-60LED-M-Individual-Addressable-5V-/231105154168)

-[Power Source, Outlet to 5V](https://www.trcelectronics.com/View/Mean-Well/RD-35A.shtml?gclid=CjwKCAjwg-DpBRBbEiwAEV1_-AjomefRKshlGr2H7Lwyo-U164iOeiUgQHAlKNaGN3aW73AOFTybRBoCDrUQAvD_BwE)

-[Wall to Bare wire adapter (Can just chop off from some other cord or device)](https://www.cablewholesale.com/specs/10w1-10106.php?utm_source=GoogleShopping&utm_medium=cpc&utm_term=10W1-10106&utm_campaign=NEMA%205-15P%20to%20Standard%20ROJ%20Power%20Cord%2C%20Black%2C%2018%2F3%20(18AWG%203%20Conductor)%20SVT%2C%2010%20Amp%20%2F%20125%20Volt%2C%206%20foot&gclid=CjwKCAjwg-DpBRBbEiwAEV1_-Ohx-VB09svkTxMwg9Qox4s7GdxlXGfOIlai-8XsFYfLurRTktlBJhoCmh4QAvD_BwE)



## Downloads
-[Arduino IDE](https://www.arduino.cc/en/main/software)

-[Adafruit Neopixel Drivers](https://github.com/adafruit/Adafruit_NeoPixel)

## Assembly
### Hardware
-Tie the positive wire from the outlet input to L on the power adapted, the neutral wire to N and the ground to the ground symbol

-Tie one of the red positive wire from the lights to the +V output on the adapter and the white negative wire to -V

-Solder the other red positive wire from the lights to VIN on the MCU, the white one to ground and the middle green data pin to RX (NOT TX)

### Software
-Select "Node MCU 1.0 (ESP-12 Module)" from tools->boards in the arduino IDE

-Open node.ino from the github project 

-CHANGE SSID TO YOUR LOCAL NETWORK NAME AND PASS TO THE PASSWORD AT THE TOP OF NODE.INO

-Flash the file onto the MCU

-Run input.py play music and and watch the lights!
