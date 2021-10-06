#import Images
import asyncio
from asyncio.events import get_event_loop
from asyncio.windows_events import NULL
import os
from asyncio.base_events import _run_until_complete_cb
import websockets
import json
import time
import multiprocessing
import io
import PySimpleGUI as sg
import platform
import qrcode
import nest_asyncio
import random

from StateHandler import States
from StateHandler import StateHandler

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO

    from mfrc522 import SimpleMFRC522

from PIL import Image, ImageTk
from multiprocessing import Process
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
loop = asyncio.get_event_loop()
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
img_Busy = get_img_data('Pictures/Busy.png')

chargerID = ['0','0','0','0','0','0']
url = "ws://54.220.194.65:1337/ssb"

#pLeaSe dOn't change any of the values in generateQR or x and y in GUI. It looks bad on the PC but works good on the Pi.
def generateQR():
    qr = qrcode.QRCode(
        version=8,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(chargerID)
    qr.make(fit=True)
    img_qrCodeGenerated = qr.make_image(fill_color="black", back_color="white")
    #img_qrCodeGenerated = qrcode.make(chargerID)
    type(img_qrCodeGenerated)
    img_qrCodeGenerated.save("Pictures/QrCode.png")

def GUI():
    global chargerID
    sg.theme('Black')
    
    backgroundLayout =  [
                            [sg.Image(data=img_startingUp, key='IMAGE', size=(480, 800))]
                        ]
    
    IdLayout =  [
                    [  
                        sg.Text(chargerID[0], font=('ITC Avant Garde Std', 36), key='ID0', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[1], font=('ITC Avant Garde Std', 36), key='ID1', justification='center', pad=(25,0), text_color='white'),
                        sg.Text(chargerID[2], font=('ITC Avant Garde Std', 36), key='ID2', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[3], font=('ITC Avant Garde Std', 36), key='ID3', justification='center', pad=(25,0), text_color='white'),
                        sg.Text(chargerID[4], font=('ITC Avant Garde Std', 36), key='ID4', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[5], font=('ITC Avant Garde Std', 36), key='ID5', justification='center', pad=(25,0), text_color='white')
                    ]
                ]

    qrCodeLayout =  [
                        [   
                            sg.Image(data=img_qrCode, key='QRCODE', size=(285,285)) 
                        ]
                    ]
    
    chargingPowerLayout =   [
                                [  
                                    sg.Text("61 kW at 7.3kWh", font=('ITC Avant Garde Std', 24), key='POWER', justification='center', text_color='white')
                                ]
                            ]
    
    chargingTimeLayout =   [
                                [  
                                    sg.Text("4 minutes until full", font=('ITC Avant Garde Std', 24), key='TIME', justification='center', text_color='white')
                                ]
                            ]

    chargingPercentLayout = [
                                [
                                    sg.Text("0", font=('ITC Avant Garde Std', 160), key='PERCENT', justification='center', text_color='red'),
                                    sg.Text("%", font=('ITC Avant Garde Std', 45), text_color='red')
                                ]
                            ]

    background_window = sg.Window(title="FlexiCharge", layout=backgroundLayout, no_titlebar=True, location=(0,0), size=(480,800), keep_on_top=False, margins=(0,0)).Finalize()
    if platform.system() != 'Windows':
        background_window.Maximize()
    background_window.TKroot["cursor"] = "none"

    id_window = sg.Window(title="FlexiChargeTopWindow", layout=IdLayout, location=(27,703), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    id_window.TKroot["cursor"] = "none"
    id_window.hide()

    qr_window = sg.Window(title="FlexiChargeQrWindow", layout=qrCodeLayout, location=(95, 165), grab_anywhere=False, no_titlebar=True, background_color='white', margins=(0,0)).finalize() #location=(95, 165) bildstorlek 285x285 från början
    qr_window.TKroot["cursor"] = "none"
    qr_window.hide()

    chargingPower_window = sg.Window(title="FlexiChargeChargingPowerWindow", layout=chargingPowerLayout, location=(166, 648), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingPower_window.TKroot["cursor"] = "none"
    chargingPower_window.hide()

    chargingTime_window = sg.Window(title="FlexiChargeChargingTimeWindow", layout=chargingTimeLayout, location=(166, 696), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingTime_window.TKroot["cursor"] = "none"
    chargingTime_window.hide()

    chargingPercent_window = sg.Window(title="FlexiChargeChargingPercentWindow", layout=chargingPercentLayout, location=(80, 250), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingPercent_window.TKroot["cursor"] = "none"
    chargingPercent_window.hide()

    return background_window, id_window, qr_window, chargingPower_window, chargingTime_window, chargingPercent_window

window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent = GUI()

def refreshWindows():
    global window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent
    window_back.refresh()
    window_id.refresh()
    window_qr.refresh()
    window_chargingPower.refresh()
    window_chargingTime.refresh()
    window_chargingPercent.refresh()

async def statemachine(websocket):
    global window_back, window_id, window_qr, state, lastState 

    while True:
        if state.get_state() == States.S_STARTUP:
            pass
        
        elif state.get_state() == States.S_NOTAVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_notAvailable)
                refreshWindows()
        
        elif state.get_state() == States.S_AVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_id['ID0'].update(chargerID[0])
                window_id['ID1'].update(chargerID[1])
                window_id['ID2'].update(chargerID[2])
                window_id['ID3'].update(chargerID[3])
                window_id['ID4'].update(chargerID[4])
                window_id['ID5'].update(chargerID[5])
                generateQR()
                window_back['IMAGE'].update(data=img_chargerID)
                window_id.UnHide()
                window_qr.UnHide()
                refreshWindows()
                
                res = await websocket.recv()
                res_pared = json.loads(res)
<<<<<<< Updated upstream
=======
                
                if res_pared[3] == "ReserveNow":
                    await reserveNow(websocket,res)
                time.sleep(random.randint(4,10))
                state.set_state(States.S_BUSY)
>>>>>>> Stashed changes
                
                if res_pared[3] == "ReserveNow":
                    await reserveNow(websocket,res)
                time.sleep(random.randint(4,10))
                state.set_state(States.S_BUSY)
                
        elif state.get_state() == States.S_BUSY:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_followInstructions)
                window_id.hide()
                window_qr.hide()
                refreshWindows()
                
                #this might need to change later but for now it is random
                time.sleep(random.randint(4,10))
                state.set_state(States.S_PLUGINCABLE)

        elif state.get_state() == States.S_PLUGINCABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_plugInCable)
                window_id.hide()
                window_qr.hide()
                refreshWindows()
                time.sleep(random.randint(6,15))
                state.set_state(States.S_CONNECTINGTOCAR)
        
        elif state.get_state() == States.S_CONNECTINGTOCAR:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_connectingToCar)
                refreshWindows()
                time.sleep(random.randint(10,15))
                state.set_state(States.S_CHARGING)

        elif state.get_state() == States.S_CHARGING:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_charging)
                window_chargingPower.un_hide()
                window_chargingTime.un_hide()
                window_chargingPercent.un_hide()
                refreshWindows()
                time.sleep(random.randint(5,15))
                state.set_state(States.S_FULLYCHARGED)

        elif state.get_state() == States.S_FULLYCHARGED:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_fullyCharged)
                window_chargingPower['POWER'].update("64 kW used")
                window_chargingTime.hide()
                window_chargingPercent.hide()
                refreshWindows()

        elif state.get_state() == States.S_CHARGINGCANCELLED:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_chargingCancelled)
                refreshWindows()

        elif state.get_state() == States.S_AUTHORIZING:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_authorizing)
                refreshWindows()

