import asyncio
import os
import websockets
import json
import time
import multiprocessing
import io
import PySimpleGUI as sg
import platform
import qrcode

from StateHandler import States
from StateHandler import StateHandler

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO

    from mfrc522 import SimpleMFRC522

from PIL import Image, ImageTk
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, Location, RegistrationStatus
from ocpp.v16 import call_result, call


def get_img_data(f, maxsize=(480, 800)):
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

state = StateHandler()
lastState = StateHandler()
sg.Window._move_all_windows = True

img_chargerID = get_img_data('Pictures/ChargerIDNew.png')
img_startingUp = get_img_data('Pictures/StartingUp.png')
img_notAvailable = get_img_data('Pictures/NotAvailable.png')
img_errorWhileCharging = get_img_data('Pictures/AnErrorOccuredWhileCharging.png')
img_authorizing = get_img_data('Pictures/Authorizing.png')
img_charging = get_img_data('Pictures/Charging.png')
img_chargingCancelled = get_img_data('Pictures/ChargingCancelled.png')
img_connectingToCar = get_img_data('Pictures/ConnectingToCar.png')
img_disconnectingFromCar = get_img_data('Pictures/DisconnectingFromCar.png')
img_followInstructions = get_img_data('Pictures/FollowInstructions.png')
img_fullyCharged = get_img_data('Pictures/FullyCharged.png')
img_plugInCable = get_img_data('Pictures/PlugInCable.png')
img_rfidNotValid = get_img_data('Pictures/RFIDnotValid.png')
img_unableToCharge = get_img_data('Pictures/UnableToCharge.png')
img_qrCode = get_img_data('Pictures/QrCode.png')
img_busy = get_img_data('Pictures/Busy.png')

chargerID = ['1','3','3','7','6','9']

img_qrCodeGenerated = qrcode.make(chargerID)
type(img_qrCodeGenerated)
img_qrCodeGenerated.save("Pictures/QrCode.png")

def GUI():
    sg.theme('Black')
    
    background_image =  [
                            [sg.Image(data=img_startingUp, key='IMAGE', size=(480, 800))]
                        ]

    background_window = sg.Window(title="FlexiCharge", layout=background_image, no_titlebar=True, location=(0,0), size=(480,800), keep_on_top=False, margins=(0,0)).Finalize()
    if platform.system() != 'Windows':
        background_window.Maximize()
    background_window.TKroot["cursor"] = "none"
    
    IdLayout =    [
                    [  
                        sg.Text(chargerID[0], font=('Tw Cen MT Condensed Extra Bold', 30), key='ID0', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[1], font=('Tw Cen MT Condensed Extra Bold', 30), key='ID1', justification='center', pad=(25,0), text_color='white'),
                        sg.Text(chargerID[2], font=('Tw Cen MT Condensed Extra Bold', 30), key='ID2', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[3], font=('Tw Cen MT Condensed Extra Bold', 30), key='ID3', justification='center', pad=(25,0), text_color='white'),
                        sg.Text(chargerID[4], font=('Tw Cen MT Condensed Extra Bold', 30), key='ID4', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[5], font=('Tw Cen MT Condensed Extra Bold', 30), key='ID5', justification='center', pad=(25,0), text_color='white')
                    ]
                ]

    qrCodeLayout =  [
                        [   
                            sg.Image(data=img_qrCode, key='QRCODE', size=(280,280)) 
                        ]
                    ]

    top_window = sg.Window(title="FlexiChargeTopWindow", layout=IdLayout, location=(27,703), keep_on_top=True, grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    top_window.TKroot["cursor"] = "none"
    top_window.hide()

    qr_window = sg.Window(title="FlexiChargeQrWindow", layout=qrCodeLayout, location=(95, 165), keep_on_top=True, grab_anywhere=False, no_titlebar=True, background_color='white', margins=(0,0)).finalize() #location=(115, 182) bildstorlek 250x250 från början
    qr_window.TKroot["cursor"] = "none"
    qr_window.hide()
    
    return background_window, top_window, qr_window

def refreshWindows(window_back, window_top, window_qr):
    window_back.refresh()
    window_top.refresh()
    window_qr.refresh()

def statemachine(v):
    window_back, window_top, window_qr = GUI()
    global state
    global lastState
     
    while True:
        print(state.get_state())
        print(v)

        if state.get_state() == States.S_STARTUP:
           asyncio.get_event_loop().run_until_complete(connect())
       
        elif state.get_state() == States.S_NOTAVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_notAvailable)
                refreshWindows(window_back,window_top, window_qr)
        
        elif state.get_state() == States.S_AVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_chargerID)
                window_top.UnHide()
                window_qr.UnHide()
                refreshWindows(window_back,window_top, window_qr)
                time.sleep(5)
                state.set_state(States.S_BUSY)

        elif state.get_state() == States.S_BUSY:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_busy)
                window_top.hide()
                window_qr.hide()
                refreshWindows(window_back,window_top, window_qr)

        #elif state.get_state() == States.S_CONNECTING:
       
        #elif state.get_state() == States.S_CONNECTED:
       
        #elif state.get_state() == States.S_DISPLAYID:
       
        #elif state.get_state() == States.S_AUTHORIZING:
       
        #elif state.get_state() == States.S_PLUGINCABLE:
       
        else:
            window_back['IMAGE'].update(data=img_notAvailable)
            window_back.refresh()

async def connect():
    url = "ws://localhost:9000/CP_Carl"
    global state
    try:
        async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
            state.set_state(States.S_AVAILABLE)
            #print("Connected.")
            x = [2, "CP_Carl", "Authorize", {"idTag": "B4A63CDF"}]
            y = json.dumps(x)
            await websocket.send(y)
            try:
                x = [2, "CP_Carl", "Heartbeat", {}]
                y = json.dumps(x)
                #print("Sending heartbeat.")
                await websocket.send(y)
                time.sleep(3)
                await websocket.recv()
            except websockets.ConnectionClosed:
                print("Disconnected.")
    except:
        state.set_state(States.S_AVAILABLE)


def RFID():
    while True:
        reader = SimpleMFRC522()
        id, text = reader.read()
        print("Tag ID:", id)
        print("Tag text:", text)
        GPIO.cleanup()

def RFIDtest(v):
    v.value = 1


if __name__ == '__main__':
    v = multiprocessing.Value('d', 0)
    rfid = multiprocessing.Process(target=RFIDtest, args=(v))
    state = multiprocessing.Process(target=statemachine, args=(v))

    #statemachine()
    #gui = Process(target=GUI)
    #gui.start()

    #OCPP = Process(target=asyncio.get_event_loop().run_until_complete(connect()))
    #OCPP.start()

    #if platform.system() != 'Windows':
    #    rfid = Process(target=RFID)
    #    rfid.start()

    #gui.join()
    #OCPP.join()

    #if platform.system() != 'Windows':
    #    rfid.join()
    
    