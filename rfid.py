#!/usr/bin/env as GPIO

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("To read tag press y, to write to tag press x")
val = input('Input action: ')

if val == "y":
    try:
            print("Place tag on reader")
            id, text = reader.read()
            print("Tag ID:", id)
            print("Tag text:", text)
    finally:
            GPIO.cleanup()
elif val == "x":
    try:
            text = input('new data: ')
            print("Now place your tag to write")
            reader.write(text)
            print("written")
    finally:
            GPIO.cleanup()
else:
    print("Wrong action given")
    GPIO.cleanup()