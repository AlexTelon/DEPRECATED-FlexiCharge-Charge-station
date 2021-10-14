import json
import asyncio
from StateHandler import States
from StateHandler import StateHandler
from datetime import datetime

async def authorize(idTag, websocket):
    x = [2, "ssb", "Authorize", {"idTag": idTag}]
    y = json.dumps(x)
    await websocket.send(y)
    response = await websocket.recv()

async def send_heartbeat(websocket):
    while True:
        hb = [2, "ssb", "Heartbeat", {}]
        z = json.dumps(hb)
        print("Sending Heartbeat...")
        await websocket.send(z)
        print(await websocket.recv())
        await asyncio.sleep(2)

async def reserveNow(websocket, res, state):
    #global state
    #check if already booked?
    try:
        res_pared = json.loads(res)
        print(res_pared)

        pkg_accepted = [3, res_pared[1], "ReserveNow", {"status": "Accepted"}]
        pkg_accepted_send = json.dumps(pkg_accepted)
        await websocket.send(pkg_accepted_send)
        state.set_state(States.S_BUSY)
        return res_pared
    except:
        pkg_rejected = [3, res_pared[1], "ReserveNow", {"status": "Rejected"}]
        pkg_rejected_send = json.dumps(pkg_rejected)
        await websocket.send(pkg_rejected_send)
        #state.set_state(States.S_AVAILABLE)
        return 0

async def remoteStartTransaction(websocket):
    try:
        # Send fake request from server
        #pkg = ["ssb", "RemoteStart"]
        #pkg_send = json.dumps(pkg)
        #await websocket.send(pkg_send)
        # Retrieve request
        response = await websocket.recv()
        response_parsed = json.loads(response)
        print(response_parsed)

        # Send back Accepted
        pkg_accepted = [3,
            response_parsed[1],
            response_parsed[2],
            {
            "status": "Accepted"
                               } ]
        pkg_accepted_send = json.dumps(pkg_accepted)
        await websocket.send(pkg_accepted_send)
        return True
    except:
        return False

async def remoteStopTransaction(websocket):
    try:
        # Send fake request from server
        #pkg = ["ssb", "RemoteStop"]
        #pkg_send = json.dumps(pkg)
        #await websocket.send(pkg_send)

        # Retrieve request
        #response = await websocket.recv()
        #response_parsed = json.loads(response)
        #print(response_parsed)
        #if (response_parsed[2] == "StopTransaction"):
        # Send back Accepted
        pkg_accepted = [3,
            response_parsed[1],
            response_parsed[2],
            {
            "status": "Accepted"
                               } ]
        pkg_accepted_send = json.dumps(pkg_accepted)
        await websocket.send(pkg_accepted_send)

            #event.set()

    except:
        pass

async def statusNotification(websocket):
    pkg = [1, {'connectorID': 1,
    'errorCode': 'NoError',
    'info': 0,
    'status': 'Available',
    'timestamp': datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
    'vendorId': 0,
    'vendorErrorCode': 0}]
    pkg_send = json.dumps(pkg)
    await websocket.send(pkg_send)

    response = await websocket.recv()
    response_parsed = json.loads(response)
    print(response_parsed)

async def startTransaction(websocket, json_data, uniqueID):
    x = [2, uniqueID, "StartTransaction", {
            "connectorId": json_data[3]['connectorID'],
            "idTag": json_data[3]['idTag'],
            "timestamp": datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
            "meterStart": 1,
            "reservationId": json_data[3]['reservationID']
        }]
    y = json.dumps(x)
    await websocket.send(y)
    resp = await websocket.recv()
    return json.loads(resp)

async def stopTransaction(websocket, json_data, uniqueID):
    x = [2, uniqueID, "StopTransaction", {
        "transactionId": json_data[3]['transactionId'],
        "idTag": json_data[3]['idTagInfo'],
        "timestamp": datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
        "meterStop": 2
    }]
    y = json.dumps(x)
    await websocket.send(y)
    print("Response: " + await websocket.recv())

async def dataTransfer(websocket, dataUniqueID, latestCharge, currentCharge):
    b = [{ "transactionId": str(346), "latestMeterValue": str(latestCharge), "CurrentChargePercentage": str(currentCharge) }]

    y = json.dumps(b)

    x = [   2,
            dataUniqueID,
            "DataTransfer",
            {
                "messageId": "ChargeLevelUpdate",
                "data": y
            }
        ]
    y = json.dumps(x)
    await websocket.send(y)
    print("Response: " + await websocket.recv())


async def HandleReceive(websocket, event, dataUniqueID, latestCharge, currentCharge, temp):
    print("handling the recv")
    functionText = "none"
    if temp == 0:
        pkg_recv = await websocket.recv()
        json_data = json.loads(pkg_recv)
        functionText = json_data[2]
        print(json_data)

    if functionText == "RemoteStopTransaction":
        print("remoteStop")
        await remoteStopTransaction(websocket)
        event.set()
    else:
        print("dataTransfer")
        await dataTransfer(websocket, dataUniqueID, latestCharge, currentCharge)
