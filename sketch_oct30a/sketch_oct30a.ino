void setup() {
  pinMode(12,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(9,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()>0){
    int kierunek = Serial.read()-'0';
    switch(kierunek){
      case 1:
        digitalWrite(12,HIGH);
        break;
      case 2:
        digitalWrite(11,HIGH);
        break;
      case 3:
        digitalWrite(10,HIGH);
        break;
      case 4:
        digitalWrite(9,HIGH);
        break;
      default:
        digitalWrite(12,LOW);
        digitalWrite(11,LOW);
        digitalWrite(10,LOW);
        digitalWrite(9,LOW);
        break;
      }   
    }
}
