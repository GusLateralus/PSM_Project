// dht11_sensor.h
#ifndef DHT11_SENSOR_H
#define DHT11_SENSOR_H

#include <DHT.h>

#define DHTPIN 2     // Pin donde está conectado el DHT11
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void initDHT11() {
    dht.begin();
}

// Modificar la función readDHT para devolver un array de float con temperatura y humedad
void readDHT(float &temp, float &hum) {
  // Lee la humedad
  hum = dht.readHumidity();
  // Lee la temperatura en Celsius
  temp = dht.readTemperature();

  // Verifica si las lecturas han fallado
  if (isnan(hum) || isnan(temp)) {
    Serial.println("Fallo al leer del sensor DHT!");
    return;
  }

  // Imprime los valores en el monitor serial
  Serial.print("DHT11 ");
  Serial.print("Humedad = ");
  Serial.print(hum);
  Serial.print("%, ");
  Serial.print("Temperatura = ");
  Serial.print(temp);
  Serial.println(" *C");
}

#endif
