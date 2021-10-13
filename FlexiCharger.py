import asyncio
import websockets
import json
import time
import multiprocessing
import PySimpleGUI as sg
import platform
import nest_asyncio
import random
from OCPPfunctions import authorize, send_heartbeat, reserveNow, remoteStartTransaction, remoteStopTransaction, startTransaction, stopTransaction
from GUI import GUI, generateQR, get_img_data, refreshWindows
from StateHandler import States
from StateHandler import StateHandler

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522

state = StateHandler()
lastState = StateHandler()
sg.Window._move_all_windows = True
response = 0

img_chargerID = get_img_data('Pictures/ChargerIDNew.png')
img_startingUp = get_img_data('Pictures/StartingUp.png')
img_notAvailable = get_img_data('Pictures/NotAvailable.png')
img_errorWhileCharging = get_img_data('Pictures/AnErrorOccuredWhileCharging.png')
img_authorizing = get_img_data('Pictures/authorizing.png')
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
chargingPrice = 0
chargingCapacity = [4.4, 22.5, 27.2, 33.5, 40.0, 60.0, 64.0, 95.0, 95.0, 100.0]
chargingSpeed = [2.8, 3.2, 3.7, 4.6, 6.6, 7.2, 7.4, 11.0, 22.0, 50.0]
url = "ws://54.220.194.65:1337/ssb"

window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price = GUI(chargerID,img_startingUp,img_qrCode)

async def statemachine(websocket):
    global window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price, state, lastState, chargerID, chargingPrice
    while True:
        if state.get_state() == States.S_STARTUP:
            pass
        
        elif state.get_state() == States.S_NOTAVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_notAvailable)
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark)
        
        elif state.get_state() == States.S_AVAILABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_price.un_hide()
                window_id['ID0'].update(chargerID[0])
                window_id['ID1'].update(chargerID[1])
                window_id['ID2'].update(chargerID[2])
                window_id['ID3'].update(chargerID[3])
                window_id['ID4'].update(chargerID[4])
                window_id['ID5'].update(chargerID[5])
                window_price['PRICE'].update("Price: " + str(chargingPrice) + "kr / kWh")
                generateQR(chargerID)
                window_back['IMAGE'].update(data=img_chargerID)
                window_id.UnHide()
                window_qr.UnHide()
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                
                state.set_state(States.S_CHARGING)
                """res = await websocket.recv()
                res_pared = json.loads(res)
                #print(res_pared)
                if res_pared[2] == "ReserveNow":
                    await reserveNow(websocket,res,state)"""
                
        elif state.get_state() == States.S_BUSY:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_followInstructions)
                window_price.hide()
                window_id.hide()
                window_qr.hide()
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                
                #this might need to change later but for now it is random
                #resp = await websocket.recv()
                #resp_pared = json.loads(resp)
                if await remoteStartTransaction(websocket):
                    #await startTransaction(websocket)
                    state.set_state(States.S_PLUGINCABLE)

        elif state.get_state() == States.S_PLUGINCABLE:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_plugInCable)
                window_id.hide()
                window_qr.hide()
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                time.sleep(random.randint(2,5))
                state.set_state(States.S_CONNECTINGTOCAR)
        
        elif state.get_state() == States.S_CONNECTINGTOCAR:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_connectingToCar)
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                time.sleep(random.randint(2,5))
                state.set_state(States.S_CHARGING)

        elif state.get_state() == States.S_CHARGING:
            percent = 0
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_charging)
                
                window_price.hide() 
                window_id.hide()
                window_qr.hide()
                
                window_chargingPower.un_hide()
                window_chargingTime.un_hide()
                window_chargingPercent.un_hide()
                window_chargingPercentMark.un_hide()

                window_chargingPercent['PERCENT'].update(value='0')
                window_chargingPercent.move(140, 245)
                window_chargingPercentMark.move(276, 350) 

                randomSpeed = random.randint(0,9)
                chargedkWh = 0
                chargingTime = chargingCapacity[randomSpeed] / chargingSpeed[randomSpeed] * 60
                test = "kWh at " + str(chargingSpeed[randomSpeed]) + "kW"
                countTo9 = 0

                while True:
                    window_chargingPercent['PERCENT'].update(value=str(int(percent * 100)))
                    window_chargingPower['POWER'].update(value=(str(round(chargedkWh,1)) + test))

                    if percent < 0.20:
                        window_chargingPercentMark['PERCENTMARK'].update(text_color='red')
                        window_chargingPercent['PERCENT'].update(text_color='red')
                    elif percent >= 0.20 and percent < 0.3:
                        window_chargingPercentMark['PERCENTMARK'].update(text_color='yellow')
                        window_chargingPercent['PERCENT'].update(text_color='yellow')
                    elif percent >= 0.75:
                        window_chargingPercentMark['PERCENTMARK'].update(text_color='#78BD76')
                        window_chargingPercent['PERCENT'].update(text_color='#78BD76')
                    if percent >= 0.10:
                        window_chargingPercent.move(60, 245)
                        window_chargingPercentMark.move(330, 350)                     
                    if percent > 0.99:   
                        #await stopTransaction(websocket,response)
                        break

                    refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)

                    chargedkWh += chargingSpeed[randomSpeed] / 60
                    percent = round((chargedkWh / chargingCapacity[randomSpeed]), 2)

                    chargingTime -= 1
                    chargingTimeMinutes = int(chargingTime / 60)
                    
                    if chargingTimeMinutes < 1:
                        window_chargingTime['TIME'].update(value="< 1 minutes until full.")
                    else:
                        window_chargingTime['TIME'].update(value=str(chargingTimeMinutes) + " minutes until full.")

                    time.sleep(0.20)

                    if countTo9 == 9:
                        countTo9 = 0
                        #send metervalues
                    else:
                        countTo9 += 1
                state.set_state(States.S_FULLYCHARGED)

        elif state.get_state() == States.S_FULLYCHARGED:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_fullyCharged)
                window_chargingPower['POWER'].update(str(round(chargedkWh, 1)) + " kW used")
                window_chargingTime.hide()
                window_chargingPercent.hide()
                window_chargingPercentMark.hide()
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                time.sleep(4)
                window_chargingPower.hide()
                state.set_state(States.S_AVAILABLE)
                
        elif state.get_state() == States.S_CHARGINGCANCELLED:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_chargingCancelled)
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)

        elif state.get_state() == States.S_AUTHORIZING:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_authorizing)
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)  

def RFID():
    while True:
        reader = SimpleMFRC522()
        id, text = reader.read()
        print("Tag ID:", id)
        print("Tag text:", text)
        GPIO.cleanup()

async def main():
    global loop, state, chargerID, chargingPrice
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
            print(resp_parsed)

            dataTransfer = await websocket.recv()
            dataTransfer_parsed = json.loads(dataTransfer)
            print(dataTransfer_parsed)

            chargingInfo = json.loads(dataTransfer_parsed[3]['data'])
            print(chargingInfo)
            chargerID = list(str(chargingInfo["chargerId"]))
            chargingPrice = float(chargingInfo['chargingPrice']) / 100
            tasks = [
                asyncio.get_event_loop().create_task(statemachine(websocket)),
                #loop.create_task(send_heartbeat(websocket)),
            ]
            asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    except:
        state.set_state(States.S_NOTAVAILABLE)

nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())          