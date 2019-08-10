#!/usr/bin/env python3
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time

import board
import neopixel

import logging
from logging.handlers import RotatingFileHandler

from kbd_map import kbmapAZERTY as kbmap



def write_report(report):
	try:
		with open('/dev/hidg0', 'rb+') as fd:
			fd.write(report)
	except:
		logger.error("unable to write on /dev/hidg0")

def sendStr(str) :
    for c in str : sendChr(c)
	
def sendChr(char) :
    if not char in kbmap.keys() :
        logger.warning("Unknown char: "+ str(char)) ; return
    # key down
    # print(kbmap[char])
    buf[2], buf[0] = kbmap[char]
    write_report(buf)
    # key up
    buf[2], buf[0] = 0x00, 0x00
    write_report(buf)


def sendReturn() :
    buf[2], buf[0] = 0x28, 0x00
    write_report(buf)
    # key up
    buf[2], buf[0] = 0x00, 0x00
    write_report(buf)
	
def sendTab() :
    buf[2], buf[0] = 0x2b, 0x00
    write_report(buf)
    # key up
    buf[2], buf[0] = 0x00, 0x00
    write_report(buf)

def end_read(signal,frame):
    global continue_reading
    logger.warning("clean exit, good job !") #not supposed to occur
    continue_reading = False
    GPIO.cleanup()
	
def dataToStr (data):
	if(len(data)==16):
		outStr = ""
		c=0
		while (c<16):
			if(data[c]!=0) :
				try :
					outStr += str(chr(data[c]))
				except :
					logger.error("Unable to cast into char ")
					pixels[0]=(0,255,0)
					time.sleep(5)
					outStr = ""
					return outStr
			c+=1
		return outStr
	else:
		logger.error("not enough data")
		pixels[0]=(0,255,0)
		time.sleep(5)
		outStr = ""
		return outStr


pixels = neopixel.NeoPixel(board.D18, 1,brightness=0.1)
pixels[0]= (0,0,0)

buf = bytearray(8)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

file_handler = RotatingFileHandler("kbdInject.log",'a',1000000,1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
# stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.info("Keyboard keystrokes injector script started")

continue_reading = True

MIFAREReader = MFRC522.MFRC522()

while continue_reading:
	pixels[0] = (0,0,255)
	# Detecter les tags
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	# Une carte est detectee
	if status == MIFAREReader.MI_OK:
		# logger.info("Tag detected")
		pixels[0] = (255,255,0)
	# Recuperation UID
	(status,uid) = MIFAREReader.MFRC522_Anticoll()
	if status == MIFAREReader.MI_OK:
		logger.info("Tag UID : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
		# Clee d authentification par defaut
		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		#key = [0x00,0x00,0x00,0x00,0x00,0x00]
		# Selection du tag
		MIFAREReader.MFRC522_SelectTag(uid)
		# Authentification
		
		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
		if status == MIFAREReader.MI_OK:
			usrData = MIFAREReader.MFRC522_Read(8)
			passData = MIFAREReader.MFRC522_Read(9)
			
			# logger.info("Will send keystrokes: "+ dataToStr(usrData) + "\t"+ dataToStr(passData))
			
			sendStr( dataToStr(usrData))
			sendTab()
			sendStr( dataToStr(passData))
			sendReturn()

			MIFAREReader.MFRC522_StopCrypto1()
			pixels[0]=(255,0,0)
			time.sleep(5)
		else:
				logger.error("TAG read error : MIFAREReader.MI_OK is False ")
				pixels[0]=(0,255,0)
				time.sleep(5)
