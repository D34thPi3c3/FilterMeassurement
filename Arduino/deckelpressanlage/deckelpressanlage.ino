#include "HX711_ADC.h"

const int numReadings = 5;

int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average

HX711_ADC LoadCell(2, 3);
long t;

void setup() {
Serial.begin(57600);
Serial.println("START INITIALIZE SENSOR");
//load cell initiation
LoadCell.begin();
long stabilisingtime = 9000;      // tare preciscion can be improved by adding a few seconds of stabilising time
LoadCell.start(stabilisingtime);
LoadCell.setCalFactor(11470);     // user set calibration factor (float)
Serial.println("Startup + tare is complete");

//Height sensor
//pinMode(8, INPUT);

//Command pressmess
//pinMode(9, INPUT);

//Step output
//pinMode(11, OUTPUT);
//digitalWrite(11, LOW);

//Step output
//pinMode(13, OUTPUT);
//digitalWrite(13, HIGH);
//delay(1);
//digitalWrite(13, LOW);

//Command move
pinMode(2, INPUT);

//Step output
pinMode(3, OUTPUT);
digitalWrite(3, LOW);

//Stop pressure
pinMode(4, OUTPUT);
digitalWrite(4, HIGH);

  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}


int averagForce() {
  while (readIndex <= numReadings){
  total = total - readings[readIndex];
  // read from the sensor:
  LoadCell.update();
  readings[readIndex] = LoadCell.getData();
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;
  delay(12);
  }
  readIndex=0;

  // calculate the average:
  average = total / numReadings;
  // send it to the computer as ASCII digits
  Serial.println(average);
  return average;
}


void loop() {
  int LCstatus = LoadCell.update();
  if(LCstatus == 1){
    float data = LoadCell.getData();
    Serial.print("Folgende Daten gibt der Kraftsensor aus");
    Serial.print(data);
    Serial.print("kg");
    Serial.print(" / in Newton:");
    Serial.print(data*9.81);
    Serial.println("N");
    if(data < -30.00){
      digitalWrite(4, HIGH);
    }
    else{
      digitalWrite(4, LOW);
    }
  }
  else{
    Serial.println("Es existiert irgend ein Fehler!!!!");
  }
  delay(100);
}
