int i = 0, b = 0;
int sending_flag = 0; 
char source[] = "11110000111100001111000011110000111100001111";

void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  // initial signal ( 1s of open led)
  if (Serial.available() > 0){
    b = Serial.read();
    // 49 ASCII int for "1" char 
    if (b == 49){
      digitalWrite(8, HIGH);
      delay(2000);
      digitalWrite(8, LOW);
      delay(2000);

      sending_flag = 1;
    }
  }

  if (sending_flag == 1){
    for(i = 0; source[i] != '\0'; i++){
      Serial.println(source[i]);
      if (source[i] == '1') {
        digitalWrite(8, HIGH);
      }
      else {
        digitalWrite(8, LOW);
      }
      delay(200);
    }
    //b = 0;
    sending_flag=0;

    // chiusura dell'invio del messaggio
    // spegni led per un secondo
    // accendi led per 1 secondo
    // spegni definitvamente
    digitalWrite(8, LOW);
    delay(500);
    digitalWrite(8, HIGH);
    delay(2000);
    digitalWrite(8, LOW);
    //delay(1000);
    
  }
}
