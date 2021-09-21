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

chargerID = get_img_data('Pictures/chargerid.png')
startingUp = get_img_data('Pictures/StartingUp.png')
notAvailable = get_img_data('Pictures/NotAvailable.png')

layout1 =    [
                [sg.Image(data=startingUp, key='__IMAGE__', size=(480, 800))]
            ]

window = sg.Window(title="FlexiCharge", layout=layout1, no_titlebar=True, location=(0,0), size=(480,800), keep_on_top=False).Finalize()
#window.Maximize()

test = 0
while True:
    if test == 2:
        test = 0
        window['__IMAGE__'].update(data=chargerID)
        window.refresh()
    else:
        test += 1
        time.sleep(3)
window.close()