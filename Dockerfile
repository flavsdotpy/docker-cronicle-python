FROM soulteary/cronicle:0.9.46

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache python3 py3-pip

WORKDIR /opt/cronicle
COPY bin/python-script-plugin.py ./bin/python-script-plugin.py
RUN chmod +x ./bin/python-script-plugin.py
COPY config/python.pixl ./import/python.pixl

COPY bin/entrypoint.sh ./bin/

CMD ["/bin/sh", "bin/entrypoint.sh"]