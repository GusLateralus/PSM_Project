#ifndef RTC_DS3231_H
#define RTC_DS3231_H

#include <Wire.h>
#include <RTClib.h>

// Instancia del RTC DS3231
RTC_DS3231 rtc;

// Variables para almacenar la fecha y hora
String dateStr;
String timeStr;

void rtc_setup() {
  // Iniciar comunicación serial
  //Serial.begin(9600);

  // Iniciar comunicación con el RTC DS3231
  if (!rtc.begin()) {
      Serial.println("Error al detectar el RTC DS3231. Verifica la conexión.");
      //while (1); // Detener si no se detecta el RTC
  }

  // Si el RTC ha perdido energía, ajusta la fecha y hora a la compilación del código
  if (rtc.lostPower()) {
      Serial.println("RTC perdido, ajustando a la fecha y hora de compilación.");
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  else{
    Serial.println("RTC iniciado correctamente.");
    //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  // Configurar alarma para que se active cada minuto
  rtc.writeSqwPinMode(DS3231_OFF); // Apagar señal SQW
  rtc.setAlarm1(
    rtc.now() + TimeSpan(0, 0, 1, 0), // Activar alarma en 1 minuto
    DS3231_A1_Minute // Tipo de alarma
  );
}

// Función para actualizar las cadenas de fecha y hora
void print_rtc_datetime() {
    DateTime now = rtc.now();

    // Crear cadena para la fecha en formato dd/mm/yyyy
    char dateBuffer[11]; // Tamaño suficiente para "dd/mm/yyyy\0"
    snprintf(dateBuffer, sizeof(dateBuffer), "%02d/%02d/%04d", now.day(), now.month(), now.year());
    dateStr = String(dateBuffer); // Guardar en variable

    // Crear cadena para la hora en formato hh:mm:ss
    char timeBuffer[9]; // Tamaño suficiente para "hh:mm:ss\0"
    snprintf(timeBuffer, sizeof(timeBuffer), "%02d:%02d:%02d", now.hour(), now.minute(), now.second());
    timeStr = String(timeBuffer); // Guardar en variable
}



// // Función para obtener la hora en formato hh:mm:ss
// String get_rtc_time() {
//     DateTime now = rtc.now();
//     char buf[9]; // Para almacenar el formato de la hora
//     snprintf(buf, sizeof(buf), "%02d:%02d:%02d", now.hour(), now.minute(), now.second());
//     return String(buf);
// }

// // Función para obtener la fecha en formato dd/mm/yyyy
// String get_rtc_date() {
//     DateTime now = rtc.now();
//     char buf[11]; // Para almacenar el formato de la fecha
//     snprintf(buf, sizeof(buf), "%02d/%02d/%04d", now.day(), now.month(), now.year());
//     return String(buf);
// }

#endif