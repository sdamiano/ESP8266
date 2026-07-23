# 📡 Comunicación IoT Punto a Punto con ESP8266 + ESP-NOW (MicroPython v1.23)

[![MicroPython](https://img.shields.io/badge/MicroPython-v1.23-blue.svg)](https://micropython.org/)
[![Hardware](https://img.shields.io/badge/Hardware-ESP8266%20%7C%20NodeMCU-orange.svg)](https://www.espressif.com/)
[![Protocol](https://img.shields.io/badge/Protocol-ESP--NOW-green.svg)](https://www.espressif.com/en/products/software/esp-now/overview)

En proyectos de Internet de las Cosas (IoT), la comunicación entre dispositivos suele depender de redes Wi-Fi locales y protocolos como MQTT o Sockets TCP. Sin embargo, cuando se requiere conectar dos módulos de forma directa, rápida y sin depender de un router, **ESP-NOW** es el protocolo ideal.

Este proyecto documenta la implementación de una estación de telemetría punto a punto: un **nodo sensor de temperatura y humedad (AHT10)** transmite datos mediante ESP-NOW a un **nodo receptor con pantalla LCD 16x2 I2C**, utilizando **MicroPython v1.23**.

---

## 🛠️ Arquitectura del Sistema

```text
  ┌─────────────────────────┐                   ┌─────────────────────────┐
  │   NODO 1: EMISOR        │                   │   NODO 2: RECEPTOR      │
  │                         │                   │                         │
  │   [Sensor AHT10]        │   ESP-NOW (2.4GHz)│   [Display LCD 16x2]    │
  │         │               │ ────────────────► │         │               │
  │      (I2C)              │     Canal 1       │      (I2C)              │
  │         ▼               │                   │         ▼               │
  │   ESP8266 NodeMCU       │                   │   ESP8266 NodeMCU       │
  └─────────────────────────┘                   └─────────────────────────┘
```

---

## 🚀 Solución al Bootloop (Firmware v1.23 vs. Memorias Flash)

> [!WARNING]
> Al actualizar módulos ESP8266 económicos (como NodeMCU Amica con chips clonados) a MicroPython **v1.22+**, suele generarse un bucle infinito de reinicios (**bootloop**), inundando la consola de caracteres extraños y congelando el IDE. Flashear directamente desde IDEs como Thonny no resuelve este problema.

### Configuración Correcta de Flasheo con NodeMCU PyFlasher

Para revivir las placas y garantizar un arranque estable:

1. Utilizar **NodeMCU PyFlasher** (o `esptool.py` vía terminal).
2. **Flash Mode:** Seleccionar **`dio`** o **`dout`** (*evitar el modo `qio`, ya que genera incompatibilidad con la memoria de varios chips clonados*).
3. **Erase Flash:** Seleccionar obligatoriamente **`Yes`** (imprescindible para limpiar residuos corruptos en el sistema de archivos interno `LittleFS`).

---

## 🔌 Hardware y Conexiones

### 1. Nodo Emisor (Sensor AHT10)
Alimentado estrictamente a **3.3V** desde la placa NodeMCU.

| Pin AHT10 | Pin NodeMCU (ESP8266) | Descripción |
| :---: | :---: | :--- |
| **VIN** | `3V3` | Alimentación 3.3V |
| **GND** | `GND` | Tierra |
| **SCL** | `D1` (GPIO 5) | Reloj I2C |
| **SDA** | `D2` (GPIO 4) | Datos I2C |

---

### 2. Nodo Receptor (Display LCD 16x2 I2C)
El adaptador I2C del display funciona de forma óptima a **5V**. Se conecta al pin `VIN` del NodeMCU (que toma energía directa del puerto USB).

| Pin LCD I2C | Pin NodeMCU (ESP8266) | Descripción |
| :---: | :---: | :--- |
| **VCC** | `VIN` | Alimentación 5V (desde puerto USB) |
| **GND** | `GND` | Tierra |
| **SCL** | `D1` (GPIO 5) | Reloj I2C |
| **SDA** | `D2` (GPIO 4) | Datos I2C |

> [!TIP]
> **Calibración:** Si el display enciende pero no muestra caracteres, ajustar el potenciómetro azul ubicado en el adaptador I2C posterior.

---

## 📂 Organización de Archivos (.py)

Para ejecutar el proyecto, se deben subir las librerías indicadas a la memoria interna de cada NodeMCU antes de cargar el script principal de cada nodo.

### 📡 Archivos del Emisor
* **`ahtx0.py`**: Controlador de hardware para la lectura de registros del sensor AHT10.
* **`emisor.py`**: Script principal (*renombrar a `main.py` al subirlo a la placa*).
  * *Detalle de funcionamiento:* Aísla la radio en el **Canal 1** (`wlan.disconnect()`) y envía las tramas de telemetría a la dirección MAC del receptor.

### 📺 Archivos del Receptor
* **`lcd_api.py`**: Abstracción y control genérico de comandos para pantallas LCD.
* **`esp8266_i2c_lcd.py`**: Driver físico que conecta la API del LCD con el bus I2C.
* **`receptor.py`**: Script principal (*renombrar a `main.py` al subirlo a la placa*).
  * *Detalle de funcionamiento:* Permanece en escucha abierta en el **Canal 1** capturando el buffer con `e.recv()` y renderiza los datos recibidos.

> [!IMPORTANT]
> **Fix de Herencia en MicroPython v1.21+:** En `esp8266_i2c_lcd.py`, la propiedad `self.backlight = True` debe instanciarse en la **primera línea** del constructor para evitar un error de tipo `AttributeError: 'I2cLcd' object has no attribute 'backlight'`.

---

## 📌 Conclusiones

* **Velocidad y Eficiencia:** La comunicación vía ESP-NOW logra una latencia de respuesta en el orden de los milisegundos sin sobrecarga de infraestructura.
* **Independencia de Red:** Ideal para nodos distribuidos (estaciones meteorológicas caseras, sensores agrícolas rurales o telemetría rápida) que operan sin router Wi-Fi.
* **Claves del Éxito:** Flasheo en modo `dio`/`dout` con borrado completo de memoria flash y la sincronización manual estricta del canal de radiofrecuencia entre ambas antenas.
