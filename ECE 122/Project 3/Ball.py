from Mapping_for_Tkinter import Mapping_for_Tkinter
from tkinter import *
import math
import time
import random

class Ball:
    def __init__(self,map,canvas,x0,y0,velocity,angle):
        self.bool1=False
        self.m=map
        self.c=canvas
        self.x0=x0
        self.y0=y0
        self.v=float(velocity)
        self.theta=float(angle)*(math.pi/180)
        self.r=map.get_width()/120
        self.ball=canvas.create_oval(map.get_i(x0)-self.r,map.get_j(y0)+self.r,map.get_i(x0)+self.r,map.get_j(y0)-self.r,fill="blue",outline="blue")
    def update_xy(self,t,r1=None,r2=None):
        """Changes the position of the ball with time and rebounds off of edges"""
        x = self.x0 + self.v * t * math.cos(self.theta)
        y = self.y0 + self.v * t * math.sin(self.theta)
        j = self.m.get_j(y)
        i = self.m.get_i(x)
        self.x=x
        self.y=y
        self.c.coords(self.ball,i-self.r,j+self.r,i+self.r,j-self.r)
        if r2 and self.y>=self.m.get_y(r2.spy)-self.r and r2.ls <= self.m.get_i(self.x) <= r2.rs: ## checks if the ball hits racket2
            self.y0 = self.m.get_y(r2.spy) - self.r
            self.x0 = self.x
            self.theta = random.uniform(-170, -10) * math.pi / 180
            return 6
        elif r1 and self.y<=self.m.get_y(r1.top)+self.r and r1.ls<=self.m.get_i(self.x)<=r1.rs: ## checks if the ball hits racket1
            self.y0=self.m.get_y(r1.top)+self.r+1
            self.x0=self.x
            self.theta=-1*self.theta
            return 5
        elif x>=self.m.get_xmax()-self.r: ##Checks if ball has hit the right boundary
            self.theta=math.pi-self.theta
            self.x0=x
            self.y0=y
            return 4
        elif x<=self.m.get_xmin()+self.r: ##Checks if ball hits the left boundary
            self.theta=math.pi-self.theta
            self.x0=x
            self.y0=y
            return 3
        elif y>self.m.get_ymax()-self.r: ##Checks if ball hits top boundary
            self.theta=random.uniform(-170,-10)*math.pi/180
            self.y0=self.m.get_ymax()-self.r
            self.x0=x
            return 2
        elif y<=self.m.get_ymin()+self.r: ##Checks if ball hits bottom boundary
            self.theta=-1*self.theta
            self.y0=y
            self.x0=x
            return 1
        else:
            return 0
    def bool2(self):
        """Allows for the breaking of a loop from a button press"""
        self.bool1=True

    def pointer(self):
        """Creates a pointer to show the angle of release"""
        self.bool1=False
        x = 20
        y = 20
        r = 20
        N = 200
        xcenter = x - r
        ycenter = x - r
        theta1 = (4 * math.pi) / (3 * N)
        theta = math.pi / 6
        line = self.c.create_line(self.m.get_i(self.x0), self.m.get_j(self.y0), self.m.get_i(self.x0 + x), self.m.get_j(self.y0 + y))
        self.c.bind("<Button-1>",lambda e: self.bool2())##Work around for getting break to bind to a click
        self.c.bind("<Button-3>",lambda e: self.bool2())
        while True: #Makes the line move in a circular manner
            if self.bool1==True:
                break
            for n in range(N):
                if self.bool1==True:
                    self.theta=theta
                    break
                if n <= N / 2:
                    theta = theta + theta1
                else:
                    theta = theta - theta1
                x = r * math.cos(theta) + xcenter
                y = r * math.sin(theta) + ycenter
                self.c.coords(line, self.m.get_i(self.x0), self.m.get_j(self.y0), self.m.get_i(self.x0 + x), self.m.get_j(self.y0 + y))
                self.c.update()
                time.sleep(0.01)
        self.c.delete(line)



    """ to complete """
    

def main(): 
        ##### create a mapping
        swidth=input("Enter window size in pixels (press Enter for default 600): ")
        if swidth=="":
            width=600
        else:
            width=int(swidth)
        m = Mapping_for_Tkinter(-1 * width/2, width/2, -1 * width/2, width/2, width)
        
        ##### User Input 
        data=input("Enter velocity and theta (press Enter for default: 500 pixel/s and 30 degree):")
        if data=="":
            velocity=500
            angle=30
        else:
            velocity,angle=data.split()
        

        
        ##### create a window, canvas and ball object
        root = Tk()
        canvas = Canvas(root, width=m.get_width(), height=m.get_height(), bg="white")
        canvas.pack()
        ball=Ball(m,canvas,0,0,velocity,angle)


           
        ############################################
        ####### start simulation
        ############################################
        t=0               # real time between event
        t_total=0         # real total time
        count=0           # rebound_total=0
        while True:
            t=t+0.01 #real time between events- in second
            t_total=t_total+0.01 #real total time- in second
            side=ball.update_xy(t)# Update ball position and return collision event
            root.update()   # update the graphic (redraw)
            if side!=0:
                count=count+1 # increment the number of rebounds
                t=0 # reinitialize the local time
            time.sleep(0.01)  # wait 0.01 second (simulation time)
            if count==10: break # stop the simulation
            
        print("Total time: %ss"%t_total)
        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

