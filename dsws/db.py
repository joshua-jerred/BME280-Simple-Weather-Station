from influxdb import InfluxDBClient

DEFAULT_FIELD = '*'


class Measurment:
    def __init__(self, name):
        self._name = name
        self._tags = {}
        self._fields = {}

    def addTag(self, key, value):
        self._tags[key] = value

    def addField(self, key, value):
        self._fields[key] = value

    def influxFormat(self):
        return {"measurement": self._name,
                "tags": self._tags,
                "fields": self._fields}


class DB:
    def __init__(self, config):
        self.config = config["database"]
        self.host = self.config["host"]
        self.port = self.config["port"]
        self.admin_user = self.config["admin_user"]
        self.admin_password = self.config["admin_password"]
        self.db_name = self.config["db_name"]
        self.web_server_user = self.config["web_server_user"]
        self.web_server_password = self.config["web_server_password"]
        self.sensor_user = self.config["sensor_user"]
        self.sensor_password = self.config["sensor_password"]

        client = InfluxDBClient(
            self.host,
            self.port,
            self.admin_user,
            self.admin_password,
            self.db_name
        )
        db_version = client.ping()
        if "1.8" not in db_version:
            raise Exception("InfluxDB version 1.8 is required")

        setup = False
        for db in client.get_list_database():
            if db['name'] == self.db_name:
                setup = True
        if not setup:
            print("Setting up DB")
            self.Setup()

        ws_setup = False
        sn_setup = False
        for user in client.get_list_users():
            if user['user'] == self.web_server_user:
                ws_setup = True
            elif user['user'] == self.sensor_password:
                sn_setup = True
        if not (ws_setup and sn_setup):
            print("Setting Up Users")
            self.Setup()
        client.close()

    def Setup(self):
        client = InfluxDBClient(
            self.host,
            self.port,
            self.admin_user,
            self.admin_password,
            self.db_name
        )
        client.create_database(self.db_name)

        client.create_user(
            self.admin_user,
            self.admin_password,
            admin=True
        )
        client.create_user(
            self.web_server_user,
            self.web_server_password,
            admin=False
        )
        client.create_user(
            self.sensor_user,
            self.sensor_password,
            admin=False
        )

        client.grant_privilege(
            'READ',
            self.db_name,
            self.web_server_user
        )
        client.grant_privilege(
            'WRITE',
            self.db_name,
            self.sensor_user
        )
        client.close()

    def write(self, measurments: list):
        client = InfluxDBClient(
            self.host,
            self.port,
            self.sensor_user,
            self.sensor_password,
            self.db_name
        )
        data = []
        for measurment in measurments:
            data.append(measurment.influxFormat())

        client.write_points(data)
        client.close()

    def __web_server_client(self):
        return InfluxDBClient(
            self.host,
            self.port,
            self.web_server_user,
            self.web_server_password,
            self.db_name
        )

    def getMostRecent(self, measurment_name):
        client = self.__web_server_client()
        res = client.query(
            f'SELECT last(value) FROM {measurment_name} WHERE time > now() - 1h limit 1000;')
        client.close()
        res = list(res.get_points(measurement=measurment_name))[0]
        return {'time': res['time'], 'value': res['last']}

    def countEntries(self, measurment_name):
        client = self.__web_server_client()
        res = client.query(
            f'SELECT COUNT(*) FROM "{measurment_name}"')
        res = list(res.get_points(measurement=measurment_name))[0]
        return {'time': res['time'], 'count': res['count_value']}
