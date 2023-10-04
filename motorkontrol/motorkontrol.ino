int x=0;

void setup() {
  pinMode(9, OUTPUT);
  pinMode(5, INPUT);
  Serial.begin(9600);
}

void loop()
{ 

if(Serial.read() == '1') {
  analogWrite(9, 60);
} 
if(Serial.read() == '0') {
  analogWrite(9, 0);
  x=1;
}
if (x==1){
 if (digitalRead(5) == HIGH) {
    analogWrite(9, 0); 
  }
  if (digitalRead(5) == LOW) {
    analogWrite(9, 60);   
  } 
}
}
