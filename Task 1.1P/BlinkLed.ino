int PinLed = 13; //Built-in LED
int sleepTime;
int timeBlink;
void setup()
{
  Serial.begin(9600);
  pinMode(PinLed,OUTPUT);
}
void loop()
{
  // Receive the timesBlink from Python 
  timeBlink = Serial.parseInt();
  for (int i = 0 ; i < timeBlink ; i++)
  {
    digitalWrite(PinLed,HIGH);
    delay(500);
    digitalWrite(PinLed,LOW);
    delay(500);
  }
  sleepTime = random(1,10);

  // Send data to serial
  Serial.println(sleepTime);
  Serial.flush();
}
