from networkx import Graph
import random
import itertools
import re
import sys

''' -----------------------------------------------------------------------------------------
Functions
-------------------------------------------------------------------------------------------- '''

def streaming_triangles(dataset, a, b):
    '''
    Estimates de triangle count and the transitivty (clustering coefficient) of a stream of edges obtained from the given dataset.
    The algorithm reads each line of the dataset simulating a stream of edges.
    For each edge, the update function is called (it is responsible of updating the reservoir samplings). After the call,
     this function estimates the values k and T
    :param dataset: dataset path
    :param a: size of the edge reservoir
    :param b: size of the wedge reservoir
    '''
    global se #global variable for edge reservoir size
    se = a
    global sw
    sw = b #global variable for wedge reservoir size

    print ("Streaming Triangles")
    print("Initial parameters: [se]=" + str(se) + ", [sw]=" + str(sw))

    #Initialization process: edge_res and wedge_res are initialized based on the given parameters.
    global edge_res  #Edge reservoir
    edge_res= [(0,0)]*se
    global wedge_res #Wedge reservoir
    wedge_res= [(0,0,0)]*sw
    global isClosed  # This is a boolean array. We set isClosed[i] to be true if wedge wedge res[i] is detected as closed.
    isClosed= [0] * sw
    global edge_res_subgraph #The subgraph associated to the edges stored in edge_res
    edge_res_subgraph = Graph()
    global wedge_tot #Set of all wedges that can be formed by edge_res
    wedge_tot = []
    tot_wedges = [0] #Total number of wedges that can be formed by edge_res


    #Read from the stream of data every income edge
    t=1
    with open(dataset) as file:
        for line in file:
            if not line.startswith('%'):
                e_t_line = line.replace("\n", "").split(" ")
                e_t = (e_t_line[0], e_t_line[1])
                print("\n \n [New edge] " + str(e_t))
                #if t<100: #Used just to show how the alg. works during the presentation
                update(e_t, t, tot_wedges)
                p= (isClosed.count(1))/len(isClosed)
                k_t = 3*p
                T_t = ((p*(t**2))/(se*(se-1)))*tot_wedges[0]
                print("[t]=" + str(t) + " [p]= " + str(p) + " [tot_wedges]= " + str(tot_wedges))
                print("Estimates after processing: \n"  +
                      "[k_t]="+  str(k_t) + ", [T_t]=" + str(T_t))
                t+=1
                #else:
                    #break

def update(e_t, t, tot_wedges):
    '''
    Updates the edge and wedge reservoir with certain probability. If edge_res changes, then it calculates all the wedges
    formed by edge_res. It also calculates the wedges involving the edge e_t given as a parameter. At the end, with a certain
    probability it also updates the wedge reservoir.
    :param e_t: edge at a time t
    :param t: moment of time t={1,2,...,n)
    :param tot_wedges: variable to store the total of wedges that are possible to generate by edge_res
    '''

    #Determine all the wedges in the reservoir that are closed by e_t
    for i in range (0, sw):
        if closed(wedge_res[i], e_t) ==1:
            isClosed[i] = 1

    #We perform reservoir sampling on edge res. This involves replacing each entry by et with probability 1/t. The remaining
    #steps are executed iff this leads to any changes in edge res.
    edge_res_updated = 0
    for i in range (0,se):
        x = random.random()
        if(x <= (1/t)):
            edge_res[i] = e_t
            edge_res_updated+=1
    #We perform some updates to tot_wedges and determine the new wedges Nt.
    if(edge_res_updated >= 1):
        #print("[edge_res] " + str(edge_res)) #Uncomment for presentation purposes
        wedges = updateWedges()
        tot_wedges[0] = len(wedges)
        n_t = calculateNt(e_t, wedges)
        new_wedges = len(n_t)

        #we perform reservoir sampling on wedge res, where each entry is randomly replaced with some
        # wedge in Nt. Note that we may remove wedges that have already closed.
        for i in range(0, sw):
            x = random.random()
            if(tot_wedges[0] !=0):
                if(x <= new_wedges/tot_wedges[0]):
                    w = random.choice(n_t)
                    wedge_res[i] = w
                    isClosed[i] = 0


def calculateNt(e_t, wedges):
    '''
    Calculates all the wedges involving the edge e_t given as a parameter
    :param e_t: edge at time e
    :param wedges: set of  wedges
    :return: total number of wedges where e_t is involved
    '''
    n_t = []
    e_t_set = set(e_t)
    for w in wedges:
        if len(set(w) - e_t_set) ==1:
            n_t.append(w)
    return n_t


def closed(wedge, e_t):
    '''
    Determines if a wedge is closed by the edge given as a parameter
    :param wedge: a triple of edges (a,b,c), where a is the node and b and c its neighbors
    :param e_t: edge (a,b) at a given time
    :return: 1 if the wedge is closed by e_t, 0 otherwise
    '''
    resp = 0
    if((e_t[0] == wedge[1] and e_t[1] == wedge[2]) or (e_t[1] == wedge[1] and e_t[0] == wedge[2])):
        resp = 1
    return resp


def updateWedges():
    '''
    Update the wedges that can be generated using the current edge_res
    :return: A set of triplets (a,b,c) of all possible wedges, where a corresponds to a node in the graph and b and c its neighbors
    '''
    graph = Graph()
    for edge in edge_res:
            graph.add_edge(edge[0], edge[1])

    wedges = wedge_iterator(graph)

    #Print the wedges to double check
    print("[wedges] " + str(len(wedges)) + ": ")
    #for w in wedges:   # Uncomment for presentation purposes
        #print(str(w))  #  Uncomment for presentation purposes

    return wedges

def wedge_iterator(graph):
    '''
    Generates all possible wedges that can be formed by a given graph
    :param graph: graph containing all the edges in edge_res
    :return: A set of triples (a,b,c) containing all the wedges in the graph. The triplet (a,b,c) is composed of a node a and its neighbors b and c
    '''
    resp = []
    for node in graph.nodes:
        neighbors = graph.neighbors(node)
        for pair in itertools.combinations(neighbors, 2):
            resp.append((node, pair[0], pair[1]))
    return resp

''' -----------------------------------------------------------------------------------------
Main & Execution
-------------------------------------------------------------------------------------------- '''

def main():
    #Parameters
    dataset = "data/petster-hamster/out.petster-hamster"
    edge_reservoir_size = 1000
    wedge_reservoir_size = 1000
    streaming_triangles(dataset, edge_reservoir_size,wedge_reservoir_size)

try:
    main(float(sys.argv[1]),float(sys.argv[2]),sys.argv[3])
except:
    main()


