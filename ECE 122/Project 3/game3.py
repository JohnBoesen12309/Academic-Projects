from tkinter import *
import time
from Racket import Racket
from Mapping_for_Tkinter import Mapping_for_Tkinter
from Ball import Ball
import random

t=0
total=0
boxes=[]
count=15
xlist=[]
ylist=[]
z1=0
dots=[]

######Setup######
swidth=input("Enter window size in pixels (Enter for 600):")
if swidth=="":
    width=600
else:
    width=int(swidth)
m=Mapping_for_Tkinter(-1*width/2,width/2,-1*width/2,width/2,width)
root=Tk()
canvas=Canvas(root,width=m.get_width(),height=m.get_height(),bg="white")
canvas.pack()
r1=Racket(m,canvas,width/10,width/60)
top=m.get_y(r1.top-(m.get_width()/120))

for j in range(3): #Creates the squares with random colors and the dots with random coordinates
    for i in range(5):
        color=random.choice(["red","blue"])
        a=i*m.get_width()/5
        b=j*m.get_width()/5
        box=canvas.create_rectangle(a,b,a+m.get_width()/5,b+m.get_width()/5,fill=color,outline=color)
        boxes=boxes+[box]
        x=random.uniform(m.get_width()/120,a+m.get_width()/5)
        xlist.append(x-m.get_width()/120) #Keeps track of max and min x-value for the dots
        xlist.append(x+m.get_width()/120)
        y=random.uniform(m.get_width()/120,b+m.get_width()/5)
        ylist.append(y-m.get_width()/120) #Keeps track of max and min y-values for the dots
        ylist.append(y+m.get_width()/120)
        dot=canvas.create_oval(x-2*m.get_width()/120,y-2*m.get_width()/120,x+2*m.get_width()/120,y+2*m.get_width()/120,fill="blue",outline="blue")
        dots.append([dot])
ball1=Ball(m,canvas,0,top,300,53)
canvas.bind("<Button-1>",lambda e:r1.shift_left())
canvas.bind("<Button-3>",lambda e:r1.shift_right())

######Ball simulation######
while True:
    z = 0
    z1=0
    t = t + 0.01
    total = total + 0.01
    side = ball1.update_xy(t,r1)
    root.update()
    while z<len(xlist): #Checks if the ball hits a dot
        if xlist[z]-5<=m.get_i(ball1.x)<=xlist[z+1]+5 and ylist[z]-5<=m.get_j(ball1.y)<=ylist[z+1]+5:
            print("%s Dots Left"%(len(dots)-1))
            canvas.delete(dots[z1]) #Deletes the dot that the ball hit and removes it from the count
            del dots[z1]
            del xlist[z+1]
            del xlist[z]
            del ylist[z+1]
            del ylist[z]
            canvas.update()
            count=count-1
            z=0 # Resets the counters
            z1=0
            break
        z=z+2
        z1=z1+1
    if side == 1 or count==0:
        print("Game Over! Dots Remaining: %s \nTotal time: %s" % (count,total))
        break
    elif side == 5:
        ball1.pointer()
        canvas.bind("<Button-1>", lambda e: r1.shift_left()) #Re-enables the racket to move
        canvas.bind("<Button-3>", lambda e: r1.shift_right())
        t=0
    elif side == 3 or side == 4:
        t = 0
    elif side==2:
        for box in boxes: #Randomly changes the color of the boxes
            color=random.choice(["red","blue"])
            canvas.itemconfig(box,fill=color,outline=color)
        t=0
    time.sleep(0.01)
canvas.mainloop()