import networkx as nx
import matplotlib.pyplot as plt
import classes as pls
import simulation as sim




#Define the local path of the shapefile  
edges_path = "./Data/test_network.shp"
nodes_path = "./Data/test_nodes.shp"


#Read the shp files 
G = nx.read_shp(edges_path,simplify=False,strict=False) # Water network graph (Contains ALL nodes between different edges that are irrelevant for the project)
N = nx.read_shp(nodes_path,simplify=False,strict=False) # Relevant to project node graph (DOES NOT contain any edges)

pos_e = {k:v for k,v in enumerate(G.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}
pos_n = {k:v for k,v in enumerate(N.nodes())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...} 


fields = pls.show_fields(N) # Get all availiable fields of the shp layer. (edges,nodes)



firstnode = pos_e[0]
#print(firstnode)

#######################-------------- Instantiate Objects ---------------##########################
#Create 100 "plastic" objects at x:0 ,y:0
plastics_100 = pls.create_plastics(5)

#Create n "node" objects. n = G.number_of_nodes() 
nodes = {}
relevant_nodes= {k[0]:k[1] for k in N.nodes.items()}
for d in G.nodes.items():
    if d[0] in relevant_nodes.keys():
        nodes[d[0]]=pls.node(relevant_nodes[d[0]]["index"],d[0][0],d[0][1],{k:relevant_nodes[d[0]][k] for k in relevant_nodes[d[0]].keys()})
    else:
        nodes[d[0]]=pls.node(str(list(pos_e.keys())[list(pos_e.values()).index(d[0])]),d[0][0],d[0][1],{})

#######################--------------------------------------------------##########################

#Pour all of the plastics (100) consecutively into the first 20 nodes of the water network. max value: size(nodes)-2
c=0
for plastic_unit in plastics_100:
    nodes[firstnode].insert_plastic(plastic_unit)
    plastic_unit.has_visited(nodes[firstnode])

#neighboring node.
# for node in G.nodes():
#     print("Neighbor:",tuple(nx.all_neighbors(G,node)), "of node:",tuple(node))
#     print("DEEEES MEEEEE",nodes[tuple(nx.all_neighbors(G,node))[0]].id, nodes[tuple(node)].id )
    # if c <= 18 :
    #     nodes[c].insert_plastic(plastic_unit)
    #     c+=1
    # else:
    #     nodes[c].insert_plastic(plastic_unit)
    #     c=0
###### Test of the methods of the classes ####
# plastics_100[0].coords()
# nodes[0].has_plastics_num()
# plastics_100[52].coords()
# plastics_100[52].find_in_node(nodes)
# nodes[31].has_plastics()
# print(nodes[0].fields['class'])
##############################################


sim.simulation(G,nodes,plastics_100)


#Display network graph figure
print(len(pos_n))
pos_pls = {k: v for k,v in enumerate(G.nodes())}
# pos_pls =  {k:v.coords() for k,v in enumerate(plastics_100)} # Get enumerated position of plastic units. Dictionary {0:(x1,y1),1:(x2,y2),...} 
pos_relabel = {k:v.has_plastics_num() for k,v in enumerate(nodes.values())} # Get enumerated amount of plastic units in nodes. Dictionary {0:5,1:4,2:0,..}
pos_node ={k:v.coords() for k,v in enumerate(nodes.values())} # Get enumerated position of nodes. Dictionary {0:(x0,y0),1:(x1,y1),...}


X=nx.DiGraph()
X.add_nodes_from(pos_pls.keys())
l = [set(x) for x in G.edges()]
edg=[tuple(k for k, v in pos_e.items() if v in s1 ) for s1 in l]


nx.draw_networkx_nodes(X, pos_pls,node_size=10)
nx.draw_networkx_labels(X, pos_node, labels=pos_relabel,font_size=16,horizontalalignment='right', verticalalignment='bottom')
X.add_edges_from(edg)
nx.draw_networkx_edges(X, pos_e)
plt.show()

