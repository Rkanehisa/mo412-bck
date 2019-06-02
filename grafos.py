#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict 
import sys
import math
import copy

class Graph(): 
    def __init__(self, V): 
        self.V = V 
        self.graph = defaultdict(list)
      
    
    def vertices(self):
        return list(self.graph)
    
    def edges(self):
        return self.graph
    
    def addEdge(self, src, dest, weight):
        newNode = [dest, weight] 
        self.graph[src].insert(0, newNode) 


class Heap(): 
  
    def __init__(self): 
        self.array = [] 
        self.size = 0
        self.pos = [] 
  
    def newMinHeapNode(self, v, dist): 
        minHeapNode = [v, dist] 
        return minHeapNode 
  
    # A utility function to swap two nodes  
    # of min heap. Needed for min heapify 
    def swapMinHeapNode(self,a, b): 
        t = self.array[a] 
        self.array[a] = self.array[b] 
        self.array[b] = t 
  
    # A standard function to heapify at given idx 
    # This function also updates position of nodes  
    # when they are swapped.Position is needed  
    # for decreaseKey() 
    def minHeapify(self, idx): 
        smallest = idx 
        left = 2*idx + 1
        right = 2*idx + 2
  
        if (left < self.size and self.array[left][1] < self.array[smallest][1]): 
            smallest = left 
  
        if (right < self.size and self.array[right][1] < self.array[smallest][1]): 
            smallest = right 
  
        # The nodes to be swapped in min  
        # heap if idx is not smallest 
        if (smallest != idx): 
  
            # Swap positions 
            self.pos[ self.array[smallest][0] ] = idx 
            self.pos[ self.array[idx][0] ] = smallest 
  
            # Swap nodes 
            self.swapMinHeapNode(smallest, idx) 
  
            self.minHeapify(smallest) 
  
    # Standard function to extract minimum  
    # node from heap 
    def extractMin(self): 
  
        # Return NULL wif heap is empty 
        if self.isEmpty() == True: 
            return
  
        # Store the root node 
        root = self.array[0] 
  
        # Replace root node with last node 
        lastNode = self.array[self.size - 1] 
        self.array[0] = lastNode 
  
        # Update position of last node 
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
  
        # Reduce heap size and heapify root 
        self.size -= 1
        self.minHeapify(0) 
  
        return root 
  
    def isEmpty(self): 
        return True if self.size == 0 else False
  
    def decreaseKey(self, v, dist): 
  
        # Get the index of v in  heap array 
  
        i = self.pos[v] 
  
        # Get the node and update its dist value 
        self.array[i][1] = dist 
  
        # Travel up while the complete tree is  
        # not hepified. This is a O(Logn) loop 
        while (i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]): 
  
            # Swap this node with its parent 
            self.pos[ self.array[i][0] ] = (i-1)/2
            self.pos[ self.array[(i-1)//2][0] ] = i 
            self.swapMinHeapNode(i, (i - 1)//2 ) 
  
            # move to parent index 
            i = (i - 1) // 2; 
  
    # A utility function to check if a given  
    # vertex 'v' is in min heap or not 
    def isInMinHeap(self, v):
        if (self.pos[v] < self.size): 
            return True
        return False

def BellmanFord(G, s):
        dist = [sys.maxsize] * G.V
        prev = [None] * G.V
        dist[s] = 0
        prev[s] = s
        
        for l in range(G.V -1):
            for i,j in G.edges().items():
                for k in j:
                    u = i
                    v,w = k
                    if dist[v] != float("Inf") and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                            prev[v] = u
                            
        for i,j in G.edges().items():
                for k in j:
                    u = i
                    v,w = k
                    if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                        return
        return dist,prev

def Johnson(G):
    new_G = Graph(G.V+1)
    V = new_G.V
    new_G.graph = copy.copy(G.graph)
    for i in range(G.V):
        new_G.addEdge(V-1,i,0)
    out = BellmanFord(new_G,V-1)
    dist,path = out
    
    for i,j in new_G.edges().items():
        if(i != V-1):
            for k in j:
                u = i
                v,w = k
                k[1]+=dist[u]-dist[v]
    
    new_G.graph.pop(V-1)
    new_G.V = G.V
    
    distall = [[] for i in range(G.V)]
    prevall = [[] for i in range(G.V)]
    
    for i in range(new_G.V):
        src = i
        dist,path = (dijkstra(new_G,src))
        distall[i] = dist
        prevall[i] = path
    return distall,prevall

def JohnsonFibHeap(G):
    new_G = Graph(G.V+1)
    V = new_G.V
    new_G.graph = copy.copy(G.graph)
    for i in range(G.V):
        new_G.addEdge(V-1,i,0)
    out = BellmanFord(new_G,V-1)
    dist,path = out
    
    for i,j in new_G.edges().items():
        if(i != V-1):
            for k in j:
                u = i
                v,w = k
                k[1]+=dist[u]-dist[v]
    
    new_G.graph.pop(V-1)
    new_G.V = G.V
    
    distall = [[] for i in range(G.V)]
    prevall = [[] for i in range(G.V)]
    
    for i in range(new_G.V):
        src = i
        dist,path = (dijkstraFibHeap(new_G,src))
        distall[i] = dist
        prevall[i] = path
    return distall,prevall

def FloydWarshall(G): 
    V = G.V
    dist = [[sys.maxsize] * V for i in range(V)]
    prox  = [[None] * V for i in range(V)] 
        
    for i,j in G.edges().items():
                for k in j:
                    u = i
                    v,w = k
                    dist[u][v] = w
                    prox[u][v] = u
    
    for i in range(V):
        prox[i][i] = i
        dist[i][i] = 0
    
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if (dist[i][j] > dist[i][k] + dist[k][j]):
                    dist[i][j] = dist[i][k]+ dist[k][j]
                    prox[i][j] = prox[k][j]
    return dist,prox

def dijkstra(G,s):
        V = G.V
        dist = []
        heap = Heap() 
        prev = []
        
        for v in range(V):
            dist.append(sys.maxsize)
            prev.append(None)
            heap.array.append(heap.newMinHeapNode(v, dist[v]) ) 
            heap.pos.append(v) 

        heap.pos[s] = s
        dist[s] = 0
        prev[s] = s
        heap.decreaseKey(s, dist[s])
        
        heap.size = V;
        
        while heap.isEmpty() == False:
            current = heap.extractMin()  
            u = current[0]
            for pCrawl in G.graph[u]: 
                v = pCrawl[0]
                if (dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]): 
                        dist[v] = pCrawl[1] + dist[u]
                        heap.decreaseKey(v, dist[v]) 
                        prev[v]= u 
                        
        return dist,prev

def dijkstraFibHeap(G,s):
    V = G.V
    visited = [False]*V
    dist = [float(sys.maxsize)] * V
    prev = [None]*V
    heapNodes = [None]*V
    
    
    heap = FibonacciHeap(V)
    for i in range(V):
        heapNodes[i] = heap.insertion(float('inf'),i)
    
    dist[s] = 0
    prev[s] = s
    heap.decrease_key(heapNodes[s],0)
    i = 0
    while heap.total_nodes > 0:
        current = heap.extract_min().pos
        u = current
        for pCrawl in G.graph[u]: 
            v = pCrawl[0]
            if (dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]): 
                dist[v] = pCrawl[1] + dist[u]
                heap.decrease_key(heapNodes[v], dist[v]) 
                prev[v]= u
    return dist,prev

class HeapNode():
        def __init__(self, key,pos):
            self.key = key
            self.pos = pos
            self.child = None
            self.parent = None
            self.next = self.prev = None
            self.degree = 0
            self.mark = False
            
    

class FibonacciHeap():
    def __init__(self,V):
        
        self.total_nodes = 0
        self.pos = [None for i in range(V)]
        self.min = None
        
    def insertion(self,key,pos):
        new_node = HeapNode(key,pos)
        new_node.next = new_node
        new_node.prev = new_node
        self.insert_on_root(new_node)
        self.pos[pos] = new_node
        self.total_nodes += 1
        return new_node
    
    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
        node = node.next
    
    def insert_on_root(self,x):
        x.parent = None
        if(self.min != None):
            z = self.min
            x.prev = z
            x.next = z.next
            z.next.prev = x
            z.next = x
        else:
            self.min = x
             
    def remove_from_root(self,x):
        if (x == self.min):
            self.min = x.next
        x.next.prev = x.prev
        x.prev.next = x.next
        
    def extract_min(self):
        z = self.min
        if(z != None):
            if (z.child != None):
                nodes = [w for w in self.iterate(z.child)]
                for x in range(0, len(nodes)):
                    self.insert_on_root(x)
                    x.parent = None
            self.remove_from_root(z)
            if (self.total_nodes ==0):
                self.min = None
            else:
                self.consolidate()
            self.total_nodes -= 1
        return z
    
    
    def consolidate(self):
        golden_ratio = int(math.log(self.total_nodes,1.6810))
        golden_ratio += 1
        A = [None for i in range(self.total_nodes)]
        for i in range(golden_ratio):
            A[i] = None
        w = self.min
        nodes = [w for w in self.iterate(self.min)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while(A[d] != None):
                y = A[d]
                if(x.key > y.key):
                    x,y = y,x
                self.fibonacciLink(y,x)
                A[d] = None
                d += 1
            A[d] = x
            
        self.min = None
        for i in range(len(A)):
            if(A[i] != None):
                self.insert_on_root(A[i])
                if(self.min == None or self.min.key < A[i].key):
                    self.min = A[i]
    
    
    def fibonacciLink(self,x,y):
        self.remove_from_root(x)
        self.insert_on_child(y,x)
        y.mark = False
    
    def insert_on_child(self,x,y):
        x.parent = y
        if(y.child == None):
            y.child = x
        else:
            x.next = y.child.next
            x.prev = y.child
            y.child.next.prev = x
            y.child.next = x
        y.degree+=1
        
    def remove_from_child(self,x,y):
        if(y.child == y.child.next):
            y.child = None
        elif y.child == x:
            y.child = x.next
            y.next.parent = y
        x.prev.next = x.next
        x.next.prev = x.prev
        
    def printRoots(self,x):
        z = x
        if(z == None):
            print("Empty")
        else:
            tmp = z
            while(True):
                print("pos=%d key=%f next=%d" % (tmp.pos,tmp.key,tmp.next.pos))
                tmp = tmp.next
                if(tmp == z):
                    break
            print()
    
    
    def decrease_key(self,x,key):
        if(x.key > key):
            x.key = key
            y = x.parent
            if(y != None and x.key < y.key):
                self.cut(x,y)
                self.cascade_cut(y)
            if(x.key < self.min.key):
                self.min = x
    
    def cut(self,x,y):
        self.insert_on_root(x)
        self.remove_from_child(x,y)
        y.degree -=1
        x.parent = None
        x.mark = False
        
        
    def cascade_cut(self,y):
        z = y.parent
        if(z != None):
            if(y.mark == False):
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

def getPath(prev,s):
    path = [[] for i in range(len(prev))]   
    for i in range(len(prev)):
        path[i].append(i)
        curr = prev[i]
        while True:
            if(curr == s):
                break
            path[i].append(curr)
            if(curr != None):
                curr = prev[curr]
            else:
                break
    return path

def printPath(src,dist,prev):
    paths = getPath(prev,src)
    
    for i in range(0,len(dist)):
        if(dist[i] < sys.maxsize):
            print("%d" % dist[i],end="")
            print(" v%d " % (src),end="")
            for j in paths[i][::-1]:
                print("v%d " % j, end="")
            print(i)
        else:
            print("Inf v%d v%d %d" % (src,i,i))