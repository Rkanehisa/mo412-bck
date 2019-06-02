from collections import defaultdict 
import sys
import math
import copy

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


def extract_min(dist, visited):
    minimum = sys.maxsize
    min_index = -1
    for v in range(len(dist)):
        if (dist[v] < minimum and visited[v] == False):
            minimum = dist[v] 
            min_index = v
    return min_index