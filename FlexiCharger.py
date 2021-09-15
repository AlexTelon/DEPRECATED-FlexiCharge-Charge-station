import asyncio
import websockets
import json
import time
import multiprocessing
import tkinter as tk
import platform

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO

    from mfrc522 import SimpleMFRC522

from PIL import Image, ImageTk
from multiprocessing import Process
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call


async def connect():
    url = "ws://localhost:9000/CP_Carl"
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
        print("Connected.")
        x = [2, "CP_Carl", "Authorize", {"idTag": "B4A63CDF"}]
        y = json.dumps(x)
        await websocket.send(y)

        while True:
            try:
                x = [2, "CP_Carl", "Heartbeat", {}]
                y = json.dumps(x)
                print("Sending heartbeat.")
                await websocket.send(y)
                time.sleep(3)
                await websocket.recv()
            except websockets.ConnectionClosed:
                print("Disconnected.")

def GUI():
    root = tk.Tk()

    canvas = tk.Canvas(root, width=480, height=800, bg='black')
    canvas.grid(columnspan=3)

    #Logo
    logo = Image.open("Pictures/white.png")
    logo = ImageTk.PhotoImage(logo)
    img_1 = tk.Label(image=logo, bg='black')
    img_1.image = logo
    img_1.place(x=90, y=40)

    #Cross
    cross = Image.open("Pictures/cross.png")
    cross = ImageTk.PhotoImage(cross)
    img_2 = tk.Label(image=cross, bg='black')
    img_2.image = cross
    img_2.place(x=118, y=202)

    #instuctions
    instuctions = tk.Label(root, text="Charger not available", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
    instuctions.place(x=118, y=563)

    instuctions = tk.Label(root, text="This charger is out of order\n and is not able to charge at the moment.", font="ITCAvantGardeStd", bg='black', fg='#E5E5E5')
    instuctions.place(x=108, y=701)
    if platform.system() != 'Windows':
        root. attributes('-fullscreen',True)
    root.config(cursor="none")
    root.mainloop()

def RFID():
    while True:
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

if __name__ == '__main__':
    gui = Process(target=GUI)
    gui.start()

    OCPP = Process(target=asyncio.get_event_loop().run_until_complete(connect()))
    OCPP.start()

    if platform.system() != 'Windows':
        rfid = Process(target=RFID)
        rfid.start()

    gui.join()
    OCPP.join()

    if platform.system() != 'Windows':
        rfid.join()
    
    