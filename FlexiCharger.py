import tkinter as tk
from PIL import Image, ImageTk

def change_to_not_available():
    startingup_frame.pack_forget()
    notavailable_frame.pack(expand=True, fill='both')
    
def change_to_available():
    notavailable_frame.pack_forget()
    available_frame.pack(expand=True, fill='both')

def change_to_authorizing():
    available_frame.pack_forget()
    authorizing_frame.pack(expand=True, fill='both')

listID =  [3, 5, 7, 9, 3, 4]

root = tk.Tk()
root.geometry('480x800')
root.overrideredirect(True)
root.overrideredirect(False)
#root.attributes('-fullscreen', True)   #kommentera inte bort vid användning på raspberry
#root.config(cursor="none")             #kommentera inte bort vid användning på raspberry

startingup_frame = tk.Frame(root, width=480, height=800, bg='black')
notavailable_frame = tk.Frame(root, width=480, height=800, bg='black')
available_frame = tk.Frame(root, width=480, height=800, bg='black')
authorizing_frame = tk.Frame(root, width=480, height=800, bg='black')

# Starting up screen ######################

#Green lightning logo
img_greenLightning = Image.open("Pictures/color-2.png")
img_greenLightning = ImageTk.PhotoImage(img_greenLightning)
logo_greenLightning = tk.Label(startingup_frame, image=img_greenLightning, bg='black')
logo_greenLightning.image = img_greenLightning
logo_greenLightning.place(x=137, y=202)

#Flexi charge text
img_flexiChargeText = Image.open("Pictures/flexichargetext1.png")
img_flexiChargeText = ImageTk.PhotoImage(img_flexiChargeText)
logo_flexiChargeText = tk.Label(startingup_frame, image=img_flexiChargeText, bg='black')
logo_flexiChargeText.image = img_flexiChargeText
logo_flexiChargeText.place(x=88, y=479)

#Starting up text
startingUp_text = tk.Label(startingup_frame, text="Starting up...", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
startingUp_text.place(x=153, y=621)

#Button
btn_change_to_not_available = tk.Button(startingup_frame, text='Change to notavailable', command=change_to_not_available)
btn_change_to_not_available.pack(side='bottom')

##########################################

#   Avalable screen ######################

#Logo
chargeid = Image.open("Pictures/chargerid.png")
chargeid = ImageTk.PhotoImage(chargeid)
img_1 = tk.Label(available_frame, image=chargeid, bg='black')
img_1.image = chargeid
img_1.place(x=9, y=4)

#chargerID_display
chargerID1 = Image.open("Pictures/chargerid2.png")
resized = chargerID1.resize((40,64), Image.ANTIALIAS)
new_resized = ImageTk.PhotoImage(resized)
img_1 = tk.Label(available_frame, image=new_resized, bg='black')
img_1.image = new_resized
img_1.place(x=57, y=708)

#chargerID_display
img_2 = tk.Label(available_frame, image=new_resized, bg='black')
img_2.image = new_resized
img_2.place(x=126, y=708)

#chargerID_display
img_3 = tk.Label(available_frame, image=new_resized, bg='black')
img_3.image = new_resized
img_3.place(x=195, y=708)

#chargerID_display
img_4 = tk.Label(available_frame, image=new_resized, bg='black')
img_4.image = new_resized
img_4.place(x=264, y=708)

#chargerID_display
img_5 = tk.Label(available_frame, image=new_resized, bg='black')
img_5.image = new_resized
img_5.place(x=333, y=708)


#chargerID_display
img_6 = tk.Label(available_frame, image=new_resized, bg='black')
img_6.image = new_resized
img_6.place(x=402, y=708)


#ChargerID
ChargerID = tk.Label(available_frame, text=listID [0], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
ChargerID.place(x=65, y=714)

ChargerID = tk.Label(available_frame, text=listID [1], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
ChargerID.place(x=134, y=714)

ChargerID = tk.Label(available_frame, text=listID [2], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
ChargerID.place(x=203, y=714)

ChargerID = tk.Label(available_frame, text=listID [3], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
ChargerID.place(x=272, y=714)

ChargerID = tk.Label(available_frame, text=listID [4], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
ChargerID.place(x=341, y=714)

ChargerID = tk.Label(available_frame, text=listID [5], font=("ITCAvantGardeStd", 30), bg='white', fg='black')
ChargerID.place(x=410, y=714)

#Button
btn_change_to_authorizing = tk.Button(available_frame, text='Change to authorizing', command=change_to_authorizing)
btn_change_to_authorizing.pack(side='bottom')

##########################################

# Not availeble screen ####################

#Flexi charge with lightning text
img_flexiChargeTextLightning = Image.open("Pictures/flexichargetextlightning.png")
img_flexiChargeTextLightning = ImageTk.PhotoImage(img_flexiChargeTextLightning)
logo_flexiChargeTextLightning = tk.Label(notavailable_frame, image=img_flexiChargeTextLightning, bg='black')
logo_flexiChargeTextLightning.image = img_flexiChargeTextLightning
logo_flexiChargeTextLightning.place(x=90, y=40)

#Cross
img_redCross = Image.open("Pictures/cross.png")
img_redCross = ImageTk.PhotoImage(img_redCross)
logo_redCross = tk.Label(notavailable_frame, image=img_redCross, bg='black')
logo_redCross.image = img_redCross
logo_redCross.place(x=118, y=202)

#instuctions
instuctions = tk.Label(notavailable_frame, text="Charger not available", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
instuctions.place(x=118, y=563)

instuctions = tk.Label(notavailable_frame, text="This charger is out of order\n and is not able to charge at the moment.", font="ITCAvantGardeStd", bg='black', fg='#E5E5E5')
instuctions.place(x=108, y=701)

#Button
btn_change_to_notavailable = tk.Button(notavailable_frame, text='Change to available', command=change_to_available)
btn_change_to_notavailable.pack(side='bottom')

############################################

# Authorizing Screen ####################

#Logo
logo = Image.open("Pictures/flexichargetextlightning.png")
logo = ImageTk.PhotoImage(logo)
img_1 = tk.Label(authorizing_frame, image=logo, bg='black')
img_1.image = logo
img_1.place(x=90, y=40)

#Dongle
dongle = Image.open("Pictures/Group 3-14.png")
dongle = ImageTk.PhotoImage(dongle)
img_2 = tk.Label(authorizing_frame, image=dongle, bg='black')
img_2.image = img_redCross
img_2.place(x=118, y=202)

#Authorizing text
authorizing_text = tk.Label(authorizing_frame, text="Authorizing...", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
authorizing_text.place(x=158, y=563)

############################################


startingup_frame.pack(expand=True, fill='both')

root.mainloop()