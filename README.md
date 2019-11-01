# Sensor-arduino-and-a-telegram-bot
DS18B20:
https://blog.ja-ke.tech/2019/01/21/DS18B20-armbian.html
/boot/armbianEnv.txt:
overlays=w1-gpio
param_w1_pin=PA2
param_w1_pin_int_pullup=0
pip install w1thermsensor

Telegram bot:
apt install libffi-dev
$ pip install python-telegram-bot --upgrade
