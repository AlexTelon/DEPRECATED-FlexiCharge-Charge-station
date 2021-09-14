import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

canvas = tk.Canvas(root, width=480, height=800, bg='black')
canvas.grid(columnspan=3)

#Logo
logo = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/white.png")
logo = ImageTk.PhotoImage(logo)
img_1 = tk.Label(image=logo, bg='black')
img_1.image = logo
img_1.place(x=90, y=40)

#Cross
cross = Image.open("C:/Users/ericc/OneDrive/Desktop/PythonTest/cross.png")
cross = ImageTk.PhotoImage(cross)
img_2 = tk.Label(image=cross, bg='black')
img_2.image = cross
img_2.place(x=118, y=202)

#instuctions
instuctions = tk.Label(root, text="Charger not available", font=("ITCAvantGardeStd", 20), bg='black', fg='#E5E5E5')
instuctions.place(x=118, y=563)

instuctions = tk.Label(root, text="This charger is out of order\n and is not able to charge at the moment.", font="ITCAvantGardeStd", bg='black', fg='#E5E5E5')
instuctions.place(x=108, y=701)



root.mainloop()