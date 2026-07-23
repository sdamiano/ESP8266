import machine
import utime
import network
import espnow
from esp8266_i2c_lcd import I2cLcd

# 1. Mapear e inicializar pantalla LCD
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)
dispositivos = i2c.scan()

if dispositivos:
    # El adaptador I2C suele responder en 0x27 o 0x3F
    lcd = I2cLcd(i2c, dispositivos[0], 2, 16)
    lcd.clear()
    lcd.putstr("ESP-NOW v1.23")
    lcd.move_to(0, 1)
    lcd.putstr("Sintonizando...")
    
    # 2. Forzar modo Estación y Canal 1 para escuchar al emisor
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    utime.sleep_ms(100)
    
    # 3. Encender el motor ESP-NOW
    e = espnow.ESPNow()
    e.active(True)
    
    print("Receptor a la escucha en Canal 1...")
    lcd.clear()
    lcd.putstr("Esperando datos")
    
    while True:
        # Escucha activa con una ventana de tiempo de 500ms
        host, msg = e.recv(500)
        
        if msg:
            try:
                # Decodificación y segmentación de datos
                datos_string = msg.decode('utf-8')
                temp, hum = datos_string.split(',')
                
                # Actualización de la interfaz en el display
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Temp: " + temp + " C")
                lcd.move_to(0, 1)
                lcd.putstr("Humedad: " + hum + " %")
                
            except Exception as err:
                print("Error de procesamiento de trama:", err)
        
        utime.sleep_ms(50)
else:
    print("Error: No se encontró la pantalla LCD en la dirección I2C esperada.")
