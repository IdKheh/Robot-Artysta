void setup() {
  pinMode(4,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  digitalWrite(3,HIGH); //PWM jednego silnika
  
  pinMode(8,OUTPUT); 
  pinMode(7,OUTPUT);
  pinMode(6,OUTPUT);
  digitalWrite(6,HIGH); //PWM drugiego silnika
  Serial.begin(9600);
}
int blokada = 0;
void loop() {
  if(Serial.available()>0){
    int kierunek = Serial.read()-'0';
    if(kierunek == 8) blokada = 1;
    if(kierunek == 9) blokada = 0;
    if(!blokada){
      switch(kierunek){
        case 1: //jazda do przodu
          digitalWrite(8,HIGH);
          digitalWrite(2,HIGH);
          digitalWrite(4,LOW);
          digitalWrite(7,LOW);       
          break;
          
        case 2: //jazda do lewo
          digitalWrite(8,HIGH);
          digitalWrite(4,HIGH);
          digitalWrite(2,LOW);
          digitalWrite(7,LOW);
          break;
          
        case 3: //jazda do prawo
          digitalWrite(7,HIGH);
          digitalWrite(2,HIGH);
          digitalWrite(4,LOW);
          digitalWrite(8,LOW);
          break;
          
        case 4: //jazda do tyłu
          digitalWrite(7,HIGH);
          digitalWrite(4,HIGH);
          digitalWrite(2,LOW);
          digitalWrite(8,LOW);
          break;
          
        default:
          digitalWrite(2,LOW);
          digitalWrite(4,LOW);
          digitalWrite(7,LOW);
          digitalWrite(8,LOW);
          break;
        }   
      }
    } 
}
