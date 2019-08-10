#!/usr/bin/env python
# -*- coding: utf8 -*-
# Version modifiee de la librairie https://github.com/mxgxw/MFRC522-python

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Fonction qui arrete la lecture proprement 
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()

def strTo16ByteArr (string):
	data = []
	for c in string:
		if (len(data)<16):
			data.append(int(ord(c)))
	while(len(data)!=16):
		data.append(0)
	return data

signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()

print "RFID password tag creator\n"


usrData = []
passData=[]
usrTxt = raw_input("Enter username :\n")
passTxt = raw_input("Enter password (max 16 chars) :\n")

usrData = strTo16ByteArr(usrTxt)
passData = strTo16ByteArr(passTxt)

print "will write : "
print "8 - " + str(usrData)
print "9 - " + str(passData)
print "\n"

# for c in usrTxt:
    # if (len(usrData)<16):
        # usrData.append(int(ord(c)))
# while(len(usrData)!=16):
    # usrData.append(0)


	
print ("Place tag")

while continue_reading:
      
    # Detecter les tags
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Une carte est detectee
    if status == MIFAREReader.MI_OK:
        print ("tag found")
    
    # Recuperation UID
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("tag UID : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
    
        # Clee d authentification par defaut
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        #key = [0x00,0x00,0x00,0x00,0x00,0x00]
      
        # Selection du tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authentification
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        if status == MIFAREReader.MI_OK:
			# print "Current : "
			# print "8 - " + str(MIFAREReader.MFRC522_Read(8))
			# print "9 - " + str(MIFAREReader.MFRC522_Read(9))

			print ("Writing ...")
			MIFAREReader.MFRC522_Write(8, usrData)
			MIFAREReader.MFRC522_Write(9, passData)
			
			usrWrited = MIFAREReader.MFRC522_Read(8)
			passWrited = MIFAREReader.MFRC522_Read(9)
			
			if usrWrited == usrData and passWrited== passData:
				print "write successful !"
			else:
				print "WRITE ERROR"
			
			# print "writed : "
			# print "8 - " + str(usrWrited) + "-" + str(usrData) 
			# print "9 - " + str(passWrited) + "-" + str(passData)

			# Stop
			MIFAREReader.MFRC522_StopCrypto1()
			continue_reading = False

        else:
            print ("Erreur d authentication")
