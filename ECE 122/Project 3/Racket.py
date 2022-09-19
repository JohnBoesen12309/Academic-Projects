from Mapping_for_Tkinter import Mapping_for_Tkinter
from tkinter import *


class Racket:
    def __init__(self, mapping, canvas, length, width,positionx=None,positiony=None):

        self.Lx=length/2 #Length from center of racket
        self.Ly=width
        self.c=canvas
        self.m=mapping
        jmin = mapping.get_j(mapping.get_ymin()) #Bottom border of window
        icenter = mapping.get_i(0.0)
        self.top=jmin-width #top of racket
        self.ls=icenter-(length/2)
        self.rs=icenter+(length/2)
        if positionx and positiony: #Allows for making a racket outside of the standard start postion
            self.spx=positionx
            self.spy=positiony+width
            self.racket = canvas.create_rectangle(self.ls+self.spx,self.spy-width, self.rs+self.spx,self.spy, fill="black")
        else:
            self.racket=canvas.create_rectangle(self.ls,self.top,self.rs,jmin,fill="black")
    def shift_left(self):
        """Moves racket to the left"""
        if self.ls > self.m.get_i(self.m.get_xmin()):#Moves until left border is hit
            self.ls=self.ls-(self.Lx)
            self.rs=self.rs-(self.Lx)
            self.c.move(self.racket,-1*self.Lx,0)
            self.c.update()
    def shift_right(self):
        """Moves racket to the right"""
        if self.rs < self.m.get_i(self.m.get_xmax()):#Moves until right border is hit
            self.ls=self.ls+(self.Lx)
            self.rs=self.rs+(self.Lx)
            self.c.move(self.racket,self.Lx,0)


def main():
    ###### create a mapping
    swidth = input("Enter window size in pixels (press Enter for default 600): ")
    if swidth == "":
        width = 600
    else:
        width = int(swidth)
    m=Mapping_for_Tkinter(-1*width/2,width/2,-1*width/2,width/2,width)

    ##### create a window, canvas, and racket
    root=Tk()
    canvas=Canvas(root,width=m.get_width(),height=m.get_height(),bg="white")
    canvas.pack()
    racket=Racket(m,canvas,width/10,width/60)

    ####### bind mouse click with action
    canvas.bind("<Button-1>",lambda e:racket.shift_left())
    canvas.bind("<Button-3>",lambda e:racket.shift_right())

    canvas.mainloop()
if __name__ == "__main__":
    main()
