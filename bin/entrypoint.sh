#!/bin/sh

if [ -e /opt/cronicle/logs/_python_plugin_imported ]
then
  echo "Python plugin already imported!"
else
  echo "Importing python plugin..."
  /opt/cronicle/bin/control.sh import /opt/cronicle/import/python.pixl
  touch /opt/cronicle/logs/_python_plugin_imported
  echo "Python plugin successfully imported!"
fi

cd /opt/cronicle && node bin/docker-entrypoint.js
