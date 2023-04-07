# Dead Simple Weather Station
A simple weather station based on the BME280

## Install
Requires InfluxDB 1.8

### Install InfluxDB
[See Here](https://docs.influxdata.com/influxdb/v1.8/) for the most up to date instructions.
```bash
# Add the repository
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list

# Install InfluxDB
sudo apt-get update
sudo apt-get install influxdb

# Start InfluxDB
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
```