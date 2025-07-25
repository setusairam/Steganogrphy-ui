# file: steganography_app.py

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from stegano import lsb  # pip install stegano

root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x500+250+180")
root.resizable(False, False)
root.configure(bg="#2f4155")

filename = None
secret = None

def showimage():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select Image File',
        filetypes=(
            ("PNG file", "*.png"),
            ("JPG File", "*.jpg"),
            ("All files", "*.*")
        )
    )
    if filename:
        img = Image.open(filename)
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img, width=250, height=250)
        lbl.image = img

def Hide():
    global secret
    if filename:
        message = text1.get(1.0, END).strip()
        if message:
            secret = lsb.hide(filename, message)

def Show():
    if filename:
        try:
            clear_message = lsb.reveal(filename)
            text1.delete(1.0, END)
            if clear_message:
                text1.insert(END, clear_message)
            else:
                text1.insert(END, "No hidden message found.")
        except Exception as e:
            text1.delete(1.0, END)
            text1.insert(END, f"Error: {str(e)}")

def save():
    if secret:
        secret.save("hidden.png")

# First frame for image
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second frame for text
frame2 = Frame(root, bd=3, bg="white", width=340, height=280, relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font=("Roboto", 12), bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=280)

Scrollbar1 = Scrollbar(frame2)
Scrollbar1.place(x=320, y=0, height=280)
Scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=Scrollbar1.set)

# Third frame for open/save buttons
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)

Label(frame3, text="Picture, image, photo file", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth frame for hide/show buttons
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)

Label(frame4, text="Picture, image, photo file", bg="#2f4155", fg="yellow").place(x=20, y=5)

root.mainloop()