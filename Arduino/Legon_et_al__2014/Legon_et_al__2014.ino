// pin definitions
int triggerPin = 12;

const byte LEDPin = 0;  // It's OK to use Pin 0 if you don't use Serial

const unsigned long stimulation_period = 500; 
const unsigned long rest_period = 500; 
unsigned long StartOfInterval;

void setup()
{
  Serial.begin(115200);  
  digitalWrite(triggerPin, LOW);
  pinMode(triggerPin, OUTPUT);

  Serial.println("Stimulation beginning in 3 seconds...");
  delay(3000);
}

void loop()
{
    digitalWrite(triggerPin, HIGH);  
    Serial.print('1');
    Serial.print('\n');

    delay(rest_period);

    digitalWrite(triggerPin, LOW);  
    Serial.print('0');
    Serial.print('\n');
}
