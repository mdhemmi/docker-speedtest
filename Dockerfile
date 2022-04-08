FROM python:3.8-alpine
LABEL email="mcchae@gmail.com"
LABEL name="Jerry Chae"
LABEL Description="alpine python 3.8 speedtest"

RUN apk --update add tzdata bash && \
    cp -f /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone && \
    date && \
    pip install speedtest-cli influxdb_client && \
    rm -rf /var/cache/apk/*

COPY speedtest.py /

ENTRYPOINT [ "/usr/local/bin/python", "/speedtest.py" ]
