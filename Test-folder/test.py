import asyncio
import websockets
import json
import time
import nest_asyncio

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call


from StateHandler import States
from StateHandler import StateHandler
from UnixConverter import UnixConverter as uc

loop = asyncio.get_event_loop()

async def send_heartbeat(ws):
    while True:
        hb = [2, "123abc", "Heartbeat", {}]
        z = json.dumps(hb)
        print("Sending Heartbeat...")
        await ws.send(z)
        print(await ws.recv())
        await asyncio.sleep(2)


async def reserveNow(websocket):
        try:
            tempj = [0]
            tempj_send = json.dumps(tempj)
            await websocket.send(tempj_send)

            res = await websocket.recv()
            res_parsed = json.loads(res)
            print(res_parsed)
            
            pkg_accepted = [3,
                res_parsed[1],
                "ReserveNow",
                { 
                "status": "Accepted"
                                   } ]
            pkg_accepted_send = json.dumps(pkg_accepted)
            await websocket.send(pkg_accepted_send)
        
            return True, res_parsed[3]['expiryDate']
            
        except:
            pkg_rejected = [1, "Rejected"]
            pkg_rejected_send = json.dumps(pkg_rejected)
            await websocket.send(pkg_rejected_send)
            return False, 0
            
        
async def connect():
    url = "ws://54.220.194.65:1337/ssb"
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
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
        chargerID = resp_parsed[2]['chargerId']
        
        #l = list(str(chargerID))
        #print(l)
        print(resp_parsed)
        
        
        boolean, expiryDate = await reserveNow(websocket)
        
        if boolean:
            expiryDate = expiryDate / 1000 # Server sends in seconds, need milliseconds.
            expire = uc.convertUnixToLocal(expiryDate) # Convert time using UnixConverter.
            print(expire.strftime('%Y-%m-%d %H:%M:%S')) # Format time using strftime().
        else:
            print("sadge")
            
        return 0
        
        
        x = [2, "knaskalas", "Authorize", {"idTag": "B4A63CDF"}]
        y = json.dumps(x)
        await websocket.send(y)
        print("Response: " + await websocket.recv())

        # sched = BackgroundScheduler()
        # sched.add_job(lambda: send_heartbeat(websocket), 'interval', seconds=5)
        # sched.start()

        x = [2, "knaskalas", "StartTransaction", {
            "connectorId": 2,
            "idTag": "B4A63CDF",
            "timestamp": datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
            "meterStart": 1,
            "reservationId": 0
        }]
        y = json.dumps(x)
        print("Sending transaction request...")
        await websocket.send(y)
        resp = await websocket.recv()
        print("Response: " + resp)
        resp_parsed = json.loads(resp)
        # print(resp_parsed[2]['transactionId'])

        x = [2, "knaskalas", "StopTransaction", {
            "transactionId": resp_parsed[2]['transactionId'],
            "idTag": "B4A63CDF",
            "timestamp": datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
            "meterStop": 1
        }]
        y = json.dumps(x)
        print("Stopping transaction...")
        await websocket.send(y)
        print("Response: " + await websocket.recv())


async def statemachine():
    while True:

        if state.get_state() == States.S_STARTUP:
            print("Starting up...")

            # Only for temporary testing purposes:
            # await connect()

            state.set_state(States.S_AVAILABLE)
            # Pseudo-code:
            # if charger_connected:
            #    state.set_state(States.S_CONNECTED)
            # else
            #    state.set_state(States.S_NOTAVAILABLE)
            ####################

        elif state.get_state() == States.S_AVAILABLE:
            print("statemachine!!")

            await asyncio.sleep(4)

        elif state.get_state() == States.S_NOTAVAILABLE:
            pass

        elif state.get_state() == States.S_CONNECTING:
            pass

        elif state.get_state() == States.S_CONNECTED:
            pass

        elif state.get_state() == States.S_DISPLAYID:
            pass

        elif state.get_state() == States.S_AUTHORIZING:
            pass

        elif state.get_state() == States.S_PLUGINCABLE:
            pass

        else:
            print("wtf man.")


async def main():
    url = "ws://54.220.194.65:1337/ssb"
    global loop
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
        tasks = [
            loop.create_task(statemachine()),
            loop.create_task(send_heartbeat(websocket)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))

nest_asyncio.apply()

state = StateHandler()
loop.run_until_complete(connect())

# uwu daddy