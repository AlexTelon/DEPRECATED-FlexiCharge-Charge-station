import tkinter as tk
from PIL import Image, ImageTk

def change_to_not_available():
    startingup_frame.pack_forget()
    notavailable_frame.pack(expand=True, fill='both')
    
def change_to_available():
    notavailable_frame.pack_forget()
    available_frame.pack(expand=True, fill='both')

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

# Starting up screen ######################

#Logo
img_logoGreen = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/color-2.png")
img_logoGreen = ImageTk.PhotoImage(img_logoGreen)
logo_startingup = tk.Label(startingup_frame, image=img_logoGreen, bg='black')
logo_startingup.image = img_logoGreen
logo_startingup.place(x=137, y=202)

#Flexi charge text
img_flexiCharge = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/flexichargetext1.png")
img_flexiCharge = ImageTk.PhotoImage(img_flexiCharge)
logo_flexiCharge1 = tk.Label(startingup_frame, image=img_flexiCharge, bg='black')
logo_flexiCharge1.image = img_logoGreen
logo_flexiCharge1.place(x=88, y=479)

#Starting up text
startingup_text = tk.Label(startingup_frame, text="Starting up...", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
startingup_text.place(x=153, y=621)

#Button
btn_change_to_notavailable = tk.Button(startingup_frame, text='Change to notavailable', command=change_to_not_available)
btn_change_to_notavailable.pack(side='bottom')

##########################################

#   Avalable screen ######################

#Logo
chargeid = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/chargerid.png")
chargeid = ImageTk.PhotoImage(chargeid)
img_1 = tk.Label(available_frame, image=chargeid, bg='black')
img_1.image = chargeid
img_1.place(x=9, y=4)

#chargerID_display
chargerID1 = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/chargerid2.png")
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

##########################################

# Not availeble screen ####################

#Logo
logo = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/white.png")
logo = ImageTk.PhotoImage(logo)
img_1 = tk.Label(notavailable_frame, image=logo, bg='black')
img_1.image = logo
img_1.place(x=90, y=40)

#Cross
cross = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/cross.png")
cross = ImageTk.PhotoImage(cross)
img_2 = tk.Label(notavailable_frame, image=cross, bg='black')
img_2.image = cross
img_2.place(x=118, y=202)

#instuctions
instuctions = tk.Label(notavailable_frame, text="Charger not available", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
instuctions.place(x=118, y=563)

instuctions = tk.Label(notavailable_frame, text="This charger is out of order\n and is not able to charge at the moment.", font="ITCAvantGardeStd", bg='black', fg='#E5E5E5')
instuctions.place(x=108, y=701)

#Button
btn_change_to_notavailable = tk.Button(notavailable_frame, text='Change to available', command=change_to_available)
btn_change_to_notavailable.pack(side='bottom')

############################################


startingup_frame.pack(expand=True, fill='both')

root.mainloop()