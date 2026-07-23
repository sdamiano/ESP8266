import utime
from machine import I2C
from lcd_api import LcdApi

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = True  # Corrección del atributo para evitar fallos de inicialización
        
        self.i2c.writeto(self.i2c_addr, b'\x00')
        utime.sleep_ms(20)
        self.hal_write_command(0x33)
        self.hal_write_command(0x32)
        self.hal_write_command(0x28)
        self.hal_write_command(0x0C)
        self.hal_write_command(0x06)
        self.hal_write_command(0x01)
        utime.sleep_ms(2)
        super().__init__(num_lines, num_columns)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0F) << 4
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x0C]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x08]))

    def hal_write_command(self, cmd):
        byte = (cmd & 0xF0) | (0x08 if self.backlight else 0x00)
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        byte = ((cmd & 0x0F) << 4) | (0x08 if self.backlight else 0x00)
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))

    def hal_write_data(self, data):
        byte = (data & 0xF0) | 0x01 | (0x08 if self.backlight else 0x00)
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        byte = ((data & 0x0F) << 4) | 0x01 | (0x08 if self.backlight else 0x00)
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
