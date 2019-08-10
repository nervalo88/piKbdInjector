
# piKbdInjector
An implementation of RpiZero USB gadget to issue keystrokes from RFID tags

It uses Rpi ZERO USB OTG gadget linux functionality to send keystrokes read from a RFID tag.
In othe words, it emulates an USB keyboards
Connect the pi to USB port - not Power -

Need to be started as root for :
- access SPI bus (maybe not mandatory)
- write kestrokes on usb target /dev/hidg0 : not required for linux but for windows targets
- acces GPIO to manage **WS2811 led**

How-to
- enable USB gadget on RPi zero : http://www.isticktoit.net/?p=1383
- Daemonify the python script : http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

```
sudo mkdir /usr/local/bin/kbdservice
sudo cp *.py /usr/local/bin/kbdservice
sudo cp kbdservice.sh /etc/init.d
sudo update-rc.d kbdservice.sh defaults
``` 
This is some kind of *old fashionned* `systemV` service, it is also possible to use now `systemd` [link](https://askubuntu.com/questions/911525/difference-between-systemctl-init-d-and-service)


- manage RGB WS2811 neoPixel : https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
```sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel```

## CREDITS
Thanks to the contributors whom made the how-to and the libraries above.
And https://github.com/mxgxw/MFRC522-python


