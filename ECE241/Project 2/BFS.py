from Graph import Graph, Vertex
from pythonds.basic import Queue

def bfs(g,start):
  if start ==None:
      return
  start.setDistance(0)
  start.setPred(None)
  vertQueue = Queue()
  vertQueue.enqueue(start)
  while (vertQueue.size() > 0):
    currentVert = vertQueue.dequeue()
    if currentVert==None:
        pass
    for nbr in currentVert.getConnections():
      if nbr == None:
          pass
      if (nbr.getColor() == 'white'):
        nbr.setColor('gray')
        nbr.setDistance(currentVert.getDistance() + 1)
        nbr.setPred(currentVert)
        vertQueue.enqueue(nbr)
    currentVert.setColor('black')
    #print(currentVert)  # prints the status of the current visited vertex

def traverse(y):
    if y == None:
        return None
    x = y
    while x.getPred()!=None:
        #print(x.getId())
        x = x.getPred()
    if x==None:
        return False
    return x.getId()