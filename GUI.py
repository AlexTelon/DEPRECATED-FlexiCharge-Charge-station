import qrcode
import platform
import io
import PySimpleGUI as sg
from PIL import Image

def GUI(chargerID,img_startingUp,img_qrCode):

    sg.theme('Black')
    
    backgroundLayout =  [
                            [sg.Image(data=img_startingUp, key='IMAGE', size=(480, 800))]
                        ]
    
    IdLayout =  [
                    [  
                        sg.Text(chargerID[0], font=('ITC Avant Garde Std Md', 33), key='ID0', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[1], font=('ITC Avant Garde Std Md', 33), key='ID1', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[2], font=('ITC Avant Garde Std Md', 33), key='ID2', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[3], font=('ITC Avant Garde Std Md', 33), key='ID3', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[4], font=('ITC Avant Garde Std Md', 33), key='ID4', justification='center', pad=(20,0), text_color='white'),
                        sg.Text(chargerID[5], font=('ITC Avant Garde Std Md', 33), key='ID5', justification='center', pad=(20,0), text_color='white')
                    ]
                ]

    qrCodeLayout =  [
                        [   
                            sg.Image(data=img_qrCode, key='QRCODE', size=(285,285)) 
                        ]
                    ]
    
    chargingPowerLayout =   [
                                [  
                                    sg.Text("61 kW at 7.3kWh", font=('Lato', 20), key='POWER', justification='center', text_color='white')
                                ]
                            ]
    
    chargingTimeLayout =   [
                                [  
                                    sg.Text("4 minutes until full", font=('Lato', 20), key='TIME', justification='center', text_color='white')
                                ]
                            ]

    chargingPercentLayout = [
                                [
                                    sg.Text("0", font=('ITC Avant Garde Std Md', 160), key='PERCENT', text_color='red')
                                ]
                            ]
   
    chargingPercentMarkLayout = [
                                    [
                                        sg.Text("%", font=('ITC Avant Garde Std Md', 55), key='PERCENTMARK', text_color='red')
                                    ]
                                ]

    priceLayout =   [
                        [
                            sg.Text("Price: 137.00kr / kWh", font=('ITC Avant Garde Std Md', 13), key='PRICE', text_color='white')
                        ]
                    ]
   
    background_window = sg.Window(title="FlexiCharge", layout=backgroundLayout, no_titlebar=True, location=(0,0), size=(480,800), keep_on_top=False, margins=(0,0)).finalize()
    if platform.system() != 'Windows':
        background_window.Maximize()
    background_window.TKroot["cursor"] = "none"

    id_window = sg.Window(title="FlexiChargeTopWindow", keep_on_top=True, layout=IdLayout, location=(26,703), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    id_window.TKroot["cursor"] = "none"
    id_window.hide()

    qr_window = sg.Window(title="FlexiChargeQrWindow", keep_on_top=True, layout=qrCodeLayout, location=(95, 165), grab_anywhere=False, no_titlebar=True, size=(285,285), background_color='white', margins=(0,0)).finalize() #location=(95, 165) bildstorlek 285x285 från början
    qr_window.TKroot["cursor"] = "none"
    qr_window.hide()

    chargingPower_window = sg.Window(title="FlexiChargeChargingPowerWindow", keep_on_top=True, layout=chargingPowerLayout, location=(162, 645), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingPower_window.TKroot["cursor"] = "none"
    chargingPower_window.hide()

    chargingTime_window = sg.Window(title="FlexiChargeChargingTimeWindow", keep_on_top=True, layout=chargingTimeLayout, location=(162, 694), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingTime_window.TKroot["cursor"] = "none"
    chargingTime_window.hide()

    chargingPercent_window = sg.Window(title="FlexiChargeChargingPercentWindow", keep_on_top=True, layout=chargingPercentLayout, location=(140, 245), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingPercent_window.TKroot["cursor"] = "none"
    chargingPercent_window.hide()

    chargingPercentMark_window = sg.Window(title="FlexiChargeChargingPercentWindow", keep_on_top=True, layout=chargingPercentMarkLayout, location=(276, 350), grab_anywhere=False, no_titlebar=True, background_color='black', margins=(0,0)).finalize()
    chargingPercentMark_window.TKroot["cursor"] = "none"
    chargingPercentMark_window.hide()

    price_window = sg.Window(title="FlexiChargeTopWindow", keep_on_top=True, layout=priceLayout, location=(24,610), grab_anywhere=False, no_titlebar=True, background_color='white', margins=(0,0)).finalize()
    price_window.TKroot["cursor"] = "none"
    price_window.hide()

    return background_window, id_window, qr_window, chargingPower_window, chargingTime_window, chargingPercent_window, chargingPercentMark_window, price_window

#pLeaSe dOn't change any of the values in generateQR or x and y in GUI. It looks bad on the PC but works good on the Pi.
def generateQR(chargerID):
    qr = qrcode.QRCode(
        version=8,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(chargerID)
    qr.make(fit=True)
    img_qrCodeGenerated = qr.make_image(fill_color="black", back_color="white")
    #img_qrCodeGenerated = qrcode.make(chargerID)
    type(img_qrCodeGenerated)
    img_qrCodeGenerated.save("Pictures/QrCode.png")

def get_img_data(f, maxsize=(480, 800)):
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def refreshWindows(window_back, window_id, window_qr, window_chargingPower, window_chargingTime, window_chargingPercent, window_chargingPercentMark, window_price):
    window_back.refresh()
    window_id.refresh()
    window_qr.refresh()
    window_chargingPower.refresh()
    window_chargingTime.refresh()
    window_chargingPercent.refresh()
    window_chargingPercentMark.refresh()
    window_price.refresh()