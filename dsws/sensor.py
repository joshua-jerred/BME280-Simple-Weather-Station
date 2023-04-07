from .config import ReadConfig
from .db import DB, Measurment

import random
import smbus
from ctypes import c_short, c_byte
import time


def _short(data, index):
    return c_short((data[index+1] << 8) + data[index]).value


def _ushort(data, index):
    return (data[index+1] << 8) + data[index]


def readBme280(bus, i2c_address):
    _device = smbus.SMBus(bus)
    REG = 0xD0
    EXPECTED = 0x60
    res = _device.read_byte_data(i2c_address, REG)
    if res != EXPECTED:
        print(f"Unexpected response from BME280: {res}")
        return None
    _device.write_byte_data(i2c_address, 0xF2, 0x01)  # Hum 1x oversampling

    s1 = _device.read_i2c_block_data(i2c_address, 0x88, 26)
    s2 = _device.read_i2c_block_data(i2c_address, 0xE1, 7)

    T1 = _ushort(s1, 0)
    T2 = _short(s1, 2)
    T3 = _short(s1, 4)
    P1 = _ushort(s1, 6)
    P2 = _short(s1, 8)
    P3 = _short(s1, 10)
    P4 = _short(s1, 12)
    P5 = _short(s1, 14)
    P6 = _short(s1, 16)
    P7 = _short(s1, 18)
    P8 = _short(s1, 20)
    P9 = _short(s1, 22)
    H1 = s1[25]
    H2 = _short(s2, 0)
    H3 = s2[2]
    H4 = (s2[3] << 4) | (s2[4] & 0xF)
    H5 = (s2[5] << 4) | (s2[4] >> 4)
    H6 = c_byte(s2[6]).value

    # 1x temp, 1x pressure, normal mode
    _device.write_byte_data(i2c_address,  0xF4, 0b00100111)
    _device.write_byte_data(i2c_address,  0xF5, 0b01000000)  # 125ms standby
    time.sleep(0.5)

    data = _device.read_i2c_block_data(i2c_address, 0xF7, 8)
    raw_pressure = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    raw_temperature = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    raw_humidity = (data[6] << 8) | data[7]

    tvar1 = ((raw_temperature >> 3) - ((T1 << 1))) * ((T2)) >> 11

    tvar2 = (((((raw_temperature >> 4) - (T1))
               * ((raw_temperature >> 4)
                  - (T1))) >> 12)
             * (T3)) >> 14
    t_fine_ = tvar1 + tvar2
    T = (t_fine_ * 5 + 128) >> 8
    temp_c_ = T / 100.0

    pvar1 = t_fine_ - 128000
    pvar2 = pvar1 * pvar1 * P6
    pvar2 = pvar2 + ((pvar1 * P5) << 17)
    pvar2 = pvar2 + (P4 << 35)
    pvar1 = ((pvar1 * pvar1 * P3) >> 8) + ((pvar1 * P2) << 12)
    pvar1 = ((((1) << 47) + pvar1)) * (P1) >> 33
    p = 1048576 - raw_pressure
    p = int((((p << 31) - pvar2) * 3125) / pvar1)
    pvar1 = ((P9) * (p >> 13) * (p >> 13)) >> 25
    pvar2 = ((P8) * p) >> 19
    p = ((p + pvar1 + pvar2) >> 8) + ((P7) << 4)
    press_mbar_ = (p / 256.0) / 100.0

    h = (t_fine_ - 76800)
    h = (((((raw_humidity << 14) - ((H4) << 20)
            - ((H5) * h)) + 16384) >> 15)
         * (((((((h * (H6)) >> 10)
                * (((h * (H3)) >> 11)
                   + (32768))) >> 10) + (2097152))
             * (H2) + 8192) >> 14))
    h = (h - (((((h >> 15) * (h >> 15)) >> 7) * (H1))
              >> 4))
    h = 0 if h < 0 else h
    h = 419430400 if h > 419430400 else h
    rh_ = (h >> 12) / 1024.0

    return (temp_c_, rh_, press_mbar_)


def Collect(config_location):
    config = ReadConfig(config_location)
    db = DB(config)

    sensor_cfg = config["sensor"]
    bus = int(sensor_cfg["i2c_bus"])
    i2c_address = int(sensor_cfg["i2c_address"], 16)
    data = readBme280(bus, i2c_address)

    temp = Measurment("air_temperature")
    temp.addTag("sensor", "bme280")
    temp.addField("value", data[0])
    temp.addField("unit", "celsius")

    rh = Measurment("relative_humidity")
    rh.addTag("sensor", "bme280")
    rh.addField("value", data[1])
    rh.addField("unit", "percent")

    pres = Measurment("atmospheric_pressure")
    pres.addTag("sensor", "bme280")
    pres.addField("value", data[2])
    pres.addField("unit", "millibar")

    measurments = [temp, rh, pres]

    db.write(measurments)
