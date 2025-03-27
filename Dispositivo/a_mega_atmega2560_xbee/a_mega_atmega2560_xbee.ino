#include "mq135_sensor.h"
#include "dht11_sensor.h"
#include "rtc_module.h"
#include "sd_card_module.h"

String receivedData = ""; // Para almacenar los datos recibidos

float tempDHT, humDHT;
float ppmMQ135;
float tempObjectMLX;
float heartRateMAX;
float spo2MAX;

void setup() {
    Serial.begin(9600);
    Serial1.begin(9600); // Configura el XBee en el Mega
    
    // Inicializar módulos
    Serial.print("\nHabilitando sensores y módulos...");
    Serial.println("");
    delay(100);

    // Configura los sensores
    initDHT11();
    //initRFM69();
    rtc_setup(); // Iniciar el RTC DS3231

    Serial.println("Sensores configurados y listos para continuar.");

    // Configura la tarjeta SD
    setupSD();

    // Iniciar mediciones (entrar al void loop())
    //Serial.println(F("Fije el sensor al dedo. Presione cualquier tecla para iniciar la conversión."));
    // while (Serial.available() == 0); // Wait until user presses a key
    // Serial.read();
    
  // Verifica si hay datos disponibles en Serial1
  //int response = 0;

  // while(1){ // Espera a que se encienda la pulsera
  //   if (Serial1.available()) {
  //     Serial.println("ok");
  //   break;
  //   }
  // }
  Serial.println("Esperando para recibir los datos de la pulsera...");
}

void loop(){      
  // sensores();
  // limpiar();
  if (Serial1.available()){
    //Serial.println("...");
    char receivedChar = Serial1.read();
    delay(100);
    // Verifica el final de línea
    if (receivedChar == '\n') {
      parseData(); // Procesa los datos recibidos
      sensores();
      limpiar();
      //delay(100);
    }
    else {
      receivedData += receivedChar; // Agrega el carácter recibido
    }
  }

  // Espera 2 segundos antes de la siguiente lectura
  //delay(1000);
}

void limpiar(){
  // Limpia las variables para el siguiente paquete
  float tempDHT, humDHT;
  float ppmMQ135;
  float tempObjectMLX;
  float heartRateMAX;
  float spo2MAX;

  receivedData = ""; // Limpia la variable para el siguiente paquete
}

void sensores(){
  // Lee los datos del DS3231
  print_rtc_datetime();  // Imprimir la hora y fecha
  Serial.println(dateStr); // Imprimir fecha
  Serial.println(timeStr); // Imprimir hora

  // Lee los datos del DHT11
  readDHT(tempDHT, humDHT);

  // Lee los datos del MQ135
  readMQ135(ppmMQ135, tempDHT, humDHT);

  // Muestra los valores recibidos para verificar
  Serial.print("MLX90614 Object = "); Serial.print(tempObjectMLX); Serial.println(" *C");
  //Serial.print(", Object = "); Serial.print(tempObjectMLX); Serial.println("*C");
  Serial.print("MAX30102 HR = "); Serial.print(heartRateMAX); Serial.print(" bpm");
  Serial.print(", SPO2 = "); Serial.print(spo2MAX); Serial.println("%");

  // Escribe los datos en la tarjeta SD
  writeDataToSD(dateStr, timeStr, tempDHT, humDHT, ppmMQ135, tempObjectMLX, heartRateMAX, spo2MAX);
}

void parseData() {
  int commaIndex1 = receivedData.indexOf(',');
  int commaIndex2 = receivedData.indexOf(',', commaIndex1 + 1);
  //int commaIndex3 = receivedData.indexOf(',', commaIndex2 + 1);

  if (commaIndex1 > 0 && commaIndex2 > 0) {

    tempObjectMLX = receivedData.substring(0, commaIndex1).toFloat();
    heartRateMAX = receivedData.substring(commaIndex1 + 1, commaIndex2).toFloat();
    spo2MAX = receivedData.substring(commaIndex2 + 1).toFloat();
  }
}
