# ESP8266
ESP8266 funcionando con protocolo ESP-NOW

En los proyectos de Internet de las Cosas (IoT), la comunicación inalámbrica entre dispositivos suele depender de una red Wi-Fi local y de protocolos como MQTT o Sockets TCP. Sin embargo, cuando necesitamos conectar dos módulos de forma directa, rápida y sin depender de un router, ESP-NOW —el protocolo desarrollado por Espressif— es el rey indiscutido.

En este artículo técnico, documentaremos cómo conectar un nodo sensor de temperatura y humedad (AHT10) con un nodo receptor equipado con un display LCD 16×2 I2C, utilizando la versión más reciente de MicroPython (v1.23). Además, analizaremos los problemas típicos de bootloop en placas clonadas y cómo solucionarlos.

El Desafío del Hardware: Firmwares Nuevos vs. Memorias Flash
Al trabajar con módulos ESP8266 económicos (como el NodeMCU Amica), las versiones de MicroPython superiores a la v1.22 pueden generar un bucle infinito de reinicios (bootloop) en el primer arranque, inundando la consola de caracteres extraños y congelando entornos como Thonny IDE.

La Solución Definitiva al Bootloop:
Para solucionar esto de raíz, evitamos el instalador automático del IDE y recurrimos a NodeMCU PyFlasher (o esptool.py por línea de comandos) aplicando la siguiente configuración estratégica:

Flash Mode: dio o dout (estos modos de direccionamiento son más compatibles con chips de memoria clonados que el modo qio).

Erase Flash: Seleccionar obligatoriamente Yes para limpiar cualquier residuo corrupto en el sistema de archivos interno (LittleFS).

Nota de arquitectura: Para este proyecto, configuramos ambos módulos con la versión MicroPython v1.23, la cual ya incluye soporte nativo y estable para el módulo espnow.

1. Nodo 1: El Emisor (Sensor AHT10)
El AHT10 es un sensor de alta precisión que trabaja bajo el protocolo I2C. Lo alimentamos estrictamente a 3.3V desde la placa NodeMCU.

Conexiones Físicas (I2C por defecto):
VIN ➡️ 3V3

GND ➡️ GND

SCL ➡️ D1 (GPIO 5)

SDA ➡️ D2 (GPIO 4)

Librería del Sensor (ahtx0.py):
