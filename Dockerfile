FROM soulteary/cronicle:0.9.46

ENV PYTHONUNBUFFERED=1

COPY bin/python-script-plugin.py /opt/cronicle/bin/python-script-plugin.py
RUN chmod +x /opt/cronicle/bin/python-script-plugin.py

RUN apk add --no-cache python3 py3-pip
