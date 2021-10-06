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


#please don't change any of the values in generateQR or x and y in GUI. It looks bad on the PC but works good on the Pi.
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


def chargingsTatus():
    
    x = 0
    while x < 11:
        print("adding")
        
        x = x+1
        charginglayout =    [
                        [
                               sg.Text(x, font=('Tw Cen MT Condensed Extra Bold', 50), key='ID0', justification='center', pad=(20,0))
                        ]
                    ]
        

        charging_window = sg.Window(title="FlexiChargeTopWindow", layout=charginglayout, location=(220,300),keep_on_top=True, grab_anywhere=False, transparent_color=sg.theme_background_color(), no_titlebar=True).finalize()
        charging_window.TKroot["cursor"] = "none"
        time.sleep(1)
        charging_window.hide()
        refreshWindows()
        




def GUI():
    global chargerID
    global x
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
                            sg.Image(data=img_qrCode, key='QRCODE', size=(285,285)) 
                        ]
                    ]
    
                 
        

    top_window = sg.Window(title="FlexiChargeTopWindow", layout=IdLayout, location=(27,703), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    top_window.TKroot["cursor"] = "none"
    top_window.hide()

    qr_window = sg.Window(title="FlexiChargeQrWindow", layout=qrCodeLayout, location=(95, 165), grab_anywhere=False, no_titlebar=True, background_color='white', margins=(0,0)).finalize() #location=(95, 165) bildstorlek 285x285 från början
    qr_window.TKroot["cursor"] = "none"
    qr_window.hide()

    return background_window, top_window, qr_window

window_back, window_top, window_qr = GUI()

def refreshWindows():
    global window_back, window_top, window_qr, window_charging
    window_back.refresh()
    window_top.refresh()
    window_qr.refresh()

async def statemachine(websocket):
    global window_back, window_top, window_qr, state, lastState

    while True:
        if state.get_state() == States.S_STARTUP:
            #asyncio.get_event_loop().run_until_complete(connect())
            pass
        elif state.get_state() == States.S_NOTAVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_notAvailable)
                refreshWindows()
        
        elif state.get_state() == States.S_AVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_top['ID0'].update(chargerID[0])
                window_top['ID1'].update(chargerID[1])
                window_top['ID2'].update(chargerID[2])
                window_top['ID3'].update(chargerID[3])
                window_top['ID4'].update(chargerID[4])
                window_top['ID5'].update(chargerID[5])
                generateQR()
                window_back['IMAGE'].update(data=img_chargerID)
                window_top.UnHide()
                window_qr.UnHide()
                refreshWindows()
                time.sleep(5)
                asyncio.get_event_loop().run_until_complete(reserveNow(websocket))

        elif state.get_state() == States.S_BUSY:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_charging)
                
                window_top.hide()
                window_qr.hide()
                chargingsTatus()
                refreshWindows()

                #time.sleep(7)
                #state.set_state(States.S_AVAILABLE)

        #elif state.get_state() == States.S_CONNECTING:
       
        #elif state.get_state() == States.S_CONNECTED:
       
        #elif state.get_state() == States.S_DISPLAYID:
       
        #elif state.get_state() == States.S_AUTHORIZING:
       
        #elif state.get_state() == States.S_PLUGINCABLE:
       
        else:
            window_back['IMAGE'].update(data=img_notAvailable)
            window_back.refresh()

async def authorize(idTag):
    x = [2, "ssb", "Authorize", {"idTag": "B4A63CDF"}]
    y = json.dumps(x)
    await websocket.send(y)
    response = await websocket.recv()

async def send_heartbeat():
    while True:
        hb = [2, "ssb", "Heartbeat", {}]
        z = json.dumps(hb)
        print("Sending Heartbeat...")
        await websocket.send(z)
        print(await websocket.recv())
        await asyncio.sleep(2)

async def reserveNow(websocket):
    global state
    try:
        #Remove for using the app
        tempj = [0]
        tempj_send = json.dumps(tempj)
        await websocket.send(tempj_send)
        #end of remove

        res = await websocket.recv()
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
    
"""
    def chargingsTatus():
    #window = GUI()
    x=0
    while x < 10:
        x = x+1
        layout =    [
                        [
                            sg.Text(x, font=('Tw Cen MT Condensed Extra Bold', 30), key='ID0', justification='center', pad=(20,0))
                        ]
                    ]

        top_window = sg.Window(title="FlexiChargeTopWindow", layout=layout, location=(25,710),keep_on_top=True, grab_anywhere=False, transparent_color=sg.theme_background_color(), no_titlebar=True).finalize()
        top_window.TKroot["cursor"] = "none"
        time.sleep(1)
"""