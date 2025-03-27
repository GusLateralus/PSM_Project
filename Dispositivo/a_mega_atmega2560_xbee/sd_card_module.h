// sd_card_module.h
#ifndef SD_CARD_MODULE_H
#define SD_CARD_MODULE_H

#include <SPI.h>
#include <SD.h>

#define SD_PIN 53

File dataFile;
int timeSEC;

void setupSD() {
  //pinMode(10, OUTPUT);  // Asegúrate de configurar el pin CS como salida

  // Inicializa la tarjeta SD
  if (!SD.begin(SD_PIN)) {
    Serial.println("Error al inicializar la tarjeta SD!");
    return;
  }
  Serial.println("Tarjeta SD inicializada correctamente.");
  
  //SD.remove("datos.csv");
  if(!SD.exists("datos.csv"))
  {
      //SD.remove("datos.csv");
      dataFile = SD.open("datos.csv", FILE_WRITE);
      if (dataFile) {
        //dataFile.println("Tiempo, Temperatura (DHT11), Humedad (DHT11), PPM (MQ135), Temp. Ambiente (MLX90614), Temp. Objeto (MLX90614), Pulso Card. (MAX30102), Oxigenacion (MAX30102)");
        Serial.println("Archivo datos.csv creado y encabezado añadido.");
        dataFile.println("Fecha, Hora, Temp. Ambiental (DHT11), Humedad (DHT11), CO2 PPM (MQ135),  Temp. Corporal (MLX90614), Pulso Card. (MAX30102), Oxigenacion (MAX30102)");
        dataFile.close();
      } else {

        Serial.println("Error creando el archivo datos.csv");
      }
  }
  else{
    Serial.println("Escribiendo en archivo .csv existente...");
  }
}

void writeDataToSD(String dateStr, String timeStr, float tempDHT, float humDHT, int ppmMQ135, float tempObjectMLX, float heartRateMAX, float spo2MAX) {
  //delay(1);
  dataFile = SD.open("datos.csv", FILE_WRITE);
  if (dataFile) {
    // Escribir datos en formato CSV
    dataFile.print(dateStr); // Escribir la fecha DS3231
    dataFile.print(", "); 
    dataFile.print(timeStr); // Escribir la hora DS3231
    dataFile.print(", ");
    dataFile.print(tempDHT); // Temperatura DHT11
    dataFile.print(", ");
    dataFile.print(humDHT); // Humedad DHT11
    dataFile.print(", ");
    dataFile.print(ppmMQ135); // CO2 MQ135
    dataFile.print(", ");
    // dataFile.print(tempAmbientMLX); // Temperatura entorno MLX90614
    // dataFile.print(", ");
    dataFile.print(tempObjectMLX); // Temperatura persona MLX90614
    dataFile.print(", ");
    dataFile.print(heartRateMAX); // Pulso cardíaco MAX30102
    dataFile.print(", ");
    dataFile.println(spo2MAX); // SPO2 MAX30102

    dataFile.close();
  } 
  else {
    Serial.println("Error al abrir el archivo para escribir.");
  }
}

#endif