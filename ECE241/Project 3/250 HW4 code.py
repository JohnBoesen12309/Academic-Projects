import numpy as np


class queens:
    def __init__(self,show):
        self.size = 8
        self.num_s = 0
        self.show = show
        self.place([-1]*self.size, 0)
        print("There are", self.num_s, "solutions")


    def place(self, p, target): # Place queens
        if target == self.size: #Stop if off of the board
            self.num_s += 1
            self.board(p)

        else:
            for i in range(self.size):
                if self.check(p, target, i):
                    p[target] = i
                    self.place(p, target + 1)


    def check(self, p, taken, c): #check to see if spot is taken
        for i in range(taken):
            if p[i] == c or p[i] - i == c - taken or p[i] + i == c + taken:
                return False
        return True


    def board(self, p): #Display board
        if self.show == "1":
            print("  1|2|3|4|5|6|7|8")
        sol = []
        for row in range(self.size):
            line = ""
            for column in range(self.size):
                if p[row] == column:
                    line += "+ "
                    sol.append((column+1,row+1))
                else:
                    line += ". "
            if self.show == "1":
                print(row+1,line)
        print("\n",sol,"\n")


if __name__ == "__main__":
    # show= input("Show board:")
    show = "0"
    queens(show)