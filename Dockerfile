FROM soulteary/cronicle:0.9.46

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache python3 py3-pip

COPY bin/python-script-plugin.py /opt/cronicle/bin/python-script-plugin.py
RUN chmod +x /opt/cronicle/bin/python-script-plugin.py
COPY config/plugins.pixl /tmp/plugins.pixl
RUN /opt/cronicle/bin/control.sh import /tmp/plugins.pixl
