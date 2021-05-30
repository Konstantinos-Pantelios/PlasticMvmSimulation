import networkx as nx
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
import plastics as pls




#Define the local path of the shapefile  
edges_path = "/home/konstantinos/Desktop/TUDelft-Courses/Q4/GEO1101/Clean water layer/data/delft_waterlines.shp"
nodes_path = "/home/konstantinos/Desktop/TUDelft-Courses/Q4/GEO1101/Clean water layer/data/delft_nodes.shp"


#Read the shp files 
G = nx.read_shp(edges_path,simplify=False,strict=False) # Water network graph (Contains ALL nodes between different edges that are irrelevant for the project)
N = nx.read_shp(nodes_path,simplify=False,strict=False) # Relevant to project node graph (DOES NOT contain any edges)

pos_e = {k:v for k,v in enumerate(G.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}
pos_n = {k:v for k,v in enumerate(N.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...} 

print(pos_n)


fields = pls.show_fields(N) # Get all availiable fields of the shp layer. (edges,nodes)


# print("nodes of graph X:",X.number_of_nodes()," Nodes of graph N:",len(pos_n))


#######################-------------- Instantiate Objects ---------------##########################
#Create 100 "plastic" objects at x:0 ,y:0
plastics_100 = pls.create_plastics(100)

#Create n "node" objects. n = G.number_of_nodes() 
nodes = []
for index in pos_n.keys():
    nodes.append(pls.node(index,pos_n[index][0],pos_n[index][1]))
#######################--------------------------------------------------##########################


#Pour all of the plastics (100) consecutively into the first 20 nodes of the water network. max value: size(nodes)-2
c=0
for plastic_unit in plastics_100:
    if c <= 18 :
        nodes[c].insert_plastic(plastic_unit)
        c+=1
    else:
        nodes[c].insert_plastic(plastic_unit)
        c=0
###### Test of the methods of the classes ####
# plastics_100[0].coords()
# nodes[0].has_plastics_num()
# plastics_100[52].coords()
# plastics_100[52].find_in_node(nodes)
# nodes[31].has_plastics()
##############################################


#Display network graph figure
pos_pls =  {k:v.coords() for k,v in enumerate(plastics_100)} # Get enumerated position of plastic units. Dictionary {0:(x1,y1),1:(x2,y2),...} 
pos_relabel = {k:v.has_plastics_num() for k,v in enumerate(nodes)} # Get enumerated amount of plastic units in nodes. Dictionary {0:5,1:4,2:0,..}
pos_node ={k:v.coords() for k,v in enumerate(nodes)} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}


X=nx.MultiGraph()
X.add_nodes_from(pos_pls.keys())
l = [set(x) for x in G.edges()]
edg=[tuple(k for k, v in pos_e.items() if v in s1 ) for s1 in l]


nx.draw_networkx_nodes(X, pos_pls,node_size=10)
nx.draw_networkx_labels(X, pos_node, labels=pos_relabel,font_size=16,horizontalalignment='right', verticalalignment='bottom')
X.add_edges_from(edg)
nx.draw_networkx_edges(X, pos_e)
plt.show()

