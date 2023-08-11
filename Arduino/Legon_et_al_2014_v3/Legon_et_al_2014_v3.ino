// Central Microprocessor for Stimulation Paradigms and Trigger Controls
// Author: Kai Wing Kevin Tang, 2023

// Pin definitions
int triggerPin_FUS = 12;
int triggerPin_FES = 13;
int triggerPin_FUStoLSL = 11;
int triggerPin_FEStoLSL = 10;
int pwmPin = 9;             // The PWM output pin

// Serial I/O Communication
int incomingByte = 0; 
int start_flag = 0;

// Stimulation Paradigm
const unsigned long stimulation_period = 500; 
const unsigned long rest_period = 500; 
const unsigned long interval = stimulation_period + rest_period;
const unsigned long FES_delay = 100;
const unsigned long pulseDurationMicros = stimulation_period*1000;
const unsigned long single_pulse_ON_micros = 360;
const unsigned long single_pulse_OFF_micros = 640;


// Global Variables
unsigned long StartOfInterval;
unsigned long elapsed_rest;
unsigned long currentMicros;
unsigned long previousMicros = 0;
unsigned long pulseMicros = 0;


unsigned long elapsed_epoch = 0;
int pwmValue = 0;                 // PWM duty cycle value (0 to 255)
int counter = 0;


void setup()
{
  Serial.begin(115200);  
  digitalWrite(triggerPin_FUS, LOW);
  pinMode(triggerPin_FUS, OUTPUT);
  digitalWrite(triggerPin_FES, LOW);
  pinMode(triggerPin_FES, OUTPUT);
  digitalWrite(triggerPin_FUStoLSL, LOW);
  pinMode(triggerPin_FUStoLSL, OUTPUT);

  Serial.println("Press 1 to begin paradigm, Press CTRL+C to stop paradigm");
}

void loop()
{

  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte == '1'){
      start_flag = 1;
      Serial.println("Stimulation beginning in 10 seconds...");
      delay(10000);
      Serial.println("3");
      delay(1000);
      Serial.println("2");
      delay(1000);
      Serial.println("1");
      delay(1000);
      Serial.println("------------------------ : Start ");
    }
  }

  while (start_flag == 1){
      currentMicros = micros();

      // PWM
      if (currentMicros - previousMicros >= interval*1000){
        // Save the current time
        previousMicros = currentMicros;

        // Check if its time for FES pulse
        if (currentMicros - pulseMicros >= FES_delay*1000){
          digitalWrite(triggerPin_FES, HIGH);  
          digitalWrite(triggerPin_FEStoLSL, HIGH); 
          Serial.print("01");
          Serial.print('\n');
        }

        //Serial.print(float(pulseMicros));
        //Serial.print("\n");
        delayMicroseconds(interval*1000);
        // Reset internal pulse timer
        pulseMicros = currentMicros;
        //counter = 0;
      }

      // Check if its time for internal pulse
      if (currentMicros - pulseMicros < pulseDurationMicros){
        // Pulse Triggers ON for FUS
        digitalWrite(triggerPin_FUS, HIGH); 
        digitalWrite(triggerPin_FUStoLSL, LOW); 
        Serial.print("10");
        Serial.print('\n');

        delayMicroseconds(single_pulse_OFF_micros);

        // Pulse Trigger OFF for FUS
        digitalWrite(triggerPin_FUS, LOW);  
        digitalWrite(triggerPin_FES, LOW);  
        digitalWrite(triggerPin_FEStoLSL, LOW);
        Serial.print("00");
        Serial.print('\n');
      }
      else{
        digitalWrite(triggerPin_FUStoLSL, HIGH);
      }

      if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        if(incomingByte == '0'){
          start_flag = 0;
          Serial.println("------------------------ : End Experiment ");
          break;
        }
      }
    }
}
