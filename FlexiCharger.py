import asyncio
from datetime import datetime
import websockets
import json
import time
import PySimpleGUI as sg
import platform
import nest_asyncio
import random
import multiprocessing
from OCPPfunctions import HandleReceive, handleExpire, statusNotification, authorize, dataTransfer, send_heartbeat, reserveNow, remoteStartTransaction, remoteStopTransaction, startTransaction, stopTransaction
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
uniqueID = 0
dataUniqueID = 0
test = 0

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
img_unableToCharge = get_img_data('Pictures/UnableToCharge.png')
img_qrCode = get_img_data('Pictures/QrCode.png')
img_Busy = get_img_data('Pictures/Busy.png')

chargerID = ['0','0','0','0','0','0']
chargingPrice = 0
chargingCapacity = [4.4, 22.5, 27.2, 33.5, 40.0, 60.0, 64.0, 95.0, 95.0, 100.0]
chargingSpeed = [2.8, 3.2, 3.7, 4.6, 6.6, 7.2, 7.4, 11.0, 22.0, 50.0]
url = "ws://54.220.194.65:1337/ssb"
loop = asyncio.get_event_loop()

window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price = GUI(chargerID,img_startingUp,img_qrCode)

async def statemachine(websocket):
    global window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price, state, lastState, chargerID, chargingPrice, uniqueID, response, dataUniqueID
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
                
                res = await websocket.recv()
                res_pared = json.loads(res)
                #print(res_pared)
                if res_pared[2] == "ReserveNow":
                    response = await reserveNow(websocket,res,state)
                
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
                expiryDate = response[3]['expiryDate']

                event = asyncio.Event()
                event2 = asyncio.Event()
                temp = 0
                count = 0
                coro = 0

                while True:
                    if event.is_set():
                        global test
                        response = await startTransaction(websocket, response, uniqueID)
                        print(response)
                        dataUniqueID = response[1]
                        state.set_state(States.S_PLUGINCABLE)
                        break
                   
                    elif event2.is_set():
                        state.set_state(States.S_AVAILABLE)
                        break

                    if count == 5:
                        temp = 1
                        count = 0
                    else:
                        count += 1
                        temp = 0
                    
                    coro = asyncio.run_coroutine_threadsafe(handleExpire(websocket, event, event2, temp, expiryDate, uniqueID), loop)
                    await asyncio.sleep(0.1)
                    coro.cancel()

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
            percent = 0.01
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_charging)

                window_chargingPower.un_hide()
                window_chargingTime.un_hide()
                window_chargingPercent.un_hide()
                window_chargingPercentMark.un_hide()

                window_chargingPercent['PERCENT'].update(value='1')
                window_chargingPercent.move(140, 245)
                window_chargingPercentMark.move(276, 350)

                randomSpeed = random.randint(0,9)
                chargedkWh = 1
                #chargingTime = chargingCapacity[randomSpeed] / chargingSpeed[randomSpeed] * 60
                chargingTime = 100
                #test = "kWh at " + str(chargingSpeed[randomSpeed]) + "kW"
                test = "kWh at " + str(1) + "kW"
                countTo9 = 0
                countTo3 = 0
                latestCharge = 1

                event = asyncio.Event()
                coro = 0
                temp = 0

                while True:
                    #print(event.is_set())
                    #window_chargingPercent['PERCENT'].update(value=str(int(percent * 100)))
                    #window_chargingPower['POWER'].update(value=(str(round(chargedkWh, 1)) + test))
                    window_chargingPercent['PERCENT'].update(value=int(percent * 100))
                    window_chargingPower['POWER'].update(value=(str(round(chargedkWh,1)) + test))
                    if event.is_set():
                        await asyncio.sleep(0.3)
                        if coro.cancel():
                            state.set_state(States.S_CHARGINGCANCELLED)
                            await stopTransaction(websocket, response, uniqueID)
                            break
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
                        state.set_state(States.S_FULLYCHARGED)
                        break

                    refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)

                    #chargedkWh += chargingSpeed[randomSpeed] / 60
                    #percent = round((chargedkWh / chargingCapacity[randomSpeed]), 2)
                    if countTo3 == 3:
                        countTo3 = 0
                        chargedkWh += 1
                        chargingTime -= 1
                    else:
                        countTo3 += 1

                    percent = chargedkWh / 100

                    #chargingTime -= 1
                    chargingTimeMinutes = int(chargingTime / 60)

                    if chargingTimeMinutes < 1:
                        window_chargingTime['TIME'].update(value="< 1 minutes until full.")
                    else:
                        window_chargingTime['TIME'].update(value=str(chargingTimeMinutes) + " minutes until full.")

                    if countTo9 == 9:
                        temp = 1
                        countTo9 = 0
                    else:
                        if countTo9 == 0:
                            latestCharge = int(percent * 100)
                        temp = 0
                        countTo9 += 1
                    
                    coro = asyncio.run_coroutine_threadsafe(HandleReceive(websocket, event, dataUniqueID, latestCharge, int(percent * 100), temp, response[3]['transactionId']), loop)
                    await asyncio.sleep(0.3)
                    coro.cancel()
                        

        elif state.get_state() == States.S_FULLYCHARGED:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_fullyCharged)
                window_chargingPower['POWER'].update(str(round(chargedkWh, 1)) + " kWh used")
                window_chargingTime.hide()
                window_chargingPercent.hide()
                window_chargingPercentMark.hide()
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                time.sleep(4)
                window_chargingPower.hide()
                state.set_state(States.S_AVAILABLE)
                await statusNotification(websocket, uniqueID)
                
        elif state.get_state() == States.S_CHARGINGCANCELLED:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_chargingTime['TIME'].update(value="Charging stopped.")
                window_chargingPower['POWER'].update(value=str(round(chargedkWh,1)) +"kWh charged.")
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)
                time.sleep(4)
                window_chargingPower.hide()
                window_chargingTime.hide()
                window_chargingPercent.hide()
                window_chargingPercentMark.hide()
                state.set_state(States.S_AVAILABLE)
                await statusNotification(websocket, uniqueID)

        elif state.get_state() == States.S_AUTHORIZING:
            if lastState.get_state() != state.get_state():
                lastState.set_state(state.get_state())
                window_back['IMAGE'].update(data=img_authorizing)
                refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price)  

async def main():
    global loop, state, chargerID, chargingPrice, uniqueID
    try:
        async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
            state.set_state(States.S_AVAILABLE)
            print("Connected.")
            x = ['ssb', 'FreeCharger']
            y = json.dumps(x)
            await websocket.send(y)
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

            uniqueID = resp_parsed[1]

            dataTransfer = await websocket.recv()
            dataTransfer_parsed = json.loads(dataTransfer)
            dataUniqueID = dataTransfer_parsed[1]
            print(dataTransfer_parsed)

            chargingInfo = json.loads(dataTransfer_parsed[3]['data'])
            print(chargingInfo)
            chargerID = list(str(chargingInfo["chargerId"]))
            chargingPrice = float(chargingInfo['chargingPrice']) / 100
            tasks = [
                loop.create_task(statemachine(websocket)),
                #loop.create_task(send_heartbeat(websocket)),
            ]
            loop.run_until_complete(asyncio.wait(tasks))
    except:
        state.set_state(States.S_NOTAVAILABLE)

nest_asyncio.apply()
loop.run_until_complete(main())          