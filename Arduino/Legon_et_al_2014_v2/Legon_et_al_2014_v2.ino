// pin definitions
int triggerPin_FUS = 12;
int triggerPin_FES = 13;

const byte LEDPin = 0;  // It's OK to use Pin 0 if you don't use Serial

const unsigned long stimulation_period = 500; 
const unsigned long rest_period = 500; 
unsigned long StartOfInterval;

void setup()
{
  Serial.begin(115200);  
  digitalWrite(triggerPin_FUS, LOW);
  pinMode(triggerPin_FUS, OUTPUT);
  digitalWrite(triggerPin_FES, LOW);
  pinMode(triggerPin_FES, OUTPUT);

  Serial.println("Stimulation beginning in...");
  Serial.println("3");
  delay(1000);
  Serial.println("2");
  delay(1000);
  Serial.println("1");
  delay(1000);
  time = millis();
}

void loop()
{
    // Check if 100ms has passed since start of FUS, if so begin FES (Median Nerve Stimulation)
    if ((millis() - time) > 100){
      digitalWrite(triggerPin_FES, HIGH);
      Serial.print("FES High");
    }

    // Pulse Triggers for FUS
    digitalWrite(triggerPin_FUS, HIGH);  
    Serial.print('1');
    Serial.print('\n');

    delay(rest_period);

    digitalWrite(triggerPin_FUS, LOW);  
    Serial.print('0');
    Serial.print('\n');
}
