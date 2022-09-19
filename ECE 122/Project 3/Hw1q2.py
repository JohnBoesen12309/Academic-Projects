class hw1q2:
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c
    def Mono(self):
        x=(2*self.b+self.c)/self.a
        return x
    def Poly(self):
        x=(self.c**2-2*self.b)
        return x

if __name__=="__main__":
    a,b,c=input("Please input a,b,c: ").split(",")
    inp=hw1q2(int(a),int(b),int(c))
    formNum=int(input("1: ax-2b=c    2: sqrt(ax+2b)=c: "))
    if formNum==1:
        print(inp.Mono())
    elif formNum==2:
        print(inp.Poly())
    else:
        while formNum!=1 or formNum!=2:
            formNum=int(input("1: ax-2b=c    2: sqrt(ax+2b)=c"))