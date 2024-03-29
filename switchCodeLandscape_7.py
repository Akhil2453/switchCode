#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
from tkinter import *
import tkinter.font as tkFont
import requests
from PIL import Image, ImageTk

def raise_frame(frame):
    frame.tkraise()

#Declare Global Variables
root = None
dfont = None
welcome = None
msg = None
value = None
number = ""
count = ""
cnt = 0

#GPIO pins
button = 18

#Fulscreen or windowed
fullscreen = False

def number_e():
    global number
    global count
    global cnt
    num = number.get()
    number.set(num)
    pushCnt = str(cnt)
    print(num)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': num, 'MCID': '002000330', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    num=""
    number.set(num)
    cnt = 0
    count.set(num)
    raise_frame(PageTwo)
    root.update()
    time.sleep(5)
    raise_frame(welcome)
    root.update()

def exit():
    global number
    global count
    global cnt
    print("checking the count for no number entered: ", cnt)
    pushCnt = str(cnt)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': '9999999999', 'MCID': '002000330', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    num=""
    number.set(num)
    cnt = 0
    count.set(num)
    raise_frame(PageTwo)
    root.update()
    time.sleep(5)
    raise_frame(welcome)
    root.update()

def num_get(num):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(num))

def delt():
    temp = e.get()[:-1]
    e.delete(0, END)
    e.insert(0, temp)

def clr():
    e.delete(0, END)

def cancel():
    global cnt
    raise_frame(welcome)
    cnt = 0
    e.delete(0, END)

#toggle fullscreen
def toggle_fullscreen(event=None):
    global root
    global fullscreen
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()

#go into windowed mode
def end_fullscreen(event=None):
    global root
    global fullscreen
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize()

#resize font based on screen size
def resize(event=None):
    global dfont
    global welcome
    new_size = -max(12, int((welcome.winfo_height() / 10)))
    dfont.configure(size=new_size)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def endprogram():
    GPIO.cleanup()

def loop():
    temp = 1
    global root
    global value
    global msg
    global number
    global num
    global visible
    global count
    global cnt
    c=0
    #time.sleep(1)
    a=GPIO.input(button)
    if(a == False):
        time.sleep(0.2)
        c=c+1
        print("Button Pressed:",c,"times")
        raise_frame(PageOne)
        cnt = cnt + 1
        count.set(cnt)
        print("count: ", cnt)
        root.after(30000, exit)
    root.after(500, loop)

#create the window
root = Tk()
root.title("Bottle Crusher")
root.geometry('1024x640')

welcome = Frame(root)
PageOne = Frame(root)
PageTwo = Frame(root)

for frame in (welcome, PageOne, PageTwo):
    frame.grid(row=8, column=3, sticky='news')

value = DoubleVar()
msg = StringVar()
number = StringVar()
count = StringVar()

dfont = tkFont.Font(size=-6)
myfont = tkFont.Font(size=24)
mfont = tkFont.Font(size=20)
nfont = tkFont.Font(size=20)
wel = Label(welcome, text="\nWelcome to Biocrux Zone", font=myfont)
wel.grid(row=1, column=0, padx=50, pady=20)
#wel.place(x=70, y=200)
wel1 = Label(welcome, text="\nPlease drop\n\nyour waste bottle here\n\nto get rewarded", font=myfont)
wel1.grid(row=2, column=0, padx=50, pady=0)
load = Image.open("/home/pi/switchCode/logo.jpg")
load = load.resize((212,112), Image.BICUBIC)
render = ImageTk.PhotoImage(load)
img = Label(welcome, image=render)
img.image = render
#img.place(x=87, y=0)
img.grid(row=0, column=0, padx=406, pady=25)

Label(PageOne, text="Enter your Mobile Number to get Rewarded\n", font=myfont).grid(columnspan=3, row=0, column=0, padx=(185,1), pady=15)
Label(PageOne, text="Bottle Count: ", font=myfont).grid(row=1, column = 0, padx=(250,1), pady=5, columnspan=2)
Label(PageOne, textvariable=count, font=myfont).place(x=585, y=125) #grid(row=1, column=2, padx=(0,0), pady=5)
Label(PageOne, text="\n", font=myfont).grid(row=1, column = 3, padx=(0,0), pady=0)
e = Entry(PageOne, textvariable=number, width=20, font=myfont)
e.grid(columnspan=3, row=2, column=0, padx=(200,1), pady=15)
Button(PageOne, text='1', command=lambda:num_get(1), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=3, column=0, padx=(200,10), pady=(15,0))
Button(PageOne, text='2', command=lambda:num_get(2), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=3, column=1, padx=(0,10), pady=(15,0))
Button(PageOne, text='3', command=lambda:num_get(3), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=3, column=2, padx=(0,10), pady=(15,0))
Button(PageOne, text='4', command=lambda:num_get(4), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=4, column=0, padx=(200,10), pady=(10,0))
Button(PageOne, text='5', command=lambda:num_get(5), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=4, column=1, padx=(0,10), pady=(10,0))
Button(PageOne, text='6', command=lambda:num_get(6), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=4, column=2, padx=(0,10), pady=(10,0))
Button(PageOne, text='7', command=lambda:num_get(7), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=5, column=0, padx=(200,10), pady=(10,0))
Button(PageOne, text='8', command=lambda:num_get(8), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=5, column=1, padx=(0,10), pady=(10,0))
Button(PageOne, text='9', command=lambda:num_get(9), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=5, column=2, padx=(0,10), pady=(10,0))
Button(PageOne, text='0', command=lambda:num_get(0), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=6, column=1, padx=(0,10), pady=(10,0))
Button(PageOne, text='Delete', command=delt, borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=6, column=2, padx=(0,10), pady=(10,0))
Button(PageOne, text='Clear', command=clr, borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=6, column=0, padx=(200,10), pady=(10,0))
Button(PageOne, text='Enter', bg='#0052cc', fg='#ffffff', command=number_e, borderwidth=5, relief=RAISED, height=1, width=22, font=nfont).grid(row=7, column=0, columnspan=2,padx=(200,10), pady=(10,0))
Button(PageOne, text='Cancel', command=cancel, borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=7, column=2, padx=(0,10), pady=(10,0))

#Label(PageTwo, text=" ", font=myfont).grid(row=0, column=1, padx=5, pady=5)
Label(PageTwo, text="Thank You\n\nfor your contribution\n\nin making our environment clean.\n\n\n\nBe Clean. Go Green.", font=myfont).grid(row=1, column=1, padx=250, pady=150)
#Button(PageTwo, text="welcomeScreen", command=lambda:raise_frame(welcome)).grid(row=2, column=1, padx=35, pady=35)
# load1 = Image.open("message.png")
# load1 = load1.resize((950,640), Image.BICUBIC)
# render1 = ImageTk.PhotoImage(load1)
# img1 = Label(PageTwo, image=render1)
# img1.image = render1
# img.grid(row=0, column=0, padx=37, pady=0)

root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

root.bind('<Configure>', resize)

setup()

root.after(1000, loop)
raise_frame(welcome)
toggle_fullscreen()
root.mainloop()
