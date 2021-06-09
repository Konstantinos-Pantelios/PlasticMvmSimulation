import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import classes as pls
import simulation as sim
import numpy as np
import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    print("################ Plastic Movement Simulator ################"+"\n"+ "##------   TUDelft - Noria Sustainable Innovators   ------##"+"\n"+"##------      Synthesis project GEO1101 - 2021      ------##"+"\n"+"############################################################"+"\n")
    print("|NOTES:")
    print("|-> The simulation works by assuming a wind direction of 45 degrees (SW)")
    print("|-> Plastiscs are being inserted into the network's nodes based on proximity to 'recreation' locations (1 to 1)"+'\n')
def params(lever):
    print("################ Plastic Movement Simulator ################"+"\n"+ "##------   TUDelft - Noria Sustainable Innovators   ------##"+"\n"+"##------      Synthesis project GEO1101 - 2021      ------##"+"\n"+"############################################################"+"\n")
    print("|NOTES:")
    print("|-> The simulation works by assuming a wind direction of 45 degrees (SW)")
    print("|-> Plastiscs are being inserted into the network's nodes based on proximity to 'recreation' locations (1 to 1)"+'\n')
    if lever:
        while True:
            try:
                Wind = int(input("Insert wind direction (in degrees): "))
                assert 0 <= Wind <= 359 
            except ValueError:
                cls()
                print("This is not a valid number. Try again.")
            except:
                cls()
                print("Direction should be in degrees (0-359). Try again.")
            else: 
                return Wind
                while True:    
                    try:
                        Amount = int(input("Insert amount of plastic units: "))
                        assert 1 <= Amount <= 1000 
                    except ValueError:
                        cls()
                        print("This is not a valid number. Try again.")
                    except:
                        cls()
                        print("Too large or small amount (1-1000). Try again")
                    else:
                        break
                return Wind
    else: return 45
        
def plot_start(nodes, wind_direction,leeway_drift, plastics_100):
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

    pos_pls =  {k:v.coords() for k,v in enumerate(plastics_100)}
    # pos_pls =  {k:v.coords() for k,v in enumerate(plastics_100)} # Get enumerated position of plastic units. Dictionary {0:(x1,y1),1:(x2,y2),...} 
    n_list=[k for k,v in enumerate(nodes.values()) if v.has_plastics_num()>0]
    pos_relabel =  { k:v.has_plastics_num() for k,v in enumerate(nodes.values()) if v.has_plastics_num()>0} # Get enumerated amount of plastic units in nodes. Dictionary {0:5,1:4,2:0,..}
    node_plastic_count = list(pos_relabel.values()) # list of number of plastics at the nodes
    pos_node ={k:v.coords() for k,v in enumerate(nodes.values())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}
    # print(n_list)
    # print(node_plastic_count, len(node_plastic_count))
    # print(pos_relabel, len(pos_relabel))
    #print(pos_pls,len(pos_pls))

    X=nx.Graph()
    X.add_nodes_from(pos_pls.keys())
    l = [set(x) for x in G.edges()]
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
    nx.draw_networkx_labels(X, pos_node, labels=pos_relabel,font_size=16,horizontalalignment='right', verticalalignment='bottom',)
    X.add_edges_from(G.edges())
    nx.draw_networkx_edges(X, pos_e2)
    ###################################################

def plot_end(nodes,plastics_100):
    ######### 2. Display network graph figure AFTER the completion of the simulation #####################################
    min_x=np.min([n[0] for n in nodes.keys()])
    min_y=np.min([n[1] for n in nodes.keys()])
    max_x=np.max([n[0] for n in nodes.keys()])
    max_y=np.max([n[1] for n in nodes.keys()])

    pls=[]
    for p in plastics_100:
        if p.find_in_node(nodes) == None:
            pls.append(p)
            #print(p.is_active) #= true

    pos_pls_re =  {k:v.coords() for k,v in enumerate(pls)} # Get enumerated position of plastic units. Dictionary {0:(x1,y1),1:(x2,y2),...} 
    pos_pls = {k:v.coords() for k,v in enumerate(plastics_100)}


    # pos_forelabel= []
    # for n in nodes.values(): 
    #     if n.has_plastics_num()>0: pos_forelabel.append(n)

    pos_relabel = { k:v.has_plastics_num() for k,v in enumerate(nodes.values()) if v.has_plastics_num()>0} # Get enumerated amount of plastic units in nodes. Dictionary {0:5,1:4,2:0,..}
    node_plastic_count = list(f for f in pos_relabel.values()) # list of number of plastics at the nodes
    pos_node ={k:v.coords() for k,v in enumerate(nodes.values())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}


    X=nx.Graph()
    X.add_nodes_from(pos_pls.keys())
    l = [set(x) for x in G.edges()]
    edg=[tuple(k for k, v in pos_e2.items() if v in s1 ) for s1 in l]


    plt.subplot(122)
    red_patch = mpatches.Patch(color='red', label="Plastics that haven't yet reached a particular node")
    blue_patch = mpatches.Patch(color='red', label="Plastics in nodes")
    # plt.arrow(x=min_x-70, y=min_y-80, dx=0, dy=ext_y, width=2,color='k' ) 
    # plt.arrow(x=min_x-70, y=min_y-80, dx=dx_wind, dy=dy_wind, width=10,color='b')
    # plt.arrow(x=min_x-70, y=min_y-80, dx=dx_leeway, dy=dy_leeway, width=5,color='r')
    plt.axis([min_x-200,max_x+200,min_y-200,max_y+200])
    # plt.annotate("Wind Direction: "+str(wind_direction)+" degrees", xy=(min_x+40, min_y-100,),color='b')
    # plt.annotate("N ", xy=(min_x-70+10, min_y-80+560))
    # plt.annotate("Leeway drift +"+str(leeway_drift)+" degrees", xy=(min_x+40, min_y-170),color='r')
    plt.legend(handles=[blue_patch])

    #nx.draw_networkx_nodes(X, pos_pls, nodelist=pos_pls_re, node_color='red', node_size=2,node_shape='*')
    nx.draw_networkx_nodes(X, pos_node, nodelist=pos_relabel, node_size=node_plastic_count,node_color='r')

    nx.draw_networkx_labels(X, pos_node, labels=pos_relabel, horizontalalignment="left",verticalalignment="bottom")
    X.add_edges_from(G.edges())
    nx.draw_networkx_edges(X, pos_e2)


