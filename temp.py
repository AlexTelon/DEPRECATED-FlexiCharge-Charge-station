import json

temp = 15

b = [{ "transactionId": temp, "latestMeterValue": 133769, "CurrentChargePercentage": 69 }]

x = json.dumps(b)
print(x)
    
y = [ 2,
  "uniqueID",
  "DataTransfer", { 
    "messageId": "ChargeLevelUpdate",
    "data": x } ]
z = json.dumps(y)

print(z)