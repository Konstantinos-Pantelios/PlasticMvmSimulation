import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import classes as pls
import simulation as sim
import numpy as np
import time
import os

global ENDC
ENDC = '\033[m'
global REDC
REDC = '\033[91m'
global GREENC
GREENC = '\033[92m'
global YELLOWC
YELLOWC = '\033[93m'
def initiate_terminal_txt():
    print(GREENC)
    print("################ Plastic Movement Simulator ################"+"\n"+ "##------   TUDelft - Noria Sustainable Innovators   ------##"+"\n"+"##------      Synthesis project GEO1101 - 2021      ------##"+"\n"+"############################################################"+"\n")
    print(YELLOWC)
    print("|NOTES:")
    print("|-> The simulation works by assuming a wind direction of 45 degrees (SW)")
    print("|-> Plastiscs are being inserted into the network's nodes based on proximity to 'recreation' locations (1 to 1)"+'\n')
    print(ENDC)


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    initiate_terminal_txt()
def params(lever):
    initiate_terminal_txt()
    if lever:
        while True:
            try:
                Wind = int(input("Insert wind direction (in degrees): "))
                assert 0 <= Wind <= 359 
            except ValueError:
                cls()
                print(REDC+"This is not a valid number. Try again."+ENDC)
            except:
                cls()
                print(REDC+"Direction should be in degrees (0-359). Try again."+ENDC)
            else: 
                return Wind
    else: return 45

def load_data(edge_fileNAME,node_fileNAME):
    """IMPORTANT:   -Keep the data that you want to load in the 'Data' folder (this is hardcoded)
                    -Don't create and put files in subfolders in the 'Data' directory
                    -Provide the function ONLY with the name of the files (e.g. delft_waterlines.shp, region_delft_nodes.shp)
        Return a dictionary with keys 'Edges' and 'Nodes' """

    #Get the absolute paths of the code file (main.py) and its dir  
    file_path = os.path.realpath(__file__)
    file_dir = os.path.dirname(file_path) 
    os.chdir(file_dir) #Set the working directory "..../..../..../PlasticMvmSimulation"
    curr_dir = os.getcwd()
    edges_path = os.path.join(curr_dir,"Data",edge_fileNAME) 
    nodes_path = os.path.join(curr_dir,"Data",node_fileNAME)

    #Read the shp files 
    Edge = nx.read_shp(edges_path,simplify=False,strict=False) # Water network graph (Contains ALL nodes between different edges that are irrelevant for the project)
    Node = nx.read_shp(nodes_path,simplify=False,strict=False) # Relevant to project node graph (DOES NOT contain any edges)

    return {"Edges":Edge,"Nodes":Node}

def get_sum_of_numeric_field(graph,field):
    n=0
    for node, field_dict in graph.nodes.items():
        if not field_dict[field]: #Check if the field is NULL and set it to 0 pieces of plastic
            field_dict[field]=0
        n+=field_dict[field]
    return n

def plot_start(nodes, wind_direction, leeway_drift, plastics_n):
    ##### Parameters used for ploting the figures ################################
    min_x=np.min([n[0] for n in nodes.keys()])
    min_y=np.min([n[1] for n in nodes.keys()])
    max_x=np.max([n[0] for n in nodes.keys()])
    max_y=np.max([n[1] for n in nodes.keys()])
    ext_x=int(max_x-min_x) # Unused
    ext_y=int((max_y-min_y)/8) 
    dx_wind = 0.1 * math.sin(math.radians(wind_direction))+1.1
    dy_wind =  0.1 * math.cos(math.radians(wind_direction)) +0.1
    dx_leeway = 0.09 * math.sin(math.radians(wind_direction+leeway_drift)) +1.1
    dy_leeway = 0.09 * math.cos(math.radians(wind_direction+leeway_drift)) +0.1
    #################################################################################

    ########### 1. Display network graph figure at time BEFORE initiating the algorithm. ##################################

    pos_pls =  {k:v.coords() for k,v in enumerate(plastics_n)} # Get enumerated position of plastic units. Dictionary {0:(x1,y1),1:(x2,y2),...} 
    n_list=[k for k,v in enumerate(nodes.values()) if v.has_plastics_num()>0]
    pos_relabel =  { k:v.has_plastics_num() for k,v in enumerate(nodes.values()) if v.has_plastics_num()>0} # Get enumerated amount of plastic units in nodes. Dictionary {0:5,1:4,2:0,..}
    node_plastic_count = list(pos_relabel.values()) # list of number of plastics at the nodes
    pos_node ={k:v.coords() for k,v in enumerate(nodes.values())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}


    X=nx.Graph()
    X.add_nodes_from(Node_graph.nodes())
    l = [set(x) for x in Edge_graph.edges()]
    edg=[tuple(k for k, v in pos_e.items() if v in s1 ) for s1 in l]

    plt.subplot(121)
    blue_patch = mpatches.Patch(color='tab:blue', label="Plastics in nodes")
    plt.axis([min_x-200,max_x+200,min_y-200,max_y+200])
    plt.annotate("Wind Direction: "+str(wind_direction)+" degrees", xy=(1, -0.02),xycoords='axes fraction',xytext=(1, -0.02),color='b')
    plt.annotate("Leeway drift +"+str(leeway_drift)+" degrees",  xy=(0, -0.04),xycoords='axes fraction',xytext=(1, -0.04),color='r',annotation_clip=False)
    plt.annotate("N ", xy=(1.1, 0.21),xycoords='axes fraction',xytext=(1.1, 0.21))
    plt.annotate("", xy=(1.1, 0.21), xycoords='axes fraction',xytext=(1.1, 0.1), arrowprops=dict(arrowstyle="->"),annotation_clip=False)
    plt.annotate("", xy=(dx_wind, dy_wind), xycoords='axes fraction',xytext=(1.1, 0.1), arrowprops=dict(arrowstyle="->",color='b'),annotation_clip=False)
    plt.annotate("", xy=(dx_leeway, dy_leeway), xycoords='axes fraction',xytext=(1.1, 0.1), arrowprops=dict(arrowstyle="->",color='r'),annotation_clip=False)

    plt.legend(handles=[blue_patch])


    nx.draw_networkx_nodes(X, pos_node, nodelist=n_list, node_size=node_plastic_count)
    nx.draw_networkx_labels(X, pos_node, labels=pos_relabel,font_size=16,horizontalalignment='right', verticalalignment='bottom') 
    X.add_edges_from(Edge_graph.edges())
    nx.draw_networkx_edges(X, pos_e2)
    ###################################################

