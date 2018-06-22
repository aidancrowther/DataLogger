#include <VirtualWire.h>
#include <Wire.h>
#include <dht.h>
#include <Adafruit_BMP085_U.h>
#include <LowPower.h>
#include <avr/sleep.h>
   
//Initialize sensor datatypes
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
dht DHT;

//Specify pins and variables
#define DHT11_PIN 2
#define PowerPin 9

//Specify altitude above sea level to correct pressure readings
#define Altitude 90

volatile bool adcDone;

ISR(ADC_vect) { adcDone = true; }

void setup(){

  CLKPR = (1 << CLKPCE); // enable a change to CLKPR
  CLKPR = 0; // set the CLKDIV to 0 - was 0011b = div by 8 taking 16MHz to 2MHz

  //Setup pin to control power to transmitter and sensors
  pinMode(PowerPin, OUTPUT);
  digitalWrite(PowerPin, 0);

  //Serial.begin(9600);  // Debugging only
  //Serial.println("Initializing...");

  if(!bmp.begin()){
    //Serial.println("No Pressure sensor detected");
  }

  //Serial.println("Digital sensors initialized...");
  
  //Initialise the IO and ISR
  vw_set_tx_pin(10);
  vw_setup(1000);	 // Bits per sec

  //Serial.println("Transmitter initialized...");

  pinMode(13, OUTPUT);
  pinMode(A1, INPUT);

  //Serial.println("Analog sensors initialized...");

  //Serial.println("Starting\n");
}

void loop(){

  //Turn on sensors and transmitter
  digitalWrite(PowerPin, 0);
  
  //measure battery level and light level using the adc
  int batteryLevel = map(vccRead(), 115, 160, 0, 100);
  int lightLevel = map(analogRead(A1), 0, 350, 0, 100);

  //Get data from BMP sensor
  sensors_event_t event;
  bmp.getEvent(&event);

  //Get temperature data as a float from the BMP085 sensor
  float temperature;
  bmp.getTemperature(&temperature);

  //Get data from DHT sensor
  int chk = DHT.read11(DHT11_PIN);
  char msg[30];
  String message;

  //Once pressure data has arrived, prepare the message
  if(event.pressure){
     //correct the pressure for sealevel
     int pressure = (event.pressure/pow(1-(Altitude/44330.0),5.255));
     
    //Start the message using the node identifier 'N1'
    message = "N1: "
    + String((int) temperature, DEC) + "," 
    + String((int) DHT.humidity, DEC) + ","
    + String((int) event.pressure, DEC) + ","
    + String(lightLevel, DEC) + ","
    + String(batteryLevel, DEC);
  }
  else{
    //If the sensor receives an error, send a warning
    message = "Sensor Error";
    //Serial.println("Sensor Error");
  }

  //Specify message length for sending
  int msgLength = message.length()+1;

  //Serial.println(message);
  
  //Convert the message to a character array
  message.toCharArray(msg, msgLength);

  digitalWrite(13, true); // Flash a light to show transmitting
  vw_send((uint8_t *)msg, msgLength);
  vw_wait_tx(); // Wait until the whole message is gone
  digitalWrite(13, false);
  digitalWrite(PowerPin, 1); //Turn off the sensors to save power
  sleepForMinutes(10); //Sleep the system for 10 minutes between readings
}

//Go into low power mode and sleep for a specified number of minutes
void sleepForMinutes(int i){
  i = 7*i;
  for(int time=0; time<=i; time++){
    //Go to sleep for 8 seconds
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
  }
}

//Read Vcc voltage by comparing against internal 1.1V band gap
static byte vccRead(){
  set_sleep_mode(SLEEP_MODE_ADC);
  ADMUX = bit(REFS0) | 14;
  bitSet(ADCSRA, ADIE);
  for(byte i=0; i<4; ++i){
    adcDone = false;
    while(!adcDone){
      sleep_mode();
    }
  }
  bitClear(ADCSRA, ADIE);

  return(55U * 1023U) / (ADC + 1) - 50;
}

