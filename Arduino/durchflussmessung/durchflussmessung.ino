#include <Servo.h>
#include <Wire.h>
Servo esc;
int counter;
int input = 900;
double val = 0;
double val2 = 0;
bool serialall = false;
bool messung = false;

void setup() {
  Serial.begin(57600);
  Serial.println("INITIALIZE");
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(3, INPUT);
  esc.attach(9);
  esc.writeMicroseconds(900);
  esc.writeMicroseconds(1001);
  esc.writeMicroseconds(900);
  delay(10000);
}

void loop()
{
  if(messung == true){
    digitalWrite(LED_BUILTIN, HIGH);
    for(int i = 0; i < 250; i++){
      input = 900 + i;
      esc.writeMicroseconds(input);
      delay(5);
      if(serialall == true){
        Serial.print("ESC_Microsecond: ");
        Serial.print(input);
        Serial.print(" / ");
      }
      val = analogRead(A3);
      double diffpressure = (((val-510)*2.49)/510);
      if(serialall == true){
        Serial.print("Druckdifferenz: ");
        Serial.print(diffpressure);
        Serial.println("mbar");  
      }
    }
    Serial.println("Höchste Umdrehung");
    delay(10000);
    val = analogRead(A3);
    delay(300);
    val2 = analogRead(A2);
    for(int i = 0; i < 64; i++){
      val = val + analogRead(A3);
      delay(2);
      val2 = val2 + analogRead(A2);
      counter++;
 
    }
    val = val/counter;
    val2 = val2/counter;
    double diffpressure = (((val-510)*2.49)/510);
    double druckmotor = (((val2-510)*25)/510);
    Serial.print("Druckdifferenz Durchfluss: ");
    Serial.print(diffpressure);
    Serial.println("mbar");
    double durchfluss = (diffpressure*7.999*60);
    Serial.print("Effektiver Durchfluss:");
    Serial.print(durchfluss);
    Serial.println("l/min");
    Serial.print("Druck vor motor");
    Serial.print(druckmotor);
    Serial.println("mbar");   
    digitalWrite(LED_BUILTIN, LOW);
    delay(2000);
    digitalWrite(LED_BUILTIN, HIGH);
    for(int i = 250; i>0; i--){
      input = 900 + i;
      esc.writeMicroseconds(input);
      delay(5);
      if(serialall == true){
        Serial.print("ESC_Microsecond: ");
        Serial.print(input);
        Serial.print(" / ");
      }
      val = analogRead(A3);
      double diffpressure = (((val-510)*2.49)/510);
      if(serialall == true){
        Serial.print("Druckdifferenz: ");
        Serial.print(diffpressure);
        Serial.println("mbar"); 
      }
    }
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("Tiefste Umdrehung");
    val = 0;
    counter = 0;
  }
  delay(10000);
}