def plot_end(nodes,plastics_n):
    ######### 2. Display network graph figure AFTER the completion of the simulation #####################################
    min_x=np.min([n[0] for n in nodes.keys()])
    min_y=np.min([n[1] for n in nodes.keys()])
    max_x=np.max([n[0] for n in nodes.keys()])
    max_y=np.max([n[1] for n in nodes.keys()])

    pls=[]
    for p in plastics_n:
        if p.find_in_node(nodes) == None:
            pls.append(p)


    pos_pls_re =  {k:v.coords() for k,v in enumerate(pls)} # Get enumerated position of plastic units. Dictionary {0:(x1,y1),1:(x2,y2),...} 
    pos_pls = {k:v.coords() for k,v in enumerate(plastics_n)}

    pos_relabel = { k:v.has_plastics_num() for k,v in enumerate(nodes.values()) if v.has_plastics_num()>0} # Get enumerated amount of plastic units in nodes. Dictionary {0:5,1:4,2:0,..}
    node_plastic_count = list(f for f in pos_relabel.values()) # list of number of plastics at the nodes
    pos_node ={k:v.coords() for k,v in enumerate(nodes.values())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}


    X=nx.Graph()
    X.add_nodes_from(pos_pls.keys())
    l = [set(x) for x in Edge_graph.edges()]
    edg=[tuple(k for k, v in pos_e2.items() if v in s1 ) for s1 in l]


    plt.subplot(122)
    red_patch = mpatches.Patch(color='red', label="Plastics that haven't yet reached a particular node")
    blue_patch = mpatches.Patch(color='red', label="Plastics in nodes")

    plt.axis([min_x-200,max_x+200,min_y-200,max_y+200])

    plt.legend(handles=[blue_patch])

    #nx.draw_networkx_nodes(X, pos_pls, nodelist=pos_pls_re, node_color='red', node_size=2,node_shape='*')
    nx.draw_networkx_nodes(X, pos_node, nodelist=pos_relabel, node_size=node_plastic_count,node_color='r')

    nx.draw_networkx_labels(X, pos_node, labels=pos_relabel, horizontalalignment="left",verticalalignment="bottom")
    X.add_edges_from(Edge_graph.edges())
    nx.draw_networkx_edges(X, pos_e2)


######################################################################################################################################################################################
##########################################       Code starts HERE      ###############################################################################################################

#Set the direction of the wind 
Wind = params(0) #Change this to 1 to allow the user to insert specific wind direction. 0 defaults 45 degree wind direction
wind_direction=Wind
leeway_drift=15


#initiate timer (Irrelevant to the simulation itself)
start_t=time.perf_counter() 

#Load edge and node shapefiles from 'Data'
nodes_and_grahps = load_data(edge_fileNAME= "waterlines_clean.shp", node_fileNAME= "nodes_clean.shp") #Return a dictionary with only keys: "Edges","Nodes" and values their corresponding graphs
Edge_graph = nodes_and_grahps["Edges"] #Netwrokx graph of edges (waterlines)
Node_graph = nodes_and_grahps["Nodes"] #Netwrokx graph of nodes 
#Edge_graph.add_nodes_from(Node_graph.nodes()) #Update the nodes of the edege graph with the nodes of the node graph
print("Number of nodes:",len(Node_graph.nodes))

