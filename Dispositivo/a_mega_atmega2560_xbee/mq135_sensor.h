// // mq135_sensor.h
// #ifndef MQ135_SENSOR_H
// #define MQ135_SENSOR_H

// #include <Arduino.h>

// // Definir el pin analógico al que está conectado el sensor MQ135
// const int MQ135_PIN = A0;

// // Constantes de calibración
// const float RLOAD = 10.0; // Resistencia de carga en kilo-ohmios
// const float RZERO = 76.63;
// const float PARA = 116.6020682;
// const float PARB = 2.769034857;

// // Función para inicializar el sensor MQ135
// void setupMQ135() {
//     //Serial.begin(9600);
// }

// // Función para calcular la resistencia del sensor
// float getMQ135Resistance(int rawADC) {
//     return ((1023.0 / (float)rawADC) - 1.0) * RLOAD;
// }

// // Función para calcular el ppm de CO2 aproximado
// float getMQ135PPM(float resistance) {
//     return PARA * pow((resistance / RZERO), -PARB);
// }

// // Función para leer y procesar los datos del sensor MQ135
// void readMQ135(float &ppmMQ135) {
//     // Leer el valor analógico del sensor
//     int sensorValue = analogRead(MQ135_PIN);
    
//     // Calcular la resistencia del sensor
//     float resistance = getMQ135Resistance(sensorValue);
    
//     // Calcular el ppm de CO2
//     ppmMQ135 = getMQ135PPM(resistance);
    
//     // Imprimir los valores
//     // Serial.print("Analog value: ");
//     // Serial.print(sensorValue);
//     // Serial.print(" | Resistance: ");
//     // Serial.print(resistance);
//     Serial.print("CO2 = ");
//     Serial.print(ppmMQ135);
//     Serial.println(" ppm");
// }

// #endif

#ifndef MQ135_SENSOR_H
#define MQ135_SENSOR_H

// #include <Arduino.h>

// // Definir el pin analógico al que está conectado el sensor MQ135
// const int MQ135_PIN = A0;

// // Constantes de calibración
// const float RLOAD = 10.0; // Resistencia de carga en kilo-ohmios
// const float RZERO = 76.63; // Valor de resistencia en aire limpio (ajustar tras la calibración)
// const float PARA = 116.6020682; // Constante A del gráfico de la hoja de datos del MQ135
// const float PARB = 2.769034857; // Constante B del gráfico de la hoja de datos del MQ135

// // Función para calcular la resistencia del sensor
// float getMQ135Resistance(int rawADC) {
//     return ((1023.0 / (float)rawADC) - 1.0) * RLOAD; 
// }

// // Función para calcular el ppm de CO2 aproximado
// float getMQ135PPM(float resistance) {
//     return PARA * pow((resistance / RZERO), -PARB);
// }

// // Función para inicializar el sensor MQ135
// void setupMQ135() {
//     Serial.begin(115200);
// }

// // Función para leer y procesar los datos del sensor MQ135
// void readMQ135(float &ppmMQ135) {
//     // Leer el valor analógico del sensor
//     int sensorValue = analogRead(MQ135_PIN);
    
//     // Calcular la resistencia del sensor
//     float resistance = getMQ135Resistance(sensorValue);
    
//     // Calcular el ppm de CO2
//     ppmMQ135 = getMQ135PPM(resistance);
    
//     // Imprimir los valores
//     Serial.print("Analog value: ");
//     Serial.print(sensorValue);
//     Serial.print(" | Resistance: ");
//     Serial.print(resistance);
//     Serial.print(" kOhm | CO2: ");
//     Serial.print(ppmMQ135);
//     Serial.println(" ppm");
// }

#include <MQ135.h> // Biblioteca para trabajar con el MQ135
#include <Wire.h>

#define MQ135_PIN A0  // Pin donde está conectado el sensor
#define NUM_READINGS 10 // Tamaño de la ventana para la media móvil

MQ135 mq135_sensor(MQ135_PIN);

// Variables para la media móvil
float readings[NUM_READINGS]; // Almacena las lecturas
int readIndex = 0;            // Índice actual de la ventana
float total = 0;              // Suma total de las lecturas
float average = 0;            // Promedio de las lecturas

void setupMQ135() {
  // Serial.begin(9600);
  // Serial.println("Calibrando el sensor MQ135...");
  // delay(1000);  // Tiempo para estabilizar el sensor
  // Serial.println("Sensor listo.");

  // Inicializar el array de lecturas
  for (int i = 0; i < NUM_READINGS; i++) {
    readings[i] = 0;
  }
}

void readMQ135(float &ppmMQ135, float &temp, float &hum) {
  // Leer el valor actual del sensor
  float rzero = mq135_sensor.getRZero();
  float correctedRZero = mq135_sensor.getCorrectedRZero(temp, hum);
  float resistance = mq135_sensor.getResistance();
  float ppm = mq135_sensor.getPPM();
  int correctedPPM = mq135_sensor.getCorrectedPPM(temp, hum);
  
  // Actualizar el total para la media móvil
  total = total - readings[readIndex];  // Restar el valor más antiguo
  readings[readIndex] = correctedPPM;   // Agregar la nueva lectura
  total = total + readings[readIndex];  // Actualizar el total
  
  // Mover el índice
  readIndex = (readIndex + 1) % NUM_READINGS;
  
  // Calcular la media móvil
  average = total / NUM_READINGS;
  
  average =+ 356;
  correctedPPM += 456; //356
  ppmMQ135 = correctedPPM;

  if(ppmMQ135 < 0){
    ppmMQ135 = 0;
  }
  else if(ppmMQ135 > 3000){
    ppmMQ135 = 500;
  }
  else{

  }
  // Mostrar los valores en el monitor serial
  Serial.print("PPM (crudo): ");
  Serial.print(ppm);
  Serial.print(" | PPM (media móvil): ");
  Serial.print(average);
  Serial.print(" | Corrected PPM: ");
  Serial.println(ppmMQ135);
  
  //delay(2000); // Leer cada 2 segundos
}


#endif
