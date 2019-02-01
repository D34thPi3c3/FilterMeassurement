// Store Analog Values
int val_pressure_sensor;
float val_pressure;
float val_vout;
float val_changed = 0;

// Constants
float val_pmin = -100;
float val_pmax = 100;
float val_vsup = 4.74;

// Initializing ports
int led_Yellow = 12;
int led_Red = 11;
int led_Green = 10;
int button = 4;
int button_pressed = 1;

void setup() {
  Serial.begin(9600);
  pinMode(led_Yellow, OUTPUT);
  pinMode(led_Red, OUTPUT);
  pinMode(led_Green, OUTPUT);
  pinMode(button, INPUT);
}

void loop() {
  button_pressed = digitalRead(button);
  if(button_pressed == LOW){
    val_changed = measurement();
    button_pressed = 1;
    led(val_changed);
  }
}

void led(float val_changed){
  if(val_changed >= 30){
    Serial.print("\nTest nicht bestanden bitte bestätigen!");
    Serial.print("\n----------------------------------------------------");
    while(button_pressed == 1){
      button_pressed = digitalRead(button);
      digitalWrite(led_Red, HIGH);
      delay(500);
      digitalWrite(led_Red, LOW);
      delay(500);
    }
  }else if(val_changed < 30){
    digitalWrite(led_Green, HIGH);
    delay(2000);
    digitalWrite(led_Green, LOW);
  }
}

float measurement() {
  float val_first = 0;
  float val_last = 0;
  digitalWrite(led_Yellow, HIGH);
  Serial.print("\nMessung wird durchgeführt.");
  for(int i=0; i < 10; i++){
    val_pressure_sensor = analogRead(A3);
    val_vout = val_vsup * val_pressure_sensor / 1024;
    val_pressure = ((val_vout - (0.1 * val_vsup))*(val_pmax - val_pmin) / 0.8 / val_vsup) + val_pmin;
    Serial.print("\nPressure: ");
    Serial.print(val_pressure);
    Serial.print(" mbar");
    if(i == 0){
      val_first = val_pressure;
    }
    else if(i == 9){
      val_last == val_pressure;
    }
    delay(1000);
  }
  val_changed = val_first - val_last;
  if(val_changed >= 30){
    Serial.print("\nAbweichung zu gross, Test nicht bestanden.");
  }
  else{
    Serial.print("\nAbweichung im Toleranzbereich, Test bestanden.");
  }
  Serial.print("\nAbweichung: ");
  Serial.print(val_changed);
  Serial.print(" mbar");
  Serial.print("\nMessung beendet.");
  Serial.print("\n----------------------------------------------------");
  digitalWrite(led_Yellow, LOW);
  return val_changed;
}
