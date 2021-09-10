import asyncio
import websockets
import json

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call

async def connect():
    url = "ws://localhost:9000/CP_Carl"
    async with websockets.connect(url) as websocket:
        print("Connected.")
        x = [2, "CP_Carl", "Authorize", {"idTag": "B4A63CDF"}]
        y = json.dumps(x)
        await websocket.send(y)
        while True:
            try:
                pass
            except websockets.ConnectionClosed:
                print("Disconnected.")

async def heartBeat():      #make some kind of timer loop 
    url = "ws://localhost:9000/CP_Carl"
    async with websockets.connect(url) as websocket:
        print("Sent heartbeat.")
        x = [2, "CP_Carl", "Heartbeat", {}]
        y = json.dumps(x)
        await websocket.send(y)

asyncio.get_event_loop().run_until_complete(connect())
asyncio.get_event_loop().run_until_complete(heartBeat())