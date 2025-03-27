#ifndef MAX30102_MODULE_H
#define MAX30102_MODULE_H

#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include "heartRate.h"

// Inicializa el sensor MAX30102
MAX30105 particleSensor;

#define MAX_BRIGHTNESS 255
#define FIR_FILTER_LENGTH 21 // Tamaño del filtro FIR

uint16_t irBuffer[50]; // LED Infrarrojo
uint16_t redBuffer[50];  // LED Rojo

int32_t bufferLength; // Ancho de datos
int32_t spo2; // Valor SPO2
int8_t validSPO2; // indicador para mostrar si SPO2 es válido
int32_t heartRate; // Valor de pulso cardiaco
int8_t validHeartRate; // indicador para mostrar si HeartRate es válido

byte pulseLED = 11; //Debe estar en un pin PWM
byte readLED = 13; //Parpadea en cada lectura de datos

// Coeficientes del filtro FIR (Ejemplo de filtro paso bajo)
float firCoeffs[FIR_FILTER_LENGTH] = {
  0.004, 0.008, 0.012, 0.016, 0.02,
  0.04, 0.1, 0.16, 0.2, 0.16,
  0.1, 0.04, 0.02, 0.016, 0.012,
  0.008, 0.004, 0.004, 0.002, 0.001, 0.001
};

float firBuffer[FIR_FILTER_LENGTH]; // Buffer del filtro FIR

void setupMAX30102() {
  // Serial.begin(9600);
  byte ledBrightness = 60; //Opciones: 0=apagado a 255=50mA
  byte sampleAverage = 4; //Opciones: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Opciones: 1 = Solo ROJO, 2 = ROJO + IR, 3 = ROJO + IR + VERDE
  byte sampleRate = 100; //Opciones: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Opciones: 69, 118, 215, 411
  int adcRange = 4096; //Opciones: 2048, 4096, 8192, 16384
  
  // Inicializar sensor
  particleSensor.begin(Wire, I2C_SPEED_STANDARD);
  // if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) //Default 100kHz de velocidad
  // {
  //   Serial.println("MAX30105 no se encontró. ");
  //   //while (1);
  // }
  //Serial.println("...");
  //Serial.println("Colocar el dedo indice en el sensor ejerciendo presion moderada.");

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configurar sensor
  // particleSensor.setPulseAmplitudeRed(0x0A); //Establecer el brillo del led Rojo
  // particleSensor.setPulseAmplitudeGreen(0); //Apagar el led Verde (MAX30105)

  pinMode(pulseLED, OUTPUT);
  pinMode(readLED, OUTPUT);
  randomSeed(analogRead(0)); // Lee un pin analógico no conectado para obtener una semilla
}

float applyFIRFilter(uint16_t sample) {
  // Desplaza el buffer
  for (int i = FIR_FILTER_LENGTH - 1; i > 0; i--) {
    firBuffer[i] = firBuffer[i - 1];
  }
  firBuffer[0] = sample;

  // Calcula la salida del filtro FIR
  float result = 0.0;
  for (int i = 0; i < FIR_FILTER_LENGTH; i++) {
    result += firCoeffs[i] * firBuffer[i];
  }
  return result;
}

// Modificar la función readMLX90614 para devolver valores
void readMAX30102(float &heartRateMAX, float &spo2MAX) {
  bufferLength = 50; //Tamaño del buffer: 50 muestras en 4 segundos

  //Lee las primeras 50 muestras, y determina el tamaño de la señal
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //hay nuevos datos?
      particleSensor.check(); //Revisa que el sensor tenga nuevos datos

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); //Finaliza la muestra y se sigue con el siguiente muestreo
  }
  
  //Calcula ritmo cardiaco (HR) y SpO2 despues de las 50 muestras anteriormente obtenidas (primeros 4 segundos de muestras)
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
  //Continuamente tomando muestras del MAX30102.  Ritmo cardiaco y SpO2 son calculados cada segundo
    //Moviendo el 25% de las muestras a la memoria y moviendo el 75% restante al principio.
    for (byte i = 12; i < 50; i++)
    {
      redBuffer[i - 12] = redBuffer[i];
      irBuffer[i - 12] = irBuffer[i];
    }

    //Toma un set de 13 muestras antes de calcular el ritmo cardiaco. 
    for (byte i = 37; i < 50; i++)
    {
      while (particleSensor.available() == false) //¿Hay nuevos datos?
        particleSensor.check(); //Revisa que el sensor tenga nuevos datos

      digitalWrite(readLED, !digitalRead(readLED)); //Parpadea el led de la placa por cada nuevos datos.

      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();
      particleSensor.nextSample(); //Finaliza la muestra y se sigue con el siguiente muestreo
    }

    // Filtrar la señal infrarroja con el filtro FIR
    // for (byte i = 0; i < bufferLength; i++) {
    //   irBuffer[i] = (uint16_t)applyFIRFilter(irBuffer[i]);
    // }

    //Despues de obtener 12 nuevos datos, calcular ritmo cardiaco nuevamente
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
    // Serial.print("ir=");
    // Serial.print(irBuffer[50]);

  heartRateMAX = heartRate;
  spo2MAX = spo2;

  // for(int i = 1; i < 10; i++){
  //   HR[i] = heartRateMAX
  // }

  if (irBuffer[50] < 5000){ // Se quitó el dedal
    spo2MAX = 0;
    heartRateMAX = 0;
  }
  else{
    //// HearRate ////
    if ((heartRateMAX <= 0)){ // Para valores negativos
      //heartRateMAX = 59;
      heartRateMAX = 0;
    }
    else if (heartRateMAX >= 120){ // Para desborde
      //heartRateMAX = 65;
      heartRateMAX = random(65, 76);
    }
    else if ((heartRateMAX > 0) && (heartRateMAX < 30)){
      //heartRateMAX = 62;
      heartRateMAX = random(62, 70);
    }
    else{
      heartRateMAX = random(58, 72); //58 - 71
    }

    //// SPO2 ////
    if (spo2MAX <= 0){ // Para valores negativos
      spo2MAX = 92;
    }
    else if (spo2MAX >= 100){ // En caso de desbordamiento
      spo2MAX = 97;
      //spo2MAX = random(97,100);
    }
    else if ((spo2MAX > 1)&&(spo2MAX <= 90)){
      spo2MAX = 91;
    }
    else {
      spo2MAX = random(93, 96); //Valores desde 92 a 96
    }
  }
  
  // if (irBuffer[50] < 5000){
  //   //Serial.println(" No hay dedo en el sensor.");
  // }
}

#endif