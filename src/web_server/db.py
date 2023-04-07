from influxdb import InfluxDBClient

INFLUX_HOST = 'localhost'
INFLUX_PORT = 8086

INFLUX_DB_NAME = 'test'
INFLUX_WEB_USER = 'web'
INFLUX_DATA_COLLECTOR_USER = 'collector'


class DB:
    def __init__(self, user, password, setup=False):
        self.user = user
        self.password = password
        if setup:
            self._setup_db()
        self.client = InfluxDBClient(
            host=INFLUX_HOST,
            port=INFLUX_PORT,
            username=self.user,
            password=self.password
        )

    def _setup_db(self):
        client = InfluxDBClient(
            host=INFLUX_HOST,
            port=INFLUX_PORT
        )
        client.create_database(INFLUX_DB_NAME)
        client.create_user()
