int timer = 0;
float sensorValue = 0;

void setup() {
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  sensorValue = 1024 - analogRead(A0);
  // Serial.print("                                      Emitter Signal Intensity: ");
  Serial.print(millis());
  Serial.print("; ");
  Serial.println(sensorValue);
  //delay(500);
  //Serial.println(millis());
}
