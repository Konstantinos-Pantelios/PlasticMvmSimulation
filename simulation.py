import networkx as nx
import classes as pls

def simulation(graph,nodes,plastics):
    
    #plastics = {(x1,y1):pls_object1, (x2,y2):pls_object2}
    #nodes = {(x1,y1):pls_object1, (x2,y2):node_object2} Both relevant and irrelevant
    #graph = Graph
    #graph.nodes(data=True) = [((x1,y1),{}),((x2,y2),{}),...]
    #graph.edges(data=True) = [((x_start,y_start),(x_end,y_end),{.......}),....]

    for minute in range(60): # for every minute in an hour 
        print("We are at the ",minute, "minute.")
        for node in tuple(graph.nodes()):
            node_obj=nodes[node]
            if node_obj.has_plastics_num() > 0: # checkes if the current node object has any plastics in it.
                node_coords = node_obj.coords() # Coordinates of node (x,y) tuple.
                neighbors = tuple(nx.all_neighbors(graph,node)) # Tuple with all the neighbors of the current node ((x1,y1),...).
                for plastic_unit in node_obj.has_plastics():
                    print("Plastic unit line17:",plastic_unit,"in node ", node_obj)
    
    return None