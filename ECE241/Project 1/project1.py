"""
UMass ECE 241 - Advanced Programming
Project #1   Fall 2021
project1.py - Sorting and Searching

"""

import matplotlib.pyplot as plt
import time
import random
"""
Tree Node Class
"""
class TreeNode:
    def __init__(self,key,val,left=None,right=None,parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = 0

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

"""
AVL Class
"""
class AvlTree:
    def put(self,key,val):
        if self.bst:
            self._put(key, val, self.bst)
        else:
            self.bst = TreeNode(key, val)

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.bst = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(
            newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(
            rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.bst = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(
            newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(
            rotRoot.balanceFactor, 0)
    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)

"""
Stock class for stock objects
"""
class Stock:

    """
    Constructor to initialize the stock object
    """
    def __init__(self,sname,symbol,val,prices):
        self.sname = sname
        self.symbol = symbol
        self.val = round(float(val),1)
        self.prices = prices


    """
    return the stock information as a string, including name, symbol, 
    market value, and the price on the last day (2021-02-01). 
    For example, the string of the first stock should be returned as: 
    “name: Exxon Mobil Corporation; symbol: XOM; val: 384845.80; price:44.84”. 
    """
    def __str__(self):
        return "name: %s; symbol: %s; val: %s; price:%s"%(self.sname,self.symbol,self.val,self.prices)


"""
StockLibrary class to mange stock objects
"""
class StockLibrary(AvlTree):

    """
    Constructor to initialize the StockLibrary
    """
    def __init__(self):
        self.bst = None
        self.stockList = []
        self.size = None
        self.isSorted = False


    """
    The loadData method takes the file name of the input dataset,
    and stores the data of stocks into the library. 
    Make sure the order of the stocks is the same as the one in the input file. 
    """
    def loadData(self, filename: str):
        file = open(filename,'r')
        for i in file:
            line = i.strip("\n").split("|")
            if line[1]!= "Symbol":
                self.stockList.append(Stock(line[0],line[1],line[2],line[len(line)-1]))
            else:
                self.header = line[3:]
        self.size = len(self.stockList)





    """
    The linearSearch method searches the stocks based on sname or symbol.
    It takes two arguments as the string for search and an attribute field 
    that we want to search (“name” or “symbol”). 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def linearSearch(self, query: str, attribute: str):
        #tstart = time.time()
        found = False
        for i in self.stockList:
            if i.sname == query or i.symbol == query:
                item=i
                found = True
        if found:
            return item
            #return time.time()-tstart
        else:
            return "Stock not found"
            #return time.time()-tstart


    """
    Sort the stockList using QuickSort algorithm based on the stock symbol.
    The sorted array should be stored in the same stockList.
    Remember to change the isSorted variable after sorted
    """
    def quickSort(self):
        self.quickSortHelper(self.stockList,0,self.size-1)
        self.isSorted = True
    def quickSortHelper(self,alist, first, last):
        if first < last:
            splitpoint = self.partition(alist,first,last)

            self.quickSortHelper(alist, first, splitpoint - 1)
            self.quickSortHelper(alist, splitpoint + 1, last)

    def partition(self,alist, first, last):
        pivotvalue = alist[first].symbol

        leftmark = first + 1
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and alist[leftmark].symbol <= pivotvalue:
                leftmark = leftmark + 1

            while alist[rightmark].symbol >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else:
                temp = alist[leftmark]
                alist[leftmark] = alist[rightmark]
                alist[rightmark] = temp

        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp

        return rightmark
    """
    build a balanced BST of the stocks based on the symbol. 
    Store the root of the BST as attribute bst, which is a TreeNode type.
    """
    def buildBST(self):
        #tstart = time.time()
        self.quickSort()
        for i in self.stockList:
            self.put(i.symbol,i)
            #print(self.bst.rightChild.payload.symbol,self.bst.leftChild.payload.symbol,self.bst.balanceFactor)
        #return time.time()-tstart


    #def buildBSThelper(self,current,node):
     #       if current.key > node.key:
      #          if current.hasRightChild():
       #             self.buildBSThelper(current.rightChild, node)
        #        else:
         #           current.rightChild = node
          #          node.parent = current
           #         self.updateBalance(node)
            #elif current.key < node.key:
             #   if current.hasLeftChild():
              #      self.buildBSThelper(current.leftChild, node)
               # else:
                #    current.leftChild = node
                 #   node.parent = current
                  #  self.updateBalance(node)


    """
    Search a stock based on the symbol attribute. 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def searchBST(self, query, current='dnode'):
        #tstart = time.time()
        start = self.bst
        while start.payload.symbol != query and start.hasAnyChildren():
            if query>start.payload.symbol:
                start = start.rightChild
            elif query < start.payload.symbol:
                start = start.leftChild
        if start.payload.symbol == query:
            #return time.time()-tstart
            return start.payload
        else:
            #return time.time() - tstart
            return "Stock not found"



# WRITE YOUR OWN TEST UNDER THIS IF YOU NEED
if __name__ == '__main__':
    random.seed(5)
    stockLib = StockLibrary()
    testSymbol = ["GE"]

    print("\n-------load dataset-------")
    stockLib.loadData("stock_database.csv")
    print(stockLib.size)

    print("\n-------linear search-------")
    t = 0
    t2 = 0

    #for i in range(100):
        #num = random.randint(0, stockLib.size - 1)
       # testSymbol = testSymbol+[stockLib.stockList[num].symbol]
        #testName = stockLib.stockList[num].sname
    #for j in testSymbol:
       # t =t + stockLib.linearSearch(str(testSymbol), "symbol")
   # print(t/100)
    #print(stockLib.linearSearch(testName, "name"))


    print("\n-------quick sort-------")
    print(stockLib.isSorted)
    stockLib.quickSort()
    print(stockLib.isSorted)

    print("\n-------build BST-------")
    t3 = stockLib.buildBST()
    print(t3)
    print(stockLib.bst.balanceFactor)
    print("\n---------search BST---------")
    #for i in testSymbol:
     #   t2 = t2 + stockLib.searchBST(str(testSymbol))
    print(t2/100)
    max = 0
    #for i in stockLib.stockList:
        #for j in range(len(i.prices)):
            #if j != 0:
                #change = abs(float(i.prices[j-1])-float(i.prices[j]))/float(i.prices[j-1])
                #if change > max:
                    #max = change
                    #stock = i
    #print(max,stock)


    #max = 0
    #for i in stockLib.stockList:
     #   if len(i.sname) > max:
      #      max = len(i.sname)
       #     stock = i
    #plt.plot(stockLib.header,stock.prices)
   # plt.title(stock.sname)
    #plt.xlabel("Dates")
    #plt.ylabel("Market Value (in millions)")
    #plt.xticks(rotation = 45)
    #plt.show()





