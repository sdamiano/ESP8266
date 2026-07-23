import machine
import utime
import network
import espnow
import ahtx0

# 1. Configurar Wi-Fi en modo Estación y forzar Canal 1
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect() 
utime.sleep_ms(100)

# 2. Inicializar ESP-NOW nativo
e = espnow.ESPNow()
e.active(True)

# 3. Dirección MAC del módulo receptor (LCD)
# Reemplazar con la MAC física de su propia placa
MAC_RECEPTOR = b'\x84\xf3\xeb\x12\x34\x56' 
e.add_peer(MAC_RECEPTOR)

# 4. Inicializar bus I2C para el sensor
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)
dispositivos = i2c.scan()

if 0x38 in dispositivos:
    print("Sensor AHT10 listo. Transmitiendo...")
    sensor = ahtx0.AHT10(i2c)
    
    while True:
        try:
            temp = sensor.temperature
            hum = sensor.relative_humidity
            
            # Formateamos los datos empaquetados en un string simple separado por coma
            mensaje = "{:.1f},{:.1f}".format(temp, hum)
            
            # Transmisión directa por el aire
            e.send(MAC_RECEPTOR, mensaje)
            print("Enviado con éxito:", mensaje)
            
        except Exception as err:
            print("Error en el ciclo de envío:", err)
            
        utime.sleep(2)
else:
    print("Error: Sensor AHT10 no detectado en el bus I2C.")
