import asyncio
import websockets

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call

async def connect():
    url = "ws://localhost:9000"
    async with websockets.connect(url) as websocket:
        print("connected")
        while True:
            pass
            


asyncio.get_event_loop().run_until_complete(connect())