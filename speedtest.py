import os
import sys
import json
import time
import subprocess
import speedtest
from influxdb_client import InfluxDBClient, Point


def run_speedtest():
    cmd = [
        '/usr/local/bin/speedtest',
        '--json',
    ]
    po = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    json_out = po.stdout.read().decode()
    return json.loads(json_out)


def get_test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    return res


def get_result():
    jd = run_speedtest()
    # jd = get_test()
    print(f"{jd['download']},{jd['upload']},{jd['ping']}")


def save_result():
    try:
        jd = run_speedtest()
        print(f"download={jd['download']},upload={jd['upload']},ping={jd['ping']}")
        username = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_NAME')
        retention_policy = 'autogen'
        bucket = f'{database}/{retention_policy}'
        with InfluxDBClient(url=os.environ.get('DB_HOST'), 
                token=f'{username}:{password}', org='-') as client:
            with client.write_api() as write_api:
                point = Point("upload").tag("host", jd['server']['host']).field("value", jd['upload'])
                point.to_line_protocol()
                write_api.write(bucket=bucket, record=point)
                point = Point("download").tag("host", jd['server']['host']).field("value", jd['download'])
                point.to_line_protocol()
                write_api.write(bucket=bucket, record=point)
                point = Point("ping").tag("host", jd['server']['host']).field("value", jd['ping'])
                point.to_line_protocol()
                write_api.write(bucket=bucket, record=point)
    except Exception as err:
        sys.stderr.write(f'Error: {err}')

def do_loop():
    while True:
        save_result()
        loop_delay = int(os.environ.get('LOOP_DELAY', '3600'))
        time.sleep(loop_delay)

if __name__ == '__main__':
    do_loop()
