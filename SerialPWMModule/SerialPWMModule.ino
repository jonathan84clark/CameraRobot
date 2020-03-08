/***************************************************
* SERIAL PWM MODULE
* DESC: PWM module to output PWM signals to an attached
* device.
* Author: Jonathan L Clark
* Date: 3/7/2020
***************************************************/
int incomingByte = 0; // for incoming serial data
unsigned long msTicks = 0;
unsigned long timeout_time = 0;
int commandIndex = 0;
int commandSet[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

#define PWM_1 3
#define PWM_2 5
#define PWM_3 6
#define PWM_4 9
#define PWM_5 10
#define PWM_6 11

void setup() {
   Serial.begin(9600);
   pinMode(PWM_1, OUTPUT);
   pinMode(PWM_2, OUTPUT);
   pinMode(PWM_3, OUTPUT);
   pinMode(PWM_4, OUTPUT);
   pinMode(PWM_5, OUTPUT);
   pinMode(PWM_6, OUTPUT);
   digitalWrite(PWM_1, LOW);
}

void loop() {
   msTicks = millis();
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    commandSet[commandIndex] = incomingByte;
    // At this point we recieved 16 bytes, now we process the message
    if (commandSet[commandIndex] == 10 && commandSet[0] == 0x54)
    {
        if (commandSet[1] == 2)
        {
           analogWrite(PWM_1, commandSet[2]);
        }
        if (commandSet[3] == 2)
        {
           analogWrite(PWM_2, commandSet[4]);
        }
        if (commandSet[5] == 2)
        {
           analogWrite(PWM_3, commandSet[6]);
        }
        if (commandSet[7] == 2)
        {
           analogWrite(PWM_4, commandSet[8]);
        }
        if (commandSet[9] == 2)
        {
           analogWrite(PWM_5, commandSet[10]);
        }
        if (commandSet[11] == 2)
        {
           analogWrite(PWM_6, commandSet[12]);
        }
        commandIndex = 0;
    }
    timeout_time = msTicks + 1000;
    commandIndex++;
  }
  if (timeout_time < msTicks)
  {
     analogWrite(PWM_1, 0);
     analogWrite(PWM_2, 0);
     analogWrite(PWM_3, 0);
     analogWrite(PWM_4, 0);
     analogWrite(PWM_5, 0);
     analogWrite(PWM_6, 0);
  }
}
