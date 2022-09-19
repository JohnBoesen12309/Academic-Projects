from Graph import *
import random
from BFS import bfs,traverse
Weight = float

class ISPNetwork:

    def __init__(self):
        self.network = Graph()
        self.MST = Graph()

    def buildGraph(self, filename):
        f = open(filename,'r')
        for i in f:
            line=i.strip("\n").split(",")
            self.network.addEdge(line[0],line[1],float(line[2]))
            self.network.addEdge(line[1],line[0],float(line[2]))

    def pathExist(self, router1, router2):
        if router2 ==None or router1 ==None:
            return False
        router1 = self.network.getVertex(router1) # Get the router nodes
        router2 = self.network.getVertex(router2)


        for i in self.network.vertList.values(): #Reset all node colors to white to properly search the graph
            if i.color != 'white':
                i.color = 'white'

        bfs(self.network,router1)
        try: #Attepmt to look for None cases or other outliers
            if traverse(router2) == router1.getId():
                return True
            else:
                return False
        except:
            return False

    def buildMST(self):

        notVisited = list(self.network.vertList.values())
        notVisited.sort(key=Vertex.getId)
        visited=[notVisited.pop(0)]
        # reset distance and Pred
        for vert in notVisited:
            vert.setDistance(sys.maxsize)
            vert.setPred(None)
        minEdge=None

        while len(notVisited) != 0:
            connections = []
            # find the next connection, must not be visited and have the least weight
            for visited_vert in visited:
                for vert in visited_vert.getConnections():
                    if vert not in visited:
                        connections.append((visited_vert,vert,visited_vert.getWeight(vert)))
            minCost=sys.maxsize

            #look through connections to find the least cost path
            for edgePack in connections:
                if edgePack[2] < minCost:
                    minEdge=edgePack
                    minCost=edgePack[2]

            #Move node from notVisited to visited and build graph
            notVisited.remove(minEdge[1])
            visited.append(minEdge[1])
            self.MST.addEdge(minEdge[0],minEdge[1],minEdge[2])
            self.MST.addEdge(minEdge[1],minEdge[0],minEdge[2])


    def findPath(self, router1, router2):
        current = self.MST.getVertex(router1)
        router2 = self.MST.getVertex(router2)
        output = ""
        found = False

        #Traverse MST to find path
        while not found and current.getPred():
            if current == router2:
                found = True
            else:
                #build the path output and move to next node
                output += current.id + " -> "
                current = current.getPred()
        if not found:
            return "path doesn't exist"
        else:
            return output +router2.id


    def findForwardingPath(self, router1, router2):
        #check to make sure there is a path
        if self.pathExist(router1,router2):
            router1 = self.network.getVertex(router1)
            router2 = self.network.getVertex(router2)

            #reset dist value

            for i in self.network.vertList.values():
                if i.dist != sys.maxsize:
                    i.dist = sys.maxsize
                i.setPred(None)
            self.network.dijkstra(router2)
            current = router1
            nodes = ""
            #Traverse graph to return path
            while current.getPred():
                nodes = nodes + current.getId() + " -> "
                current = current.getPred()
            return nodes+router2.getId()+"(%s)"%float(router1.getDistance())
        else:
            return "path not exist"

    def findPathMaxWeight(self, router1, router2):
        #checks to make sure that there is a path
        if self.pathExist(router1,router2):
            router1 = self.network.getVertex(router1)
            router2 = self.network.getVertex(router2)

            #Reset dist
            for i in self.network.vertList.values():
                if i.dist != sys.maxsize:
                    i.dist = sys.maxsize

            #beginning of  modified dijkstras
            pq = PriorityQueue()
            router2.setDistance(0)
            pq.buildHeap([(v.getDistance(), v) for v in self.network])
            while not pq.isEmpty():
                maxdist = [] #stores weights
                currentVert = pq.delMin()
                for nextVert in currentVert.getConnections():
                    newDist = currentVert.getDistance() \
                              + float(currentVert.getWeight(nextVert))
                    maxdist.append(float(currentVert.getWeight(nextVert)))
                    if max(maxdist) < nextVert.getDistance(): #determines the lowest maximum
                        nextVert.setDistance(newDist)
                        nextVert.setPred(currentVert)
                        pq.decreaseKey(nextVert, newDist)

            #beginning at attempt to traverse the graph to showcase path
            current = router1
            nodes=""
            #Wasn't able to finish, gives infinite loop
            #while current.getPred():
              #  nodes = nodes + current.getId() + " -> "
              #  current = current.getPred()
            #return nodes + router2.getId()

        else:
            return "path not exist"



    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([ISPNetwork.nodeEdgeWeight(v) for v in g]) // 2


if __name__ == '__main__':
    print("--------- Task1 build graph ---------")
    # Note: You should try all six dataset. This is just a example using 1221.csv
    net = ISPNetwork()
    net.buildGraph('Book1.csv')

    print("--------- Task2 check if path exists ---------")
    routers = [v.id for v in random.sample(list(net.network.vertList.values()), 5)]
    for i in range(4):
        print('Router1:', routers[i], ', Router2:', routers[i+1], 'path exist?:', net.pathExist(routers[i], routers[i+1]))

    print("--------- Task3 build MST ---------")
    #net.buildMST()
   # print('graph node size', net.MST.numVertices)
   # print('graph total edge weights', net.totalEdgeWeight(net.MST))

    print("--------- Task4 find shortest path in MST ---------")
   # for i in range(4):
    #    print(routers[i], routers[i+1], 'Path:', net.findPath(routers[i], routers[i+1]))

    print("--------- Task5 find shortest path in original graph ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findForwardingPath(routers[i], routers[i+1]))

    print("--------- Task6 find path in LowestMaxWeightFirst algorithm ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPathMaxWeight(routers[i], routers[i+1]))