Wind = params(0) #Change this to 1 to allow the user to insert specific wind direction. 0 defaults 45 degree wind direction

start_t=time.perf_counter() #initiate timer

#Define the local path of the shapefile  
edges_path = "./Data/region_delft_waterlines.shp"
nodes_path = "./Data/region_delft_nodes2.shp"


#Read the shp files 
G = nx.read_shp(edges_path,simplify=False,strict=False) # Water network graph (Contains ALL nodes between different edges that are irrelevant for the project)
N = nx.read_shp(nodes_path,simplify=False,strict=False) # Relevant to project node graph (DOES NOT contain any edges)

for datadict in G.edges.items():
    has_flow = datadict[1]['has_flow']
    start_node=datadict[0][0]
    end_node= datadict[0][1]
    nx.nodes(G)[start_node].update({"class":"Irrelevant","has_flow":has_flow})
    nx.nodes(G)[end_node].update({"class":"Irrelevant","has_flow":has_flow})



pos_e = {k:v for k,v in enumerate(G.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}
pos_n = {k:v for k,v in enumerate(N.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...} 
pos_e2 = {v:v for v in G.nodes()}

#fields = pls.show_fields(G) # Get all availiable fields of the shp layer. (edges,nodes)


#######################-------------- Instantiate Objects ---------------##########################
#Create n number of "plastic" objects at x:0 ,y:0
n=0
for node in N.nodes.items():
    if not node[1]["pls_amount"]:
        node[1]["pls_amount"]=0
    n+=node[1]["pls_amount"]

plastics_100 = pls.create_plastics(n)
plastics_to_pour = plastics_100.copy() # temporary layer used to pour all the plastic created above to the nodes depending on the latter's proximity to recreation locations.


#Create n "node" objects. n = G.number_of_nodes() 
nodes = {}
relevant_nodes= {k[0]:k[1] for k in N.nodes.items()} #Dictionary {(x1,y1):{filed1:value1,field11:value11,..},..}
z=0
for d in G.nodes.items():
    if d[0] in relevant_nodes.keys():
        identification = relevant_nodes[d[0]]["id"]
        x_coord = d[0][0]
        y_coord = d[0][1]
        attributes = {k:relevant_nodes[d[0]][k] for k in relevant_nodes[d[0]].keys()}
        nodes[d[0]]=pls.node(identification,x_coord,y_coord,attributes) #Instantiate decision making node object inside a dictionary {(x1,y1):<node_object>,..}
        for k in range(int(relevant_nodes[d[0]]["pls_amount"])):
            nodes[d[0]].insert_plastic(plastics_to_pour.pop(-1))
            z+=1
    else:
        
        identification = str(list(pos_e.keys())[list(pos_e.values()).index(d[0])])
        x_coord = d[0][0]
        y_coord = d[0][1]
        attributes = d[1]
        nodes[d[0]]=pls.node(identification,x_coord,y_coord,attributes) #Instantiate irrelevant node object inside a dictionary {(x1,y1):<node_object>,..}


#######################--------------------------------------------------##########################

 

##############################################

wind_direction=Wind
leeway_drift=15

plot_start(nodes,wind_direction,leeway_drift,plastics_100)

#**** Run the simulation ****#
sim.simulation(G,nodes,plastics_100,wind_direction,leeway_drift)
plot_end(nodes,plastics_100)
plt.show()

print("\nExecution time: "+str(round(time.perf_counter()-start_t,2))+"sec")

#############################################################

# c=0
# for n in nodes.values():
#    c+=n.has_plastics_num() 
#print("from ",len(plastics_100),",",c," plastic units are in nodes" )

### ------->>>>> Export the results into a .shp file into the ./Data/plastics directory. -------->>>>> #####
pos_pls = {k:v.coords() for k,v in enumerate(plastics_100)}
S=nx.DiGraph()
S.add_nodes_from(pos_pls.values()) #check documentation if it removes duplicates
a=0
for p in S.nodes.items():
    a+=1
    p[1].update({'Wkt':'POINT ('+str(p[0][0])+" "+str(p[0][1])+')'})
nx.write_shp(S, './Data/plastics')
print("Potential hotspots have been exported as .shp file in './Data/plastics/nodes.shp'")
### -------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>>-------->>>>> #####

# TODO: Fix issue with wierd coordinate result of plastics outside of nodes.