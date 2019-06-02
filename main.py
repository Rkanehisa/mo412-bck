import grafos
import sys

def Dijsktra(G,src):
    dist,path = grafos.dijkstra(G,src)
    return dist,path

def DijkstraFibHeap(G,src):
    dist,path = grafos.dijkstraFibHeap(G,src)
    return dist,path

def BellmanFord(G,src):
    out = grafos.BellmanFord(G,src)
    if(out != None):
        dist,path = out
        return dist,path
    else:
        print("Ciclo negativo")
        return None


def FloydWarshall(G):
    dist,prox = grafos.FloydWarshall(G)
    return dist,prox



def JohnsonBinary(G):
    dist,prox = grafos.JohnsonBinary(G)
    return dist,prox
    
def JohnsonFibHeap(G):
    dist,prox = grafos.JohnsonFibHeap(G)
    return dist,prox

def inputfile(in_file):
    f = open(in_file, "r")
    a = f.read()
    b = a.split('\n')
    G = grafos.Graph(int(b[0]))
    print(b[2])
    src = (int(b[2]))
    for i in range(3,len(b)):
        tmp = b[i].split(" ")
        G.addEdge(int(tmp[0]),int(tmp[1]),float(tmp[2]))
    return G,src


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

def printPath(src,dist,prev,out_file):
    paths = getPath(prev,src)
    
    for i in range(0,len(dist)):
        if(dist[i] < sys.maxsize):
            print("%d" % dist[i],end="",file=out_file)
            print(" v%d " % (src),end="",file=out_file)
            for j in paths[i][::-1]:
                print("v%d " % j, end="",file=out_file)
            print(i,file=out_file)
        else:
            print("Inf v%d v%d %d" % (src,i,i),file=out_file)


def main(alg,version,in_file,out_file):
    try:
        graph,src = inputfile(in_file)
    except:
        print("Invalid input file")
        return

    try:
        out = open(out_file,"w")
    except:
        print("Invalid output file")

    if(alg.lower() == "dijkstra"):
        if(version == 0):
            print("Dijkstra with array Heap")
            dist,prev = DijsktraArray(graph,src)
            printPath(src,dist,prev,out)

        elif(version == 1):
            print("Dijkstra with binary Heap")
            dist,prev =  DijkstraBinary(graph,src)
            printPath(src,dist,prev,out)

        elif(version == 2):
            print("Dijkstra with Fibonacci Heap")
            dist,prev = DijkstraFibHeap(graph,src)
            printPath(src,dist,prev,out)



    elif(alg.lower() == "bellman-ford"):
        print("Bellman Ford")
        dist,prev = BellmanFord(graph,src)
        printPath(src,dist,prev,out)


    elif(alg.lower() == "floyd-warshall"):
        print("Floyd-Warshal")
        dist,prev = FloydWarshall(graph)
        for i in range(len(prev)):
            printPath(i,dist[i],prev[i],out)



    elif(alg.lower() == "johnson"):
        if(version == 0):
            print("Johnson with Array Heap")
            dist,prev = JohnsonArray(graph)
            for i in range(len(prev)):
                printPath(i,dist[i],prev[i],out)
        elif(version == 1):
            print("Johnson with Binary Heap")
            dist,prev = JohnsonBinary(graph)
            for i in range(len(prev)):
                printPath(i,dist[i],prev[i],out)
        elif(version == 2):
            print("Johnson with Fibonacci Heap")
            dist,prev = JohnsonFibHeap(graph)
            for i in range(len(prev)):
                printPath(i,dist[i],prev[i],out)
    else:
        print("Usage <algorithm> <version> <input_file> <output_file>") 
        return
    

    out.close


if __name__== "__main__":
    if(len(sys.argv) == 5):
        alg,version,in_file,out_file = sys.argv[1:]    
        main(alg,int(version),in_file,out_file)
    #except:
    #    print("Usage <algorithm> <version> <input_file> <output_file>") 
        
    