async def authorize(idTag, websocket):
    x = [2, "ssb", "Authorize", {"idTag": idTag}]
    y = json.dumps(x)
    await websocket.send(y)
    response = await websocket.recv()

async def send_heartbeat(websocket):
    while True:
        hb = [2, "ssb", "Heartbeat", {}]
        z = json.dumps(hb)
        print("Sending Heartbeat...")
        await websocket.send(z)
        print(await websocket.recv())
        await asyncio.sleep(2)

async def reserveNow(websocket, res):
    global state
    #check if already booked? 
    try:
        res_pared = json.loads(res)
        print(res_pared)

        pkg_accepted = [3, res_pared[1], "ReserveNow", {"status": "Accepted"}]
        pkg_accepted_send = json.dumps(pkg_accepted)
        await websocket.send(pkg_accepted_send)
        state.set_state(States.S_BUSY)
    except:
        pkg_rejected = [3, res_pared[1], "ReserveNow", {"status": "Rejected"}]
        pkg_rejected_send = json.dumps(pkg_rejected)
        await websocket.send(pkg_rejected_send)
        #state.set_state(States.S_AVAILABLE)

async def connect():
    global url
    global state
    global chargerID
    try:
        async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
            state.set_state(States.S_AVAILABLE)
            print("Connected.")
            pkg = [2, "0jdsEnnyo2kpCP8FLfHlNpbvQXosR5ZNlh8v", "BootNotification", {
            "chargePointVendor": "AVT-Company",
            "chargePointModel": "AVT-Express",
            "chargePointSerialNumber": "avt.001.13.1",
            "chargeBoxSerialNumber": "avt.001.13.1.01",
            "firmwareVersion": "0.9.87",
            "iccid": "",
            "imsi": "",
            "meterType": "AVT NQC-ACDC",
            "meterSerialNumber": "avt.001.13.1.01" } ]
            pkg_send = json.dumps(pkg)
            await websocket.send(pkg_send)
            resp = await websocket.recv()
            resp_parsed = json.loads(resp)
            print(resp_parsed[2]['chargerId'])
            temp = resp_parsed[2]['chargerId']
            chargerID = list(str(temp))
    except:
        state.set_state(States.S_NOTAVAILABLE)

def RFID():
    while True:
        reader = SimpleMFRC522()
        id, text = reader.read()
        print("Tag ID:", id)
        print("Tag text:", text)
        GPIO.cleanup()

async def main():
    global loop, state, chargerID
    try:
        async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
            state.set_state(States.S_AVAILABLE)
            print("Connected.")
            pkg = [2, "0jdsEnnyo2kpCP8FLfHlNpbvQXosR5ZNlh8v", "BootNotification", {
            "chargePointVendor": "AVT-Company",
            "chargePointModel": "AVT-Express",
            "chargePointSerialNumber": "avt.001.13.1",
            "chargeBoxSerialNumber": "avt.001.13.1.01",
            "firmwareVersion": "0.9.87",
            "iccid": "",
            "imsi": "",
            "meterType": "AVT NQC-ACDC",
            "meterSerialNumber": "avt.001.13.1.01" }]
            pkg_send = json.dumps(pkg)
            await websocket.send(pkg_send)
            resp = await websocket.recv()
            resp_parsed = json.loads(resp)
            print(resp_parsed[2]['chargerId'])
            temp = resp_parsed[2]['chargerId']
            chargerID = list(str(temp))
            tasks = [
                loop.create_task(statemachine(websocket)),
                #loop.create_task(send_heartbeat(websocket)),
            ]
            loop.run_until_complete(asyncio.wait(tasks))
    except:
        state.set_state(States.S_NOTAVAILABLE)

nest_asyncio.apply()
loop.run_until_complete(main())          