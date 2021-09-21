import PySimpleGUI as sg
import os
import io
import time
from PIL import Image


def get_img_data(f, maxsize=(480, 800)):
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

sg.theme('Black')

img_chargerID = get_img_data('Pictures/chargerid.png')
img_startingUp = get_img_data('Pictures/StartingUp.png')
img_notAvailable = get_img_data('Pictures/NotAvailable.png')
img_errorWhileCharging = get_img_data('Pictures/AnErrorOccuredWhileCharging.png')
img_authorizing = get_img_data('Pictures/authorizing.png')
img_charging = get_img_data('Pictures/charging.png')
img_chargingCancelled = get_img_data('Pictures/ChargingCancelled.png')
img_connectingToCar = get_img_data('Pictures/ConnectingToCar.png')
img_disconnectingFromCar = get_img_data('Pictures/DisconnectingFromCar.png')
img_followInstructions = get_img_data('Pictures/FollowInstructions.png')
img_fullyCharged = get_img_data('Pictures/FullyCharged.png')
img_plugInCable = get_img_data('Pictures/PlugInCable.png')
img_rfidNotValid = get_img_data('Pictures/RFIDnotValid.png')
img_unableToCharge = get_img_data('Pictures/UnableToCharge.png')

layout1 =    [
                [sg.Image(data=img_startingUp, key='__IMAGE__', size=(480, 800))]
            ]

window = sg.Window(title="FlexiCharge", layout=layout1, no_titlebar=True, location=(0,0), size=(480,800), keep_on_top=False).Finalize()
#window.Maximize()
window.TKroot["cursor"] = "none"

screen = 0
while True:
    if screen == 2:
        screen = 0
        window['__IMAGE__'].update(data=img_chargerID)
        window.refresh()
    else:
        screen += 1
        time.sleep(3)
window.close()