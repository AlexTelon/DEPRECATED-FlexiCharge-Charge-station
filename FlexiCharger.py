import asyncio
import websockets
import json
import time
import multiprocessing
import io
import PySimpleGUI as sg
import platform

from StateHandler import States
from StateHandler import StateHandler

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO

    from mfrc522 import SimpleMFRC522

from PIL import Image, ImageTk
from multiprocessing import Process
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call


def get_img_data(f, maxsize=(480, 800)):
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

state = StateHandler()
img_chargerID = get_img_data('Pictures/chargerid.png')
img_startingUp = get_img_data('Pictures/StartingUp.png')
img_notAvailable = get_img_data('Pictures/NotAvailable.png')
img_errorWhileCharging = get_img_data('Pictures/AnErrorOccuredWhileCharging.png')
img_authorizing = get_img_data('Pictures/authorizing.png')
img_charging = get_img_data('Pictures/charging.png')
img_chargingCancelled = get_img_data('Pictures/ChargingCancelled.png')
img_connectingToCar = get_img_data('Pictures/ConnectingToCar.png')
img_disconnectingFromCar = get_img_data('Pictures/DisconnectingFromCar.png')
img_followInstructions = get_img_data('Pictures/FollowInstructions.png')
img_fullyCharged = get_img_data('Pictures/FullyCharged.png')
img_plugInCable = get_img_data('Pictures/PlugInCable.png')
img_rfidNotValid = get_img_data('Pictures/RFIDnotValid.png')
img_unableToCharge = get_img_data('Pictures/UnableToCharge.png')


def statemachine(window):
    if state.get_state() == States.S_STARTUP:
        pass

    elif state.get_state() == States.AVAILABLE:
        window['IMAGE'].update(data=img_chargerID)
        window.refresh()

    #elif state.get_state() == States.NOTAVAILABLE:

    #elif state.get_state() == States.CONNECTING:

    #elif state.get_state() == States.CONNECTED:

    #elif state.get_state() == States.DISPLAYID:

    #elif state.get_state() == States.AUTHORIZING:

    #elif state.get_state() == States.PLUGINCABLE:

    else:
        window['IMAGE'].update(data=img_notAvailable)
        window.refresh()

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
    sg.theme('Black')

    layout1 =    [
                    [sg.Image(data=img_startingUp, key='__IMAGE__', size=(480, 800))]
                ]

    window = sg.Window(title="FlexiCharge", layout=layout1, no_titlebar=True, location=(0,0), size=(480,800), keep_on_top=False).Finalize()
    #window.Maximize()
    window.TKroot["cursor"] = "none"
    screen = 0

    while True:
        statemachine(window)
    window.close()

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
    
    