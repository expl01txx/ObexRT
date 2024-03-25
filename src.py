import tkinter as tk
from tkinter import ttk
from tkinter import *

root = tk.Tk()
root.geometry('400x200')
root.title("[ObexRT] Crackme app")

text = StringVar()

def check():
    global text
    if text.get() == "Prop2":
        print("Done)")
    else:
        print("Login error")


inp = ttk.Entry(textvariable=text)
inp.pack()

btn = ttk.Button(text="Login", command=check)
btn.pack()
root.mainloop()

del check, inp, btn, root, text
exit(0)