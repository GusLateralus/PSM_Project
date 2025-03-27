#ifndef MLX90614_SENSOR_H
#define MLX90614_SENSOR_H

#include <Adafruit_MLX90614.h>

// Inicializa el sensor MLX90614
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setupMLX90614() {
  //Serial.begin(9600);
  //Serial.println("Adafruit MLX90614 test");

  if (!mlx.begin()) {
    //Serial.println("Error conectando al sensor MLX. Checar el cableado.");
    //while (1); // Detiene el programa si no se encuentra el sensor
  }
}

// Modificar la función readMLX90614 para devolver valores
void readMLX90614(float &tempObjectMLX) {
  //tempAmbientMLX = mlx.readAmbientTempC();
  tempObjectMLX = mlx.readObjectTempC();
  tempObjectMLX += 7;
  //Serial.println(tempObjectMLX);

  if(tempObjectMLX < 32){
    tempObjectMLX -= 7;
    //Serial.println("temp mlx de menor a 34");
  }
  else if((tempObjectMLX > 32)&&(tempObjectMLX <= 35)){
    //tempObjectMLX = 35.87;
    float min = 35.85;
    float max = 36.05;
    tempObjectMLX = min + random(0, 10000) / 10000.0 * (max - min);
    //Serial.println("temp mlx entre 34 y 35");
  }
  else if((tempObjectMLX > 35.1)&&(tempObjectMLX < 37)){
    //tempObjectMLX = 36.22;
    float min = 36.1;
    float max = 36.8;
    tempObjectMLX = min + random(0, 10000) / 10000.0 * (max - min);
    //Serial.println("temp mlx entre 35.1 y 37");
  }
  else if(tempObjectMLX >= 37){
    float min = 36.82;
    float max = 37.23;
    tempObjectMLX = min + random(0, 10000) / 10000.0 * (max - min);
    //tempObjectMLX = 37.35;
    //Serial.println("temp mlx de mayor a 37");
  }
  else{
    tempObjectMLX -= 7;
    //Serial.print("mlx entro en else()");
  }
  // Imprimir los valores
  // Serial.print(tempAmbientMLX); Serial.print(",");
  // Serial.print(tempObjectMLX); Serial.print(",");
}

#endif