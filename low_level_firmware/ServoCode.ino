#include <Servo.h>

Servo FrontLeft; //S1 Motor Front?
Servo FrontRight; //S2?
Servo RearLeft; //S1?
Servo RearRight; //S2?

int pos = 0;
int time = 0;

void setup(){
  FrontLeft.attach(9);
  FrontRight.attach(10);
  RearLeft.attach(11);
  RearRight.attach(12);
  Serial.begin(115200);
}

void loop() {
  int val[2];
  if (Serial.available() > 0){
    String incomingData = Serial.readStringUntil('\n');
    int commaIndex = incomingData.indexOf(',');
      if (commaIndex != -1){
        String part1 = incomingData.substring(0,commaIndex);
        String part2 = incomingData.substring(commaIndex+1);
        int val1 = part1.toInt();
        int val2 = part2.toInt();
        setmotors(val1,val2);
      }
  }
  /*
  setmotors(90,90);
  delay(2000);
  //motors(150,150);
  setmotors(95,85); //Forward, I believe Left motors above 90 is fwd, right above 90 is backwards
  delay(1000);
  setmotors(90,90);
  delay(1000);
  setmotors(110,90);
  delay(500);
  setmotors(90,90);
  delay(2000);
  */
}

void setmotors(int LeftSide, int RightSide){
  FrontLeft.write(LeftSide);
  FrontRight.write(RightSide);
  RearLeft.write(LeftSide);
  RearRight.write(RightSide);
}