// Central Microprocessor for Stimulation Paradigms and Trigger Controls
// Author: Kai Wing Kevin Tang, 2023

// Pin definitions
int triggerPin_FUS = 12;
int triggerPin_FES = 13;
int triggerPin_FUStoLSL = 11;
int triggerPin_FEStoLSL = 10;

// Serial I/O Communication
int incomingByte = 0; 
int start_flag = 0;

// Stimulation Paradigm
const unsigned long stimulation_period = 500; 
const unsigned long rest_period = 500; 
const unsigned long FES_delay = 100;
const unsigned long epoch_rest = 10000;

// Global Variables
unsigned long StartOfInterval;
unsigned long elapsed_rest;
unsigned long elapsed_epoch = 0;


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
      // Pulse Triggers ON for FUS
      digitalWrite(triggerPin_FUS, HIGH);
      digitalWrite(triggerPin_FUStoLSL, HIGH); 
      Serial.print('1');
      Serial.print('\n');

      // Wait for 100ms before FES
      delay(FES_delay);

      // Pulse Triggers ON for FES 
      digitalWrite(triggerPin_FES,HIGH);
      digitalWrite(triggerPin_FEStoLSL, HIGH);

      // Wait for elapsed total OFF cycle
      delay(rest_period - FES_delay);

      // Pulse Trigger OFF for FUS+FES
      digitalWrite(triggerPin_FUS, LOW);  
      digitalWrite(triggerPin_FUStoLSL, LOW); 
      digitalWrite(triggerPin_FES, LOW);  
      digitalWrite(triggerPin_FEStoLSL, LOW); 
      Serial.print('0');
      Serial.print('\n');

      if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        if(incomingByte == '0'){
          start_flag = 0;
          Serial.println("Ending experiment");
          break;
        }
      }
    }
}
