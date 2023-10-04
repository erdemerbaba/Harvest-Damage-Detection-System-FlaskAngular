void setup() {
  pinMode(9, OUTPUT);
  Serial.begin(9600);
}

void loop() //This will be executed over and over
{ 

if(Serial.read() == '1') {
  analogWrite(9, 200);
} 
if(Serial.read() == '0') {
  analogWrite(9, 0);
}
}
