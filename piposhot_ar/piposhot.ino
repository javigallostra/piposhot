#include <Servo.h>

const int PINdcMotor1 = 10;
const int PINdcMotor2 = 11;
const int PINservoV = 5;
const int PINservoH = 6;
const int maxServoV = 170;
const int minServoV = 100;
const int maxServoH = 180;
const int minServoH = 0;
const int maxDCvel = 255;//127;
const int minDCvel = 0;
const int DCvelLow = 50;
Servo servoV;
Servo servoH;
int servoVpos = 100;
int servoHpos = 180;
int dcMotor1Vel = 150;
int dcMotor2Vel = 150;

int dcMotorsSpeed(int DCspeed)
{
  /* Function to spin the DC motors at a certain speed */
  // 1 - Check limits
  if (DCspeed > maxDCvel || DCspeed < minDCvel)
  {
    return 1;
  }
  // 2 - Send speed to motors
  else
  {
    dcMotor1Vel = DCspeed;
    dcMotor2Vel = DCspeed;
    analogWrite(PINdcMotor1, dcMotor1Vel);
    analogWrite(PINdcMotor2, dcMotor2Vel);
    return 0;
  }
}

void dcMotorsLow()
{
  /* Function to activate the DC motors at low speed */
  dcMotor1Vel = DCvelLow;
  dcMotor2Vel = DCvelLow;
  analogWrite(PINdcMotor1, dcMotor1Vel);
  analogWrite(PINdcMotor2, dcMotor1Vel);
}

void dcMotorsStop()
{
  /* Function to stop the DC motors */
  dcMotor1Vel = 0;
  dcMotor2Vel = 0;
  analogWrite(PINdcMotor1, dcMotor1Vel);
  analogWrite(PINdcMotor2, dcMotor1Vel);
}

int servoVMoveTo(int angle)
{
  /* Function to move the servo V to a desired angle */
  // 1 - Check limits
  if (angle > maxServoV || angle < minServoV)
  {
    return 1;
  }
  // 2 - Select moving direction
  int adiff = angle - servoVpos;
  if (adiff == 0)
  {
    // 2.1 - We are at the desired angle
    return 0;
  }
  else if (adiff > 0)
  {
    // 2.2 - Increase angle
    while (servoVpos != angle)
    {
      servoVpos = servoVpos + 1;
      servoV.write(servoVpos);
      delay(100);
    }
    return 0;
  }
  else if (adiff < 0)
  {
    // 2.3 - Decrease angle
    while (servoVpos != angle)
    {
      servoVpos = servoVpos - 1;
      servoV.write(servoVpos);
      delay(100);
    }
    return 0;
  }
  
}

int servoHMoveTo(int angle) {
  /* Function to move the servo H to a desired angle */
  // 1 - Check limits
  if (angle > maxServoH || angle < minServoH)
  {
    return 1;
  }
  // 2 - Select moving direction
  int adiff = angle - servoHpos;
  if (adiff == 0)
  {
    // 2.1 - We are at the desired angle
    return 0;
  }
  else if (adiff > 0)
  {
    // 2.2 - Increase angle
    while (servoHpos != angle)
    {
      servoHpos = servoHpos + 1;
      servoH.write(servoHpos);
      delay(100);
    }
    return 0;
  }
  else if (adiff < 0)
  {
    // 2.3 - Decrease angle
    while (servoHpos != angle)
    {
      servoHpos = servoHpos - 1;
      servoH.write(servoHpos);
      delay(100);
    }
    return 0;
  }
  
}

void servoVswipe()
{
  /* Functino to swipe the servo V to max and min */
  while (servoVpos < maxServoV)
  {
    servoVpos = servoVpos + 1;
    servoV.write(servoVpos);
    delay(100);
  }
  while (servoVpos > minServoV)
  {
    servoVpos = servoVpos - 1;
    servoV.write(servoVpos);
    delay(100);
  }
}

void servoHswipe()
{
  /* Functino to swipe the servo H to max and min */
  while (servoHpos < maxServoH)
  {
    servoHpos = servoHpos + 1;
    servoH.write(servoHpos);
    delay(100);
  }
  while (servoHpos > minServoH)
  {
    servoHpos = servoHpos - 1;
    servoH.write(servoHpos);
    delay(100);
  }
}

void setup()
{
  // 1 - Define PIN functions
  pinMode(PINdcMotor1, OUTPUT);
  pinMode(PINdcMotor2, OUTPUT);
  servoV.attach(PINservoV);
  servoH.attach(PINservoH);
  // 2 - Begin Serial communication
  Serial.begin(9600);
  // 3 - Move servos to initial position
  //servoV.write(servoVpos);
  //servoH.write(servoHpos);
  // 4 - Wait 10 seconds for safety
  delay(100);
}

void loop()
{
  dcMotorsSpeed(200);
}
