import random
class Rectangle:
    def __init__(self,canvas,x0,y0,x,y):
        self.x0=x0
        self.y0=y0
        self.x=x
        self.y=y
        self.color=random.choice(["Blue","Red"])
        self.rect=canvas.create_rectangle(x0,y0,x0+x,y0+y,fill=self.color,outline=self.color)
        self.c=canvas
    def update_color(self):
        self.color=random.choice(["Blue","Red"])
        self.c.itemconfig(self.rect,fill=self.color,outline=self.color)
