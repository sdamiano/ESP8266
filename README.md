# Dos módulos ESP8266 funcionando con protocolo ESP-NOW

## 🛠️ Arquitectura del Sistema

  ┌─────────────────────────┐                   ┌─────────────────────────┐
  │   NODO 1: EMISOR        │                   │   NODO 2: RECEPTOR      │
  │                         │                   │                         │
  │   [Sensor AHT10]        │   ESP-NOW (2.4GHz)│   [Display LCD 16x2]    │
  │         │               │ ────────────────► │         │               │
  │      (I2C)              │     Canal 1       │      (I2C)              │
  │         ▼               │                   │         ▼               │
  │   ESP8266 NodeMCU       │                   │   ESP8266 NodeMCU       │
  └─────────────────────────┘                   └─────────────────────────┘

En los proyectos de Internet de las Cosas (IoT), la comunicación inalámbrica entre dispositivos suele depender de una red Wi-Fi local y de protocolos como MQTT o Sockets TCP. Sin embargo, cuando necesitamos conectar dos módulos de forma directa, rápida y sin depender de un router, ESP-NOW —el protocolo desarrollado por Espressif— es el rey indiscutido.

En este artículo técnico, documentaremos cómo conectar un nodo sensor de temperatura y humedad (AHT10) con un nodo receptor equipado con un display LCD 16×2 I2C, utilizando la versión más reciente de MicroPython (v1.23). Además, analizaremos los problemas típicos de bootloop en placas clonadas y cómo solucionarlos.

## El Desafío del Hardware: Firmwares Nuevos vs. Memorias Flash

Al trabajar con módulos ESP8266 económicos (como el NodeMCU Amica), las versiones de MicroPython superiores a la v1.22 pueden generar un bucle infinito de reinicios (bootloop) en el primer arranque, inundando la consola de caracteres extraños y congelando entornos como Thonny IDE.

## La Solución Definitiva al Bootloop:

Para solucionar esto de raíz, evitamos el instalador automático del IDE y recurrimos a NodeMCU PyFlasher (o esptool.py por línea de comandos) aplicando la siguiente configuración estratégica:

Flash Mode: dio o dout (estos modos de direccionamiento son más compatibles con chips de memoria clonados que el modo qio).

Erase Flash: Seleccionar obligatoriamente Yes para limpiar cualquier residuo corrupto en el sistema de archivos interno (LittleFS).

Nota de arquitectura: Para este proyecto, configuramos ambos módulos con la versión MicroPython v1.23, la cual ya incluye soporte nativo y estable para el módulo espnow.

## 1. Nodo 1: El Emisor (Sensor AHT10)
   
El AHT10 es un sensor de alta precisión que trabaja bajo el protocolo I2C. Lo alimentamos estrictamente a 3.3V desde la placa NodeMCU.

Conexiones Físicas (I2C por defecto):
VIN ➡️ 3V3

GND ➡️ GND

SCL ➡️ D1 (GPIO 5)

SDA ➡️ D2 (GPIO 4)

Librería del Sensor (ahtx0.py):

Debemos subir este controlador a la memoria de la placa para que el script principal pueda interpretar las lecturas de los registros del AHT10.

Script Principal del Emisor (emisor.py):

IMPORTANTE: Al subirlo renombralo como main.py

Detalle crítico de ESP-NOW: Las antenas deben sintonizar obligatoriamente el mismo canal de radio. Usamos wlan.disconnect() para forzar al chip a trabajar de forma aislada en el Canal 1. Además, el emisor debe conocer por bytes hexadecimales la dirección MAC del receptor.

##2. Nodo 2: El Receptor (Display LCD 16×2 I2C)
El adaptador de la pantalla LCD funciona de forma óptima a 5V. Lo conectamos al pin VIN del NodeMCU Amica (que toma la energía directa del puerto USB).

Conexiones Físicas:
VCC ➡️ VIN (5V)

GND ➡️ GND

SCL ➡️ D1 (GPIO 5)

SDA ➡️ D2 (GPIO 4)

Nota de depuración: Si el display enciende pero no muestra caracteres, se debe calibrar el contraste girando el potenciómetro azul ubicado en el adaptador posterior del LCD.

Librerías del LCD:
Para este nodo se requieren dos abstracciones. 

Primero creamos lcd_api.py (control de registros genérico) y luego esp8266_i2c_lcd.py (puente de hardware).

⚠️ Solución a un Bug Común de Herencia: En entornos MicroPython v1.21+, definir comandos de inicialización en el constructor del LCD antes de invocar la clase base provoca un error de tipo AttributeError: 'I2cLcd' object has no attribute 'backlight'. Se solucionó instanciando self.backlight = True en la primera línea del archivo del driver físico.


Script Principal del Receptor (receptor.py):

IMPORTANTE: Al subirlo renombralo como main.py

El receptor no necesita conocer la dirección MAC de la placa emisora; opera en escucha abierta capturando cualquier trama dirigida a su propia interfaz en el Canal 1.

Usamos el método e.recv(timeout) para lograr una lectura activa y fluida del buffer.

Conclusiones

Implementar ESP-NOW en MicroPython v1.23 nos otorga una velocidad de respuesta inmediata (en milisegundos) y rompe la dependencia de una infraestructura de red doméstica. Este ecosistema es ideal para estaciones meteorológicas caseras, sensores agrícolas distribuidos en zonas rurales o telemetría rápida de bajo costo.

Los puntos clave para el éxito de este despliegue fueron la correcta elección de los parámetros de flasheo de la memoria flash (dio) y la sincronización manual estricta del canal de radiofrecuencia de las antenas.

Un detalla importante, al actualizar el firmware de los ESP8266, literalmente dejaron de funcionar (BootLoop). Desde Thonny Python no hubo forma de revivirlos. Si se pudo hacer un flasheo correcto utilizando el software NodeMCU-PyFlasher

##La Solución Definitiva al Bootloop:

Para solucionar esto de raíz, evitamos el instalador automático del IDE y recurrimos a NodeMCU PyFlasher aplicando la siguiente configuración estratégica:

Flash Mode: dio o dout (estos modos de direccionamiento son más compatibles con chips de memoria clonados que el modo qio).

Erase Flash: Seleccionar obligatoriamente Yes para limpiar cualquier residuo corrupto en el sistema de archivos interno (LittleFS).

Nota de arquitectura: Para este proyecto, configuramos ambos módulos con la versión MicroPython v1.23, la cual ya incluye soporte nativo y estable para el módulo espnow.
