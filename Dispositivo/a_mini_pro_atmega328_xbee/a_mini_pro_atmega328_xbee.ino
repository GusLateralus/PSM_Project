#include <LowPower.h>
#include "max30102_module.h"  // Módulo del sensor MAX30102
#include "mlx90614_sensor.h"  // Módulo del sensor MLX90614
#include <Wire.h>
#include "LowPower.h"

float tempObjectMLX;
float heartRateMAX;
float spo2MAX;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  setupMAX30102();
  setupMLX90614();
  //Serial.println("A");
}

void loop() {
  // delay(1000);
  //Serial.println();
  // Variables para almacenar datos de los sensores
  float tempObjectMLX;
  float heartRateMAX;
  float spo2MAX;

  // Lee los datos del MLX90614
  readMLX90614(tempObjectMLX);
  // Lee los datos del MAX30102
  readMAX30102(heartRateMAX, spo2MAX);

  delay(100); // Esperar 10 segundo entre envíos
  /* XBee: solo imprimir en serial las variables a utilizar */
  Serial.print(tempObjectMLX); Serial.print(",");
  Serial.print(heartRateMAX); Serial.print(",");
  Serial.println(spo2MAX);

  delay(1000);
   LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF); // Dormir por 8 segundos
  // //sleepForSeconds(10);
  // LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF); // Dormir por 8 segundos
  // Serial.end();    // Apaga la comunicación serial (opcional)
  // Serial.begin(115200); // Reinicia la comunicación serial
  // delay(10);
  // Poner el microcontrolador en modo powerSave durante 5 segundos
  // for (int i = 0; i < 5; i++) {
  //     LowPower.powerSave(SLEEP_1S, ADC_OFF, BOD_OFF, TIMER2_ON);
  // }
}

// void sleepForSeconds(int seconds) {
//   int sleepCycles = seconds / 8; // Número total de ciclos de 8 segundos
//   for (int i = 0; i < sleepCycles; i++) {
//     LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF); // Dormir por 8 segundos
//   }
// }