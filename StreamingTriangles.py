''' -----------------------------------------------------------------------------------------
Global variables
-------------------------------------------------------------------------------------------- '''

''' Edge reservoir '''
edge_res = []

''' Wedge reservoir '''
wedge_res = []

'''  New wedges: List of all edges involving e_t, formed only by edges in edge_res'''
N_t = []

'''Number of edges formed in edge_res'''
tot_wedges = 0

'''Boolean array indicating whether a wedge in wedge_res is closed or not'''
isClosed = []

# Size of edges pool
se = 5
# Size of wedges pool
sw = 5

def streaming_triangles(se, sw):
    print ("Streaming Triangles.")
    print("Initial parameters: [se]=" + str(se) + ", [sw]=" + str(sw))

    #Initialization process: edge_res and wedge_res are initialized based on the given parameters.
    #List isClosed will have same size as wedge_res
    global edge_res
    edge_res= [0]*se
    global wedge_res
    wedge_res= [0]*sw
    global isClosed
    isClosed= [0] * sw

    #Read from the stream of data every income edge
    t=1
    with open('ucidata-zachary/out.ucidata-zachary') as file:
        for e_t in file:
            print ("\n \n [New edge] " + str(e_t))
            update(e_t)
            p= (isClosed.count(1))/len(isClosed)
            k_t = 3*p
            T_t = ((p*(t**2))/(se*(se-1)))
            print("Estimates after processing [e_t]=" + str(e_t) + ": [k_t]="+  str(k_t) + ", [T_t]=" + str(T_t))
            t+=1



def update(e_t):
    print ("UPDATE: " + e_t)
    #Determine all the wedges in the reservoir that are closed by e_t
    for i in range (0, sw):
        print("i " + str(i))
        closed(wedge_res[i], e_t)



def closed(wedge, e_t):
    print("Checking if [wedge] " + str(wedge) + "is closed by [e_t] " + str(e_t))


def main():
    #Parameters
    streaming_triangles(se,sw)


main()