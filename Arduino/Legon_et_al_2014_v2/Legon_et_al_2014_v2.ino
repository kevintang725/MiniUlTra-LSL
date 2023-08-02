// pin definitions
int triggerPin_FUS = 12;
int triggerPin_FES = 13;

// for incoming serial data
int incomingByte = 0; 
int start_flag = 0;


// stimulation paradigm
const unsigned long stimulation_period = 500; 
const unsigned long rest_period = 500; 
unsigned long StartOfInterval;
unsigned long  time;
unsigned long elapsed_rest;
unsigned long elapsed_epoch = 0;
const unsigned long epoch_rest = 1000;


void setup()
{
  Serial.begin(115200);  
  digitalWrite(triggerPin_FUS, LOW);
  pinMode(triggerPin_FUS, OUTPUT);
  digitalWrite(triggerPin_FES, LOW);
  pinMode(triggerPin_FES, OUTPUT);

  Serial.println("Press 1 to begin paradigm, Press 0 to stop paradigm");
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
      //Serial.println("Stimulation beginning in 3 seconds...");
      Serial.println("3");
      delay(1000);
      Serial.println("2");
      delay(1000);
      Serial.println("1");
      delay(1000);
      time = millis();
    }
  }

  /*
  // Check if 100ms has passed since start of FUS, if so begin FES (Median Nerve Stimulation)
    if ((millis() - time) > 100){
      digitalWrite(triggerPin_FES, HIGH);
    }
  */


  while (start_flag == 1){
      // Pulse Triggers for FUS
      digitalWrite(triggerPin_FUS, HIGH);  
      Serial.print('1');
      Serial.print('\n');

      delay(rest_period);

      digitalWrite(triggerPin_FUS, LOW);  
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
