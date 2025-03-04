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
  tempObjectMLX += 7; // Umbral de temperatura
  //Serial.println(tempObjectMLX);

  if(tempObjectMLX < 32){ // Si se quita el sensor de la muñeca:
    tempObjectMLX -= 7; // Se quita el umbral
    //Serial.println("temp mlx de menor a 32");
  }
  else{
    //tempObjectMLX -= 7;
    //Serial.print("mlx entro en else()");
  }

}

#endif