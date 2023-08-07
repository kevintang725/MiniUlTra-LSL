int x;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);  
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(1);
  while (!Serial.available());
  x = Serial.readString().toInt();
  Serial.print(x + 1);
  
}
