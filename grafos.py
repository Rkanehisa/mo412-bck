#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict 
import sys
import math
import copy
from fibHeap import FibonacciHeap
from binaryHeap import Heap

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

def dijkstraArray(G, src):  
    dist = [sys.maxsize] * G.V 
    prev = [None] * G.V 
    dist[src] = 0
    prev[src] = src
    visited = [False] * G.V 

    for i in range(G.V):
        u = extract_min(dist,visited)
        if(u != -1):
            visited[u] = True
            for k in G.graph[u]:
                v,w = k
                if (visited[v] == False and dist[v] != float("Inf") and dist[u] + w < dist[v]):
                    dist[v] = dist[u] + w
                    prev[v] = prev[u]
    return dist,prev

def DijkstraBinary(G,s):
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

def DijkstraFibHeap(G,s):
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

def JohnsonArray(G):
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
        dist,path = (dijkstraArray(new_G,src))
        distall[i] = dist
        prevall[i] = path
    return distall,prevall

def JohnsonBinary(G):
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
        dist,path = (DijkstraBinary(new_G,src))
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
        dist,path = (DijkstraFibHeap(new_G,src))
        distall[i] = dist
        prevall[i] = path
    return distall,prevall