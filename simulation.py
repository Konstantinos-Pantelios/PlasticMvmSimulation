import networkx as nx
import classes as pls

def simulation(graph,nodes,plastics):
    
    #plastics = [pls_object1, pls_object2,...]
    #nodes = {(x1,y1):pls_object1, (x2,y2):node_object2} Both relevant and irrelevant
    #graph = Graph
    #graph.nodes(data=True) = [((x1,y1),{}),((x2,y2),{}),...]
    #graph.edges(data=True) = [((x_start,y_start),(x_end,y_end),{.......}),....]
    wind_angle = 45 #in degrees fron North CW

    for minute in range(60): # for every minute in an hour 
        print("We are at the ",minute, "minute.")
        for plastic_unit in plastics: #for every plastic unit
            print("We are at plastic:",plastic_unit)
            is_in_node = plastic_unit.find_in_node(nodes)
            node_coords = is_in_node.coords()
            neighbors = tuple(nx.all_neighbors(graph,node_coords)) # Tuple with all the neighbors of the current node ((x1,y1),...).
            for neigh in neighbors:
                print("we are at neighbor:", nodes[neigh])
                distance = pls.distance(node_coords,neigh)
                edge_angle = pls.angle(node_coords,neigh)
                wind_angle=0
                relative_angle=0
                
                if edge_angle[1]==1:
                    relative_angle = abs(wind_angle - edge_angle[0])
                elif edge_angle[1]==2:
                    wind_angle=90-wind_angle
                    if wind_angle<0:
                        relative_angle = abs(360+wind_angle - edge_angle[0])
                    else:
                        relative_angle =  abs(wind_angle - edge_angle[0])
                elif edge_angle[1]==3:
                    wind_angle=180-wind_angle
                    if wind_angle<0:
                        relative_angle = abs(360+wind_angle - edge_angle[0])
                    else:
                        relative_angle =  abs(wind_angle - edge_angle[0])
                elif edge_angle[1]==4:
                    wind_angle=270-wind_angle
                    if wind_angle<0:
                        relative_angle = abs(360+wind_angle - edge_angle[0])
                    else:
                        relative_angle =  abs(wind_angle - edge_angle[0])        

                print("Positive",relative_angle,wind_angle, edge_angle)
                
                if relative_angle<=89:
                    is_in_node.remove_plastic(plastic_unit)
                    nodes[neigh].insert_plastic(plastic_unit)
                    break







        # for node in tuple(graph.nodes()):
        #     node_obj=nodes[node]
        #     if node_obj.has_plastics_num() > 0: # checkes if the current node object has any plastics in it.
        #         node_coords = node_obj.coords() # Coordinates of node (x,y) tuple.
        #         neighbors = tuple(nx.all_neighbors(graph,node)) # Tuple with all the neighbors of the current node ((x1,y1),...).
        #         for neigh in neighbors:
        #             distance = pls.distance(node_coords,neigh)
        #             relative_angle = abs(wind_angle - pls.angle(node_coords,neigh))
        #             #print('Distance',distance, "angle", relative_angle)
        #             if (relative_angle <= 89):
        #                 for plastic_unit in node_obj.has_plastics():
        #                     plastic_unit.dist_to_node = distance-plastic_unit.velocity
        #                     if plastic_unit.dist_to_node <= 0:
        #                         pass
                            # print("Plastic unit line17:",plastic_unit,"in node ", node_obj)
    
    return None