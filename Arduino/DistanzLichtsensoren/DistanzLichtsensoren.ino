uint32_t val = 0;
uint8_t counter = 0;
boolean mittelwert = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //  analogReadResolution(12);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = analogRead(A2);
  //Serial.print(val);
  counter++;
  if(mittelwert == true){
    for(int i = 0; i < 128; i++){
      val = val + analogRead(A2);
      counter++;
      delay(5);
    }
  }
  val = val/counter;
  //Serial.println("hello");
  Serial.println(val);
  val = 0;
  counter = 0;
  delay(1000);
}
