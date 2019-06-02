import grafos
import sys

def Dijsktra(G,src):
    dist,path = grafos.dijkstra(G,src)
    grafos.printPath(src,dist,path)

def DijkstraFibHeap(G,src):
    dist,path = grafos.dijkstraFibHeap(G,src)
    grafos.printPath(src,dist,path)

def BellmanFord(G,src):
    out = grafos.BellmanFord(G,src)
    if(out != None):
        dist,path = out
        grafos.printPath(src,dist,path)
    else:
        print("Ciclo negativo")


def FloydWarshall(G):
    dist,prox = grafos.FloydWarshall(G)
    for i in range(len(prox)):
        grafos.printPath(i,dist[i],prox[i])

def Johnson(G):
    dist,prox = grafos.Johnson(G)
    for i in range(len(prox)):
        grafos.printPath(i,dist[i],prox[i])


def JohnsonFibHeap(G):
    dist,prox = grafos.JohnsonFibHeap(G)
    for i in range(len(prox)):
        grafos.printPath(i,dist[i],prox[i])

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


def main(alg,version,in_file,out_file):
    graph,src = inputfile(in_file)
    try:
        pass
    except:
        print("Invalid input file")
        return

    if(alg.lower() == "dijkstra"):
        if(version == 0):
            print("Dijkstra with array Heap")
        elif(version == 1):
            print("Dijkstra with binary Heap")
            Dijkstra(graph,src)
        elif(version == 2):
            print("Dijkstra with Fibonacci Heap")
            DijkstraFibHeap(graph,src)
    elif(alg.lower() == "bellman-ford"):
        print("Bellman Ford")
        BellmanFord(graph,src)
    elif(alg.lower() == "floyd-warshall"):
        print("Floyd-Warshal")
        FloydWarshall(graph)
    elif(alg.lower() == "johnson"):
        if(version == 0):
            print("Johnson with Array Heap")
        elif(version == 1):
            print("Johnson with Binary Heap")
            Johnson(graph)
        elif(version == 2):
            print("Johnson with Fibonacci Heap")
            JohnsonFibHeap(graph)
    else:
        print("Usage <algorithm> <version> <input_file> <output_file>") 
        return
    

if __name__== "__main__":
    if(len(sys.argv) == 5):
        alg,version,in_file,out_file = sys.argv[1:]    
        main(alg,int(version),in_file,out_file)
    #except:
    #    print("Usage <algorithm> <version> <input_file> <output_file>") 
        
    