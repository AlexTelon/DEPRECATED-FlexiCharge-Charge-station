import asyncio
import websockets
import json
import time

url = "ws://54.220.194.65:1337/ssb"

async def main():
    async with websockets.connect(url, ping_interval=None, timeout=None) as websocket:
                x = ['ssb', 'RemoteStart']
                y = json.dumps(x)
                await websocket.send(y)
                print(await websocket.recv())
asyncio.get_event_loop().run_until_complete(main())         