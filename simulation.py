import math
import networkx as nx
import classes as pls
import random
import numpy as np
def vectorize_byangle(angle, p, magnitude):
    x2 = magnitude*math.sin(math.radians(angle))+p[0]
    y2 = magnitude*math.cos(math.radians(angle))+p[1]
    return np.subtract((x2,y2), p)

def vectorize_bycoords(p1, p2):

    return np.subtract(p2, p1)

def relative_angle_wind(edge,forces):
    norm = edge/np.linalg.norm(edge)
    return math.degrees(math.atan2(np.linalg.norm(np.cross(forces,norm)), np.dot(forces,norm)))



def simulation(graph,nodes,plastics,wind,drift):
    
    #plastics = [pls_object1, pls_object2,...]
    #nodes = {(x1,y1):pls_object1, (x2,y2):node_object2} Both relevant and irrelevant
    #graph = Graph
    #graph.nodes(data=True) = [((x1,y1),{}),((x2,y2),{}),...]
    #graph.edges(data=True) = [((x_start,y_start),(x_end,y_end),{.......}),....]
    #wind = int #in degrees fron North CW
    #drift = int #in degrees from North CW

    wind_angle = wind+drift # +degrees based on rule-of-thumb (literature)
    for minute in range(10): # for every minute in an hour 
        #print("We are at the ",minute, "minute.")
        for plastic_unit in plastics: #for every plastic unit
            #print("We are at plastic:",plastic_unit)
            is_in_node = plastic_unit.find_in_node(nodes)
            node_coords = is_in_node.coords()
            #neighbors = tuple(nx.all_neighbors(graph,node_coords)) # Tuple with all the neighbors of the current node ((x1,y1),...).
            succ=tuple(graph.successors(node_coords))
            pred=tuple(graph.predecessors(node_coords))
            neighbors={s:"S"for s in succ}
            neighbors.update({p:"P" for p in pred})

            for neigh in neighbors.keys():
                #print("we are at neighbor:", nodes[neigh])
                direction = neighbors[neigh]
                
                vector_wind = vectorize_byangle(wind_angle,node_coords,plastic_unit.wind_speed)
                if direction == "S":
                    vector_edge = vectorize_bycoords(node_coords,neigh)
                elif direction == "P":
                    vector_edge = vectorize_bycoords(neigh,node_coords)

                edge_dir = math.atan2(vector_edge[1],vector_edge[0])
                #if neigh has direction it means that it has flow so: vector_flow = vecorize_byangle(atan2(vector_edge[1],vector_edge[0]),neigh,plastic_unit.flow_speed else take into acount ONLY the wind)
                if graph.nodes[neigh]['has_flow']:                     
                    vector_flow = vectorize_byangle(edge_dir,node_coords,plastic_unit.flow_speed)
                    vector_forces = np.add(vector_wind,vector_flow)
                else: vector_forces = vector_wind
                
                relative_angle = relative_angle_wind(vector_edge,vector_forces)
                plastic_unit.velocity=round(np.linalg.norm(vector_forces),2)
                distance = pls.distance(node_coords,neigh)
                print(vector_forces,relative_angle)
 

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