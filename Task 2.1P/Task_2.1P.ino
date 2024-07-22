#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN,DHTTYPE);

float humid,temp;

void setup()
{
  Serial.begin(9600);

  dht.begin();
}
void loop()
{
  humid = dht.readHumidity();
  temp = dht.readTemperature();

  Serial.print(humid);
  Serial.print(",");
  Serial.println(temp);

  delay(10000);
}
