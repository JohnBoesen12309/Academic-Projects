from Racket import Racket
import time
from game1 import setup
import math

root,m,canvas,ball1,r1=setup()
r2=Racket(m,canvas,2*r1.Lx,r1.Ly,0,0)
ball1.theta=math.pi/4 #Changes ball speed and starting angle
ball1.v=300

canvas.bind("<Button-1>",lambda e:r2.shift_left())
canvas.bind("<Button-3>",lambda e:r2.shift_right())
canvas.itemconfig(r1.racket,fill="red") #Starts the bottom racket as red

t=0
total=0
while True:
    t = t + 0.01
    total = total + 0.01
    side = ball1.update_xy(t,r1,r2)
    root.update()
    if side==5: #
        canvas.itemconfig(r1.racket, fill="red")
        canvas.itemconfig(r2.racket, fill="black")
        t = 0
        canvas.bind("<Button-1>", lambda e: r2.shift_left())
        canvas.bind("<Button-3>", lambda e: r2.shift_right())
    elif side==6:
        canvas.itemconfigure(r2.racket, fill="red")
        canvas.itemconfigure(r1.racket, fill="black")
        t = 0
        canvas.bind("<Button-1>", lambda e: r1.shift_left())
        canvas.bind("<Button-3>", lambda e: r1.shift_right())
    elif side == 1:
        print("Game Over for Racket 1!")
        break
    elif side == 2:
        print("Game Over for Racket 2!")
        break
    elif side == 3 or side == 4:
        t = 0
    time.sleep(0.01)
print("Total time: %s"%total)
root.mainloop()

