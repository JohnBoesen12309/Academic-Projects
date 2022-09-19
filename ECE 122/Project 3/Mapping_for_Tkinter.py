from tkinter import *


class Mapping_for_Tkinter:
    def __init__(self,xmin,xmax,ymin,ymax,width):
        self.set_width(width)
        self.set_xmin(xmin)
        self.set_xmax(xmax,width,ymin,ymax)
        self.set_ymin(ymin)
        self.set_ymax(ymax)
        self.__set_height(width,xmin,xmax,ymin,ymax)
    def set_width (self,width):
        self.__width=width
    def set_xmin(self,xmin):
        self.__xmin=xmin
    def set_xmax(self,xmax,width,ymin,ymax):
        while xmax<=self.__xmin:
            xmin,xmax=input("Your xmax is invalid (xmax<=xmin), Re-Enter correct [xmin,xmax]: ").split()
            while xmin=="" or xmax == "":
                xmin,xmax=input("Your input is invalid (No input), Re-Enter correct [xmin,xmax]: ")
            xmin=float(xmin)
            xmax=float(xmax)
            self.__xmin=xmin
            self.__set_height(width,xmin,xmax,ymin,ymax)
        self.__xmax=xmax
    def set_ymin(self,ymin):
        self.__ymin=ymin
    def set_ymax(self,ymax):
        while ymax<=self.__ymin:
            ymin,ymax=input("Your ymax is invalid (ymax<=ymin), Re-Enter correct [ymin,ymax]: ").split()
            while ymin=="" or ymax=="":
                ymin,ymax=input("Your input is invalid(No input), Re-Enter correct [ymin,ymax]")
            ymin=float(ymin)
            ymax=float(ymax)
            self.__ymin=ymin
            self.__set_height(self.__width,self.__xmin,self.__xmax,ymin,ymax)
        self.__ymax=float(ymax)
    def __set_height(self,width,xmin,xmax,ymin,ymax):
        self.__height=width*((ymax-ymin)/(xmax-xmin))
    def get_width(self):
        return self.__width
    def get_xmin(self):
        return self.__xmin
    def get_xmax(self):
        return self.__xmax
    def get_ymin(self):
        return self.__ymin
    def get_ymax(self):
        return self.__ymax
    def get_height(self):
        return self.__height
    def get_x(self,i):
        return float(self.__xmin+i*(self.__xmax-self.__xmin)/(self.__width-1))
    def get_i(self,x):
        return float((self.__width-1)*(x-self.__xmin)/(self.__xmax-self.__xmin))
    def get_y(self,j):
        return float(self.__ymax-j*(self.__ymax-self.__ymin)/(self.__height-1))
    def get_j(self,y):
        return float((self.__ymax-y)*(self.__height-1)/(self.__ymax-self.__ymin))
    def __str__(self):
        return "%s %s %s %s %s %s"%(self.__xmin,self.__xmax,self.__ymin,self.__ymax,self.__width,self.__height)


""" to complete"""
def main(): 
    """ TESTING MAPPING using FUNCTION PLOTTER """

    #### formula input
    formula=input("Enter math formula (using x variable): ")

    #### coordinate input
    coord=input("Enter xmin,xmax,ymin,ymax (press Enter for default -5,5,-5,5): ")
    if coord=="":
        xmin,xmax=-5,5
        ymin,ymax=-5,5
    else:
        #split the string/create list of string
        xmin,xmax,ymin,ymax=coord.split()

    #### instantiate a mapping
    width=800
    m=Mapping_for_Tkinter(float(xmin),float(xmax),float(ymin),float(ymax),width) 
    print(m) # print info about object

    #### instantiate a tkinter window 
    window = Tk() 
    canvas = Canvas(window, width=m.get_width(),height=m.get_height(),bg="white") # create a canvas width*height
    canvas.pack()

    #### create axis
    if m.get_xmin()<0 and m.get_xmax()>0:
        canvas.create_line(m.get_i(0.0),m.get_j(m.get_ymin()),m.get_i(0.0),m.get_j(m.get_ymax()))
    if m.get_ymin()<0 and m.get_ymax()>0:
        canvas.create_line(m.get_i(m.get_xmin()),m.get_j(0.0),m.get_i(m.get_xmax()),m.get_j(0.0))
    
    #### plot function    
    for i in range(width):
        x=m.get_x(i)
        y=eval(formula)
        canvas.create_rectangle((m.get_i(x),m.get_j(y))*2,outline="blue")

    window.mainloop() # wait until the window is closed



if __name__=="__main__":
    main()
