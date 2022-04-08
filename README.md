# About this container

[docker hub site](https://hub.docker.com/repository/docker/mcchae/speedtest)

[github source](https://github.com/mcchae/docker-speedtest)

This is a speedtest container using [speedtest-cli](https://pypi.org/project/speedtest-cli/) on alpine-python3.8.

Based on [docker hub python](https://hub.docker.com/_/python/).
with [python:3.8-alpine Dockerfile](https://github.com/docker-library/python/blob/0a9ee3e64588bb1144d6e4e413a0c5dd5cd48651/3.8/alpine3.15/Dockerfile).

Originally this container's idea comes from [robinmanuelthiel/speedtest](https://github.com/robinmanuelthiel/speedtest). His main implementation is shell script and sometimes does not work so I create a new Python implementation.

## Environmental variables

Variable | Description | Example
---|---|---
LOOP_DELAY | checking every ***n*** seconds | 60
DB_HOST | InfluxDB host | http://influxdb:8086
DB_NAME | InfluxDB DB name | speedtest
DB_USERNAME | InfluxDB user | admin
DB_PASSWORD | InfluxDB password | admin_passW0rd


## cmd
Default CMD is:

```
/usr/local/bin/python /speedtest.py
```

## Tags

[1.0](https://hub.docker.com/layers/201881182/mcchae/speedtest/1.0/images/sha256-8e74fc23e74fa0b65c33b2b56f52f1149e5285e1148a023c491e09f204eddce6?context=repo) - for linux/amd64
[1.0-arm](https://hub.docker.com/layers/201883519/mcchae/speedtest/1.0-arm/images/sha256-3b224951a1c15b6c0df2796a87fb921435d2e93eb53817aeb4b784a3c07ca234?context=repo) - for linux/arm/v7 (Raspberry pi 3/4)

## Example docker-compose.yaml

```yaml
version: '3'
services:
  # Tests the current internet connection speed
  # once per hour and writes the results into an
  # InfluxDB instance
  speedtest:
    # for AMD CPU
    image: mcchae/speedtest:1.0
    # for ARM CPU
    #image: mcchae/speedtest:1.0-arm
    restart: always
    privileged: true   # Needed for 'sleep' in the loop
    depends_on:
      - influxdb
    environment:
      - LOOP_DELAY=60
      - DB_HOST=http://influxdb:8086
      - DB_NAME=speedtest
      - DB_USERNAME=admin
      - DB_PASSWORD=admin_passW0rd

  # Creates an InfluxDB instance to store the
  # speed test results
  influxdb:
    image: influxdb:1.8
    restart: always
    volumes:
      - influxdb:/var/lib/influxdb
    ports:
      - "8083:8083"
      - "8086:8086"
    environment:
      - INFLUXDB_ADMIN_USER=admin
      - INFLUXDB_ADMIN_PASSWORD=admin_passW0rd
      - INFLUXDB_DB=speedtest

  # Displays the results in a Grafana dashborad
  grafana:
    image: grafana/grafana:latest
    restart: always
    depends_on:
      - influxdb
    ports:
      - 3000:3000
    volumes:
      - grafana:/var/lib/grafana

volumes:
  grafana:
  influxdb:
```

## Dashboard
To configure Grafana, you need to add InfluxDB as a data source and create a dashboard with the upload, download and ping values. You can find a example dashboard configuration in the [speedtest-dashboard.json](speedtest-dashboard.json).

