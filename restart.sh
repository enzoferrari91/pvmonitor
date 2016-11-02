#!/bin/bash

echo "Starte Flask Webserver..."

cd /home/pi/Desktop/python/hoelzl

sudo service apache2 stop

nohup sudo python app.py >/dev/null 2>&1 &

echo "Fertig:  $(date)"
