import math
import networkx as nx
from numpy.core.fromnumeric import size
import classes as pls
import random
import numpy as np

def simulation(graph,nodes,plastics,wind):
    
    #plastics = [pls_object1, pls_object2,...]
    #nodes = {(x1,y1):pls_object1, (x2,y2):node_object2} Both relevant and irrelevant
    #graph = Graph
    #graph.nodes(data=True) = [((x1,y1),{}),((x2,y2),{}),...]
    #graph.edges(data=True) = [((x_start,y_start),(x_end,y_end),{.......}),....]
    #wind_angle = 30 #in degrees fron North CW

    for minute in range(60): # for every minute in an hour 
        print("We are at the ",minute, "minute.")
        for plastic_unit in plastics: #for every plastic unit
            print("We are at plastic:",plastic_unit)
            is_in_node = plastic_unit.find_in_node(nodes)
            node_coords = is_in_node.coords()
            neighbors = tuple(nx.all_neighbors(graph,node_coords)) # Tuple with all the neighbors of the current node ((x1,y1),...).
            for neigh in neighbors:
                #print("we are at neighbor:", nodes[neigh])
                wind_angle = wind
                wind_x2 = 1*math.sin(math.radians(wind_angle))+node_coords[0]
                wind_y2 = 1*math.cos(math.radians(wind_angle))+node_coords[1]
                vector_wind =  np.subtract((wind_x2,wind_y2), node_coords)
                vector_edge = np.subtract(neigh, node_coords)
                norm = vector_edge/np.linalg.norm(vector_edge)

                relative_angle=math.degrees(math.atan2(np.linalg.norm(np.cross(vector_wind,norm)), np.dot(vector_wind,norm)))

                
                distance = pls.distance(node_coords,neigh)
 

                #print("Positive",relative_angle, "Wind angle",wind_angle, )
                chance = random.randint(1,100)
                
                if relative_angle>=0 and relative_angle<=20:
                    if chance <= 95:
                        is_in_node.remove_plastic(plastic_unit)
                        nodes[neigh].insert_plastic(plastic_unit)
                        break
                elif relative_angle>20 and relative_angle <=45:
                    if chance <= 60:
                        is_in_node.remove_plastic(plastic_unit)
                        nodes[neigh].insert_plastic(plastic_unit)
                        break
                elif relative_angle>45 and relative_angle <=80:
                    if chance <= 40:
                        is_in_node.remove_plastic(plastic_unit)
                        nodes[neigh].insert_plastic(plastic_unit)
                        break    
                elif relative_angle>80 and relative_angle <=90:
                    if chance <= 20:
                        print("HERE", relative_angle)
                        is_in_node.remove_plastic(plastic_unit)
                        nodes[neigh].insert_plastic(plastic_unit)
                        break 
                #elif relative_angle 







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