const int pwmPin = 9;             // The PWM output pin
const unsigned long onTime = 500;   // Duration of ON time in milliseconds
const unsigned long offTime = 500;    // Duration of OFF time in milliseconds
const unsigned long interval = 1000;  // Interval between pulses in milliseconds
const unsigned long pulseDuration = 1; // Duration of the internal pulse

unsigned long previousMillis = 0; // Stores the last time PWM was updated
unsigned long pulseMillis = 0;    // Stores the last time of the internal pulse
int pwmValue = 0;                 // PWM duty cycle value (0 to 255)

void setup() {
  Serial.begin(115200);
  pinMode(pwmPin, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // Save the current time
    previousMillis = currentMillis;

    // Generate the PWM signal with variable ON and OFF times
    analogWrite(pwmPin, pwmValue);
    delay(onTime);
    analogWrite(pwmPin, 0);
    delay(offTime);

    // Reset the internal pulse timer
    pulseMillis = currentMillis;
  }

  // Check if it's time for the internal pulse
  if (currentMillis - pulseMillis < pulseDuration) {
    // Perform actions for the internal pulse here
    // For example, you can toggle an output pin or perform some other task
    // For demonstration, let's toggle an LED on and off
    digitalWrite(13, HIGH);
    Serial.println("1");
    delay(50);
    digitalWrite(13, LOW);
    Serial.println("0");
  }
}