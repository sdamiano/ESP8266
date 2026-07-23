import utime

class AHT10:
    def __init__(self, i2c, address=0x38):
        self.i2c = i2c
        self.address = address
        utime.sleep_ms(20)
        self.reset()
        if not self.calibrate():
            raise RuntimeError("No se pudo calibrar el sensor AHT10")

    def reset(self):
        self.i2c.writeto(self.address, b'\xba')
        utime.sleep_ms(20)

    def calibrate(self):
        self.i2c.writeto(self.address, b'\xe1\x08\x00')
        utime.sleep_ms(10)
        status = self.i2c.readfrom(self.address, 1)[0]
        return (status & 0x08) == 0x08

    def _read_raw(self):
        self.i2c.writeto(self.address, b'\xac\x33\x00')
        utime.sleep_ms(80)
        data = self.i2c.readfrom(self.address, 6)
        if (data[0] & 0x80) == 0:
            return data
        return None

    @property
    def relative_humidity(self):
        data = self._read_raw()
        if data is None:
            return None
        raw_humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        return (raw_humidity * 100) / 0x100000

    @property
    def temperature(self):
        data = self._read_raw()
        if data is None:
            return None
        raw_temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5])
        return (raw_temperature * 200) / 0x100000 - 50
