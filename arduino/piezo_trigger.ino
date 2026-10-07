const byte piezoPin = A0;
int rawValue; // raw A/D readings
int piezoValue; // peak value
int finalValue; // smoothed final value

void setup() {
  analogReference(INTERNAL); // remove this line if too sensitive
  Serial.begin(9600);
}

void loop() {
  piezo();
  //other code
}

void piezo() {
  for (int x = 0; x < 100; x++) {
    rawValue = analogRead(piezoPin); // 100 A/D readings
    if (rawValue > piezoValue) {
      piezoValue = rawValue; // store peaks
    }
  }
  if (finalValue < piezoValue) { // fast attack
    finalValue = piezoValue;
  }
  else {
    finalValue = (finalValue + piezoValue) / 2; // smooth decay
  }
  piezoValue = 0; // reset
  if (finalValue >= 9) {
    Serial.println(finalValue); // print only if > 0
    Serial.println("Movement detected");
  }
}