from .config import ReadConfig
from .db import DB, Measurment

import random


def Collect(config_location):
    config = ReadConfig(config_location)
    db = DB(config)

    temp = Measurment("air_temperature")
    temp.addTag("sensor", "bme280")
    temp.addField("value", random.uniform(-15.5, 75.0))

    rh = Measurment("relative_humidity")
    rh.addTag("sensor", "bme280")
    rh.addField("value", random.uniform(0, 100))

    pres = Measurment("atmospheric_pressure")
    pres.addTag("sensor", "bme280")
    pres.addField("value", random.uniform(800, 1000))

    measurments = [temp, rh, pres]

    db.write(measurments)
