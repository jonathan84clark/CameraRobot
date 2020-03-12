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
}

void loop() {
   msTicks = millis();
  // send data only when you receive data:
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    commandSet[commandIndex++] = incomingByte;
    if (commandIndex == 3)
    {
        commandIndex = 0;
        if (commandSet[0] == 0x01)
        {
           analogWrite(PWM_1, commandSet[1]);
        }
        if (commandSet[0] == 0x02)
        {
           analogWrite(PWM_2, commandSet[1]);
        }
        if (commandSet[0] == 0x04)
        {
           analogWrite(PWM_3, commandSet[1]);
        }
        if (commandSet[0] == 0x08)
        {
           analogWrite(PWM_4, commandSet[1]);
        }
        if (commandSet[0] == 0x10)
        {
           analogWrite(PWM_5, commandSet[1]);
        }
        if (commandSet[0] == 0x20)
        {
           analogWrite(PWM_6, commandSet[1]);
        }
        
    }
  }
}
