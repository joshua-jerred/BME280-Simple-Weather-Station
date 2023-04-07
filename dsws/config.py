import json


def ReadConfig(path):
    config = ""
    with open(path) as f:
        config = json.load(f)
    return CheckConfig(config)


def CheckConfig(config):
    # Database
    if "database" not in config:
        raise Exception("config.json is missing the database section")
    db_config = config["database"]
    if "host" not in db_config:
        raise Exception("config.json is missing the database host")
    if "port" not in db_config:
        raise Exception("config.json is missing the database port")
    if type(db_config["port"]) is not int:
        raise Exception("config.json database port is not an integer")
    if "db_name" not in db_config:
        raise Exception("config.json is missing the database name")
    if "admin_user" not in db_config:
        raise Exception("config.json is missing the admin user")
    if "admin_password" not in db_config:
        raise Exception("config.json is missing the admin password")
    if "web_server_user" not in db_config:
        raise Exception("config.json is missing the web server user")
    if "web_server_password" not in db_config:
        raise Exception("config.json is missing the web server password")
    if "sensor_user" not in db_config:
        raise Exception("config.json is missing the sensor user")
    if "sensor_password" not in db_config:
        raise Exception("config.json is missing the sensor password")
    if "retention_policy" not in db_config:
        raise Exception("config.json is missing the retention policy")

    # Sensor
    if "sensor" not in config:
        raise Exception("config.json is missing the sensor section")
    sensor_config = config["sensor"]
    if "i2c_bus" not in sensor_config:
        raise Exception("config.json is missing the i2c bus")
    if "i2c_address" not in sensor_config:
        raise Exception("config.json is missing the i2c address")
    if "read_interval" not in sensor_config:
        raise Exception("config.json is missing the read interval")
    if type(sensor_config["read_interval"]) is not int:
        raise Exception("config.json read interval is not an integer")

    # Web Server
    if "web_server" not in config:
        raise Exception("config.json is missing the web server section")
    ws_config = config["web_server"]
    if "address" not in ws_config:
        raise Exception("config.json is missing the web server address")
    if "port" not in ws_config:
        raise Exception("config.json is missing the web server port")
    if type(ws_config["port"]) is not int:
        raise Exception("config.json web server port is not an integer")

    return config
