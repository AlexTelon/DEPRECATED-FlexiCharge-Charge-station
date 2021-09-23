import asyncio
import websockets
import json
import time


#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call


from StateHandler import States
from StateHandler import StateHandler


        
async def send_heartbeat():
    while True:
        print("heartbeat!!")
        await asyncio.sleep(2)
    # hb = [2, "knaskalas", "Heartbeat", {}]
    # z = json.dumps(hb)
    # print("Sending Heartbeat...")
    # await ws.send(z)
    # await ws.recv()
        

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

          
async def testfunc():
    print("kalasknas")
          
          
async def statemachine():
    i = 1
    url = "ws://localhost:9000/knaskalas"
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
        print("Connected.")
        while True:

            if state.get_state() == States.S_STARTUP:
                print("Starting up...")
                
                # Only for temporary testing purposes: #
                #await connect()
                await testfunc()
                
                state.set_state(States.S_AVAILABLE)
                ### Pseudo-code: ###
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
            
            
   

state = StateHandler()

#statemachine()

loop = asyncio.get_event_loop()
#sched = AsyncIOScheduler()
#sched.add_job(send_heartbeat, 'interval', seconds=1)
#sched.start()
tasks = [
    loop.create_task(statemachine()),
    loop.create_task(send_heartbeat()),
]

loop.run_until_complete(asyncio.wait(tasks))
#asyncio.get_event_loop().run_until_complete(statemachine())