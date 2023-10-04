const int IN1 = 9;

void setup() {
  pinMode (IN1, OUTPUT);
}

void loop() {
  analogWrite(IN1,0); 
  //digitalWrite(IN1, HIGH);
}   
