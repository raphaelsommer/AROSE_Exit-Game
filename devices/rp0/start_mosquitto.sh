#!/bin/bash

sudo killall mosquitto
sudo mosquitto -c /etc/mosquitto/mosquitto.conf
