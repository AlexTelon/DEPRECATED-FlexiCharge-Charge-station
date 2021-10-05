import asyncio
import os
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

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from asyncio.events import get_event_loop
import os
import multiprocessing
import io
import PySimpleGUI as sg
import platform
import qrcode
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, Location, RegistrationStatus
from ocpp.v16 import call_result, call
from PIL import Image, ImageTk
from multiprocessing import Process


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

img_chargerID = get_img_data('Pictures/Chargerid.png')
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

loop = asyncio.get_event_loop()

async def send_heartbeat(ws):
    while True:
        hb = [2, "123abc", "Heartbeat", {}]
        z = json.dumps(hb)
        print("Sending Heartbeat...")
        await ws.send(z)
        print(await ws.recv())
        await asyncio.sleep(2)

async def generateQR():
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


async def refreshWindows(window_back, window_top, window_qr):
    window_back.refresh()
    window_top.refresh()
    window_qr.refresh()


async def connect(websocket):
    global chargerID
    #async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
    

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
    chargerID = resp_parsed[2]['chargerId']
    l = list(str(chargerID))
    print(l)
        #print(chargerID)
    print("Connected.")
    #x = [2, "knaskalas", "Authorize", {"idTag": "B4A63CDF"}]
    #y = json.dumps(x)
    #await websocket.send(y)
    #print("Response: " + await websocket.recv())

        # sched = BackgroundScheduler()
        # sched.add_job(lambda: send_heartbeat(websocket), 'interval', seconds=5)
        # sched.start()

    
    #x = [2, "knaskalas", "StartTransaction", {
     #       "connectorId": 2,
     #       "idTag": "B4A63CDF",
     #       "timestamp": datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
     #       "meterStart": 1,
     #       "reservationId": 0
     #   }]
    #y = json.dumps(x)
    #print("Sending transaction request...")
    #await websocket.send(y)
    #resp = await websocket.recv()
   # print("Response: " + resp)
    #resp_parsed = json.loads(resp)
        # print(resp_parsed[2]['transactionId'])

    #x = [2, "knaskalas", "StopTransaction", {
    #        "transactionId": resp_parsed[2]['transactionId'],
    #        "idTag": "B4A63CDF",
    #        "timestamp": datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
    #        "meterStop": 1
    #    }]
    #y = json.dumps(x)
    #print("Stopping transaction...")
    #await websocket.send(y)
    #print("Response: " + await websocket.recv())

        #while True:
        #    hb = [2, "knaskalas", "Heartbeat", {}]
        #    z = json.dumps(hb)
        #    print("Sending Heartbeat...")
        #    await websocket.send(z)
        #    print("Response: " + await websocket.recv())
        #    time.sleep(3)

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

        pkg_accepted = [3,
            res_pared[1],
            "ReserveNow",
            { 
            "status": "Accepted"
                               } ]
        pkg_accepted_send = json.dumps(pkg_accepted)
        await websocket.send(pkg_accepted_send)
        state.set_state(States.S_BUSY)
    except:
        pkg_rejected = [1, "Rejected"]
        pkg_rejected_send = json.dumps(pkg_rejected)
        await websocket.send(pkg_rejected_send)
        state.set_state(States.S_AVAILABLE)

async def statemachine(websocket):

    window_back, window_top, window_qr = GUI()
    global state
    global lastState
    global chargerID
    while True:
        print(state.get_state())

        if state.get_state() == States.S_STARTUP:

            print("Starting up...")
            asyncio.get_event_loop().run_until_complete(connect(websocket))
            # Only for temporary testing purposes:
            await connect(websocket)
            print ("Connect")

            state.set_state(States.S_AVAILABLE)
            # Pseudo-code:
            # if charger_connected:
            #    state.set_state(States.S_CONNECTED)
            # else
            #    state.set_state(States.S_NOTAVAILABLE)
            ####################

        elif state.get_state() == States.S_AVAILABLE:
            print("statemachine!!")
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
                refreshWindows(window_back,window_top, window_qr)
                #time.sleep(5)
            asyncio.get_event_loop().run_until_complete(reserveNow(websocket))

            await asyncio.sleep(4)

        elif state.get_state() == States.S_NOTAVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_notAvailable)
                refreshWindows(window_back,window_top, window_qr)

        elif state.get_state() == States.S_BUSY:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_Busy)
                window_top.hide()
                window_qr.hide()
                refreshWindows(window_back,window_top, window_qr)

                #time.sleep(7)
                state.set_state(States.S_AVAILABLE)

                window_back['IMAGE'].update(data=img_notAvailable)
                window_back.refresh()

        elif state.get_state() == States.S_CONNECTED:
            pass
            

        elif state.get_state() == States.S_DISPLAYID:
            pass

        elif state.get_state() == States.S_AUTHORIZING:
            pass

        elif state.get_state() == States.S_PLUGINCABLE:
            pass

async def main():
    global url
    global loop
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
        tasks = [
            loop.create_task(statemachine(websocket)),
            #loop.create_task(send_heartbeat(websocket)),
            

        ]
        loop.run_until_complete(asyncio.wait(tasks))        