#Assign 'class' and 'flow' attributes to the nodes of the 'Waterline graph'. At first all nodes are set as "Irrelevant"
for nodes,field_dict in Edge_graph.edges.items():
    start_node=nodes[0]
    end_node= nodes[1]
    has_flow = field_dict['has_flow']
    nx.nodes(Edge_graph)[start_node].update({"class":"Irrelevant","has_flow":has_flow})
    nx.nodes(Edge_graph)[end_node].update({"class":"Irrelevant","has_flow":has_flow})
    

pos_e = {k:v for k,v in enumerate(Edge_graph.nodes())} # Get enumerated position of edges. Dictionary {0:(x0,y0),1:(x1,y1),...}
pos_n = {k:v for k,v in enumerate(Node_graph.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...} 
pos_e2 = {v:v for v in Edge_graph.nodes()}


#fields = pls.show_fields(Edge_graph) # Get all availiable fields of the shp layer. (edges,nodes)

#######################-------------- Instantiate Objects (Start) ---------------##########################
#Calculate the amount of plastic from 'pls_amount' field of the Node's graph
total_plastic_pieces = get_sum_of_numeric_field(Node_graph,"pls_amount")
print('Total pieces of plastics:',total_plastic_pieces)

#Create n number of "plastic" objects at x:0 ,y:0
plastics_n = pls.create_plastics(total_plastic_pieces)
plastics_to_pour = plastics_n.copy() # temporary layer used to pour all the plastic created above to the nodes depending on the latter's proximity to recreation locations.


#Create n "node" objects. n = Edge_graph.number_of_nodes()

#NOTE:  It is important to understand that the 'Edge graph' (Edge_graph) contains nodes that define the edges but may or may not be irrelevant to the nodes that we are interested in.
#       The nodes that we are intersted in, are located into the 'Nodes graph' (Node_graph), thus we need to impose these nodes to the nodes of the 'Edge graph'.
#       To do this we loop through the 'Graph nodes' and when we see a node with the same coordinates as one of the nodes from the 'Nodes graph' then it means that this node IS relevant us, so we keep it and fill it with attributes
#       To achive this, it is REQUIRED that the 'Nodes' shapefile has been extracted from the 'Edges' shapefile (meaning in practice that the nodes of 'Nodes' is a subset of the nodes of 'Edges')
#NOTE again that due to the above data dependincy, most errors are going to originate more or less from here 
 
nodes = {}
relevant_nodes= {nodes:fields for nodes, fields in Node_graph.nodes.items()} #Dictionary {(x1,y1):{filed1:value1,field11:value11,..},..}


x,y = zip(*list(relevant_nodes.keys()))

for g_nodes,g_fields in Edge_graph.nodes.items():

    if g_nodes in list(relevant_nodes.keys()): #Checks if a node from the 'Edges graph' is a relevant node
        identification = relevant_nodes[g_nodes]["id"]
        x_coord = g_nodes[0]
        y_coord = g_nodes[1]
        attributes = {k:relevant_nodes[g_nodes][k] for k in relevant_nodes[g_nodes].keys()}
        nodes[g_nodes]=pls.node(identification,x_coord,y_coord,attributes) #Instantiate decision making node object inside a dictionary {(x1,y1):<node_object>,..}
        for k in range(int(relevant_nodes[g_nodes]["pls_amount"])):
            nodes[g_nodes].insert_plastic(plastics_to_pour.pop(-1))

    else:
        identification = str(list(pos_e.keys())[list(pos_e.values()).index(g_nodes)])
        x_coord = g_nodes[0]
        y_coord = g_nodes[1]
        attributes = g_fields
        nodes[g_nodes]=pls.node(identification,x_coord,y_coord,attributes) #Instantiate irrelevant node object inside a dictionary {(x1,y1):<node_object>,..}

#######################-------------------- Instantiate Objects (End) ------------------------------##########################

##############################################

# for node, node_obj in nodes.items():
#     print(node,node_obj.fields)

plot_start(nodes,wind_direction,leeway_drift,plastics_n)

#**** Run the simulation ****#
sim.simulation(Edge_graph,nodes,plastics_n,wind_direction,leeway_drift)
#****************************#

plot_end(nodes,plastics_n)
plt.show()

print(YELLOWC+"\nExecution time: "+str(round(time.perf_counter()-start_t,2))+"sec"+ENDC)

#############################################################

### ------->>>>> Export the results into a .shp file into the ./Data/plastics directory. -------->>>>> #####
pos_pls = {k:v.coords() for k,v in enumerate(plastics_n)}
S=nx.DiGraph()
S.add_nodes_from(pos_pls.values())
a=0
for p in S.nodes.items():
    a+=1
    p[1].update({'Wkt':'POINT ('+str(p[0][0])+" "+str(p[0][1])+')','ID': nodes[p[0]].id,'pls_amount':nodes[p[0]].has_plastics_num(),'class': nodes[p[0]].fields["class"]})

path = os.path.join("Data","plastics","hotspots.shp") # Modify this line to either change the name of the output or change the path.

nx.write_shp(S, path)
print(GREENC+"Potential hotspots have been exported as .shp file in "+path+ENDC)
### -------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>> #####

# TODO: Fix issue with wierd coordinate results of plastics outside of nodes.