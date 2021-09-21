import asyncio
import websockets
import json
import time


from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call


from StateHandler import States
from StateHandler import StateHandler


        
def send_heartbeat(ws):
        hb = [2, "knaskalas", "Heartbeat", {}]
        z = json.dumps(hb)
        print("Sending Heartbeat...")
        ws.send(z)
        

async def connect():
    url = "ws://localhost:9000/knaskalas"
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
        print("Connected.")
        x = [2, "knaskalas", "Authorize", {"idTag": "B4A63CDF"}]
        y = json.dumps(x)
        await websocket.send(y)
        print("Response: " + await websocket.recv())
        
        #sched = BackgroundScheduler()
        #sched.add_job(lambda: send_heartbeat(websocket), 'interval', seconds=5)
        #sched.start()
        
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
        #print(resp_parsed[2]['transactionId'])
        
        
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
        
        
        while True:
            hb = [2, "knaskalas", "Heartbeat", {}]
            z = json.dumps(hb)
            print("Sending Heartbeat...")
            await websocket.send(z)
            print("Response: " + await websocket.recv())
            time.sleep(3)

          
def statemachine():
    if state.get_state() == States.S_STARTUP:
        print("Starting up...")
        
        ### Pseudo-code: ###
        # if charger_connected:
        #    state.set_state(States.S_CONNECTED)
        # else
        #    state.set_state(States.S_NOTAVAILABLE)
        ### ###    
    elif state.get_state() == States.AVAILABLE:
    
    elif state.get_state() == States.NOTAVAILABLE:
    
    elif state.get_state() == States.CONNECTING:
    
    elif state.get_state() == States.CONNECTED:
    
    elif state.get_state() == States.DISPLAYID:
    
    elif state.get_state() == States.AUTHORIZING:
    
    elif state.get_state() == States.PLUGINCABLE:
    
    else
        print("wtf man.")

state = StateHandler()

statemachine()
            
#asyncio.get_event_loop().run_until_complete(connect())