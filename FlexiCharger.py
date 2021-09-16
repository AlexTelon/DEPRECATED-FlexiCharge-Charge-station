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

root = tk.Tk()
root.geometry('480x800')
root.overrideredirect(True)
root.overrideredirect(False)

startingup_frame = tk.Frame(root, width=480, height=800, bg='black')
notavailable_frame = tk.Frame(root, width=480, height=800, bg='black')
available_frame = tk.Frame(root, width=480, height=800, bg='black')
authorizing_frame = tk.Frame(root, width=480, height=800, bg='black')

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
    listID =  [1, 4, 3, 7, 5, 9]

    if platform.system() != 'Windows':
        root.attributes('-fullscreen', True)   
        root.config(cursor="none")             

    # Starting up screen ######################

    #Logo
    img_logoGreen = Image.open("Pictures/color-2.png")
    img_logoGreen = ImageTk.PhotoImage(img_logoGreen)
    logo_startingup = tk.Label(startingup_frame, image=img_logoGreen, bg='black')
    logo_startingup.image = img_logoGreen
    logo_startingup.place(x=137, y=202)

    #Flexi charge text
    img_flexiCharge = Image.open("Pictures/flexichargetext1.png")
    img_flexiCharge = ImageTk.PhotoImage(img_flexiCharge)
    logo_flexiCharge1 = tk.Label(startingup_frame, image=img_flexiCharge, bg='black')
    logo_flexiCharge1.image = img_logoGreen
    logo_flexiCharge1.place(x=88, y=479)

    #Starting up text
    startingup_text = tk.Label(startingup_frame, text="Starting up...", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
    startingup_text.place(x=153, y=621)

    #Button
    btn_change_to_notavailable = tk.Button(startingup_frame, text='Change to notavailable', command=change_to_not_available)
    btn_change_to_notavailable.pack(side='bottom')

    ##########################################

    #   Avalable screen ######################

    #Logo
    chargeid = Image.open("Pictures/chargerid.png")
    chargeid = ImageTk.PhotoImage(chargeid)
    img_1 = tk.Label(available_frame, image=chargeid, bg='black')
    img_1.image = chargeid
    img_1.place(x=9, y=4)

    #chargerID_display
    chargerID1 = Image.open("Pictures/chargerid2.png")
    resized = chargerID1.resize((40,64), Image.ANTIALIAS)
    new_resized = ImageTk.PhotoImage(resized)
    img_1 = tk.Label(available_frame, image=new_resized, bg='black')
    img_1.image = new_resized
    img_1.place(x=57, y=708)

    #chargerID_display
    img_2 = tk.Label(available_frame, image=new_resized, bg='black')
    img_2.image = new_resized
    img_2.place(x=126, y=708)

    #chargerID_display
    img_3 = tk.Label(available_frame, image=new_resized, bg='black')
    img_3.image = new_resized
    img_3.place(x=195, y=708)

    #chargerID_display
    img_4 = tk.Label(available_frame, image=new_resized, bg='black')
    img_4.image = new_resized
    img_4.place(x=264, y=708)

    #chargerID_display
    img_5 = tk.Label(available_frame, image=new_resized, bg='black')
    img_5.image = new_resized
    img_5.place(x=333, y=708)


    #chargerID_display
    img_6 = tk.Label(available_frame, image=new_resized, bg='black')
    img_6.image = new_resized
    img_6.place(x=402, y=708)


    #ChargerID
    ChargerID = tk.Label(available_frame, text=listID [0], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
    ChargerID.place(x=65, y=714)

    ChargerID = tk.Label(available_frame, text=listID [1], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
    ChargerID.place(x=134, y=714)

    ChargerID = tk.Label(available_frame, text=listID [2], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
    ChargerID.place(x=203, y=714)

    ChargerID = tk.Label(available_frame, text=listID [3], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
    ChargerID.place(x=272, y=714)

    ChargerID = tk.Label(available_frame, text=listID [4], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
    ChargerID.place(x=341, y=714)

    ChargerID = tk.Label(available_frame, text=listID [5], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
    ChargerID.place(x=410, y=714)

    #Button
    btn_change_to_authorizing = tk.Button(available_frame, text='Change to authorizing', command=change_to_authorizing)
    btn_change_to_authorizing.pack(side='bottom')

    ##########################################

    # Not availeble screen ####################

    #Logo
    logo = Image.open("Pictures/white.png")
    logo = ImageTk.PhotoImage(logo)
    img_1 = tk.Label(notavailable_frame, image=logo, bg='black')
    img_1.image = logo
    img_1.place(x=90, y=40)

    #Cross
    cross = Image.open("Pictures/cross.png")
    cross = ImageTk.PhotoImage(cross)
    img_2 = tk.Label(notavailable_frame, image=cross, bg='black')
    img_2.image = cross
    img_2.place(x=118, y=202)

    #instuctions
    instuctions = tk.Label(notavailable_frame, text="Charger not available", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
    instuctions.place(x=118, y=563)

    instuctions = tk.Label(notavailable_frame, text="This charger is out of order\n and is not able to charge at the moment.", font="ITCAvantGardeStd", bg='black', fg='#E5E5E5')
    instuctions.place(x=108, y=701)

    #Button
    btn_change_to_notavailable = tk.Button(notavailable_frame, text='Change to available', command=change_to_available)
    btn_change_to_notavailable.pack(side='bottom')

    ############################################

    # Authorizing Screen ####################

    #Logo
    logo = Image.open("Pictures/white.png")
    logo = ImageTk.PhotoImage(logo)
    img_1 = tk.Label(authorizing_frame, image=logo, bg='black')
    img_1.image = logo
    img_1.place(x=90, y=40)

    #Dongle
    dongle = Image.open("Pictures/Group 3-14.png")
    dongle = ImageTk.PhotoImage(dongle)
    img_2 = tk.Label(authorizing_frame, image=dongle, bg='black')
    img_2.image = cross
    img_2.place(x=118, y=202)

    #Authorizing text
    authorizing_text = tk.Label(authorizing_frame, text="Authorizing...", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
    authorizing_text.place(x=158, y=563)

    ############################################


    startingup_frame.pack(expand=True, fill='both')
    root.mainloop()

def change_to_not_available():
    startingup_frame.pack_forget()
    notavailable_frame.pack(expand=True, fill='both')
    
def change_to_available():
    notavailable_frame.pack_forget()
    available_frame.pack(expand=True, fill='both')

def change_to_authorizing():
    available_frame.pack_forget()
    authorizing_frame.pack(expand=True, fill='both')

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
    
    