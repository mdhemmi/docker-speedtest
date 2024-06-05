FROM python:3.8-alpine
LABEL email="hemmi@xmsoft.de"
LABEL name="Michael Hempel"
LABEL Description="alpine python 3.8 speedtest"

RUN apk --update add tzdata bash && \
    cp -f /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    echo "Europe/Berlin" > /etc/timezone && \
    date && \
    pip install speedtest-cli influxdb_client && \
    rm -rf /var/cache/apk/*

COPY speedtest.py /

ENTRYPOINT [ "/usr/local/bin/python", "/speedtest.py" ]
