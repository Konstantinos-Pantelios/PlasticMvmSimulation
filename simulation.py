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
    for minute in range(150): # for every minute in an hour 
        #print("We are at the ",minute, "minute.")
        for plastic_unit in plastics: #for every plastic unit
            #print("We are at plastic:",plastic_unit)
            is_in_node = plastic_unit.find_in_node(nodes)
            if is_in_node:
                node_coords = is_in_node.coords()
                #neighbors = tuple(nx.all_neighbors(graph,node_coords)) # Tuple with all the neighbors of the current node ((x1,y1),...).
                succ=tuple(graph.successors(node_coords))
                pred=tuple(graph.predecessors(node_coords))
                neighbors={s:"S"for s in succ}
                neighbors.update({p:"P" for p in pred})

                for neigh in neighbors.keys():
                    #print("we are at neighbor:", nodes[neigh])
                    pred_succ = neighbors[neigh]
                    vector_wind = vectorize_byangle(wind_angle,node_coords,plastic_unit.wind_speed)
                    

                    if graph.nodes[neigh]['has_flow']:    
                        if pred_succ == "S":
                            vector_edge = vectorize_bycoords(node_coords,neigh)
                            edge_dir = math.atan2(vector_edge[1],vector_edge[0]) 
                            vector_flow = vectorize_byangle(edge_dir,node_coords,plastic_unit.flow_speed)
                            vector_forces = np.add(vector_wind,vector_flow) # On water"lines" that have flow direction and thus velocity we use the combined forces
                            relative_angle = relative_angle_wind(vector_edge,vector_forces)
                        elif pred_succ == "P":
                            vector_edge = vectorize_bycoords(neigh,node_coords)
                            edge_dir = math.atan2(vector_edge[1],vector_edge[0]) 
                            vector_flow = vectorize_byangle(edge_dir,node_coords,plastic_unit.flow_speed)
                            vector_forces = np.add(vector_wind,vector_flow) # On water"lines" that have flow direction and thus velocity we use the combined forces
                            vector_edge= vectorize_bycoords(node_coords,neigh)
                            relative_angle = relative_angle_wind(vector_edge,vector_forces)
                  
                    else: 
                        vector_edge = vectorize_bycoords(node_coords,neigh)
                        vector_forces = vector_wind # On water"lines" that have NO flow direction we only account for the wind acting upon the plastics
                        edge_dir = math.atan2(vector_edge[1],vector_edge[0])
                        relative_angle = relative_angle_wind(vector_edge,vector_forces)

                    
                    plastic_unit.velocity=round(np.linalg.norm(vector_forces),2) # calculate velocity based on the combined forces vector
                    distance = pls.distance(node_coords,neigh)
    
                    chance = random.randint(1,100)
                    
                    if relative_angle>=0 and relative_angle<=20:
                        if chance <= 95:
                            is_in_node.remove_plastic(plastic_unit)
                            #nodes[neigh].insert_plastic(plastic_unit)
                            plastic_unit.dist_to_node=distance-plastic_unit.velocity
                            plastic_unit.x = plastic_unit.velocity*math.sin(math.radians(edge_dir))+plastic_unit.x
                            plastic_unit.y = plastic_unit.velocity*math.cos(math.radians(edge_dir))+plastic_unit.y
                            plastic_unit.going_to = neigh
                            plastic_unit.direction = edge_dir
                            break
                    elif relative_angle>20 and relative_angle <=45:
                        if chance <= 60:
                            is_in_node.remove_plastic(plastic_unit)
                            #nodes[neigh].insert_plastic(plastic_unit)
                            plastic_unit.dist_to_node=distance-plastic_unit.velocity
                            plastic_unit.x = plastic_unit.velocity*math.sin(math.radians(edge_dir))+plastic_unit.x
                            plastic_unit.y = plastic_unit.velocity*math.cos(math.radians(edge_dir))+plastic_unit.y
                            plastic_unit.going_to = neigh
                            plastic_unit.direction = edge_dir
                            break
                    elif relative_angle>45 and relative_angle <=80:
                        if chance <= 40:
                            is_in_node.remove_plastic(plastic_unit)
                            #nodes[neigh].insert_plastic(plastic_unit)
                            plastic_unit.dist_to_node=distance-plastic_unit.velocity
                            plastic_unit.x = plastic_unit.velocity*math.sin(math.radians(edge_dir))+plastic_unit.x
                            plastic_unit.y = plastic_unit.velocity*math.cos(math.radians(edge_dir))+plastic_unit.y
                            plastic_unit.going_to = neigh
                            plastic_unit.direction = edge_dir
                            break    
                    elif relative_angle>80 and relative_angle <=90:
                        if chance <= 20:
                            is_in_node.remove_plastic(plastic_unit)
                            #nodes[neigh].insert_plastic(plastic_unit)
                            plastic_unit.dist_to_node=distance-plastic_unit.velocity
                            plastic_unit.x = plastic_unit.velocity*math.sin(math.radians(edge_dir))+plastic_unit.x
                            plastic_unit.y = plastic_unit.velocity*math.cos(math.radians(edge_dir))+plastic_unit.y
                            plastic_unit.going_to = neigh
                            plastic_unit.direction = edge_dir
                            break 
            else: 
                plastic_unit.dist_to_node -= plastic_unit.velocity 
                if plastic_unit.dist_to_node <= 0:
                    nodes[plastic_unit.going_to].insert_plastic(plastic_unit)
                    plastic_unit.x=plastic_unit.going_to[0]
                    plastic_unit.y=plastic_unit.going_to[1]
                else:
                    plastic_unit.x = plastic_unit.velocity*math.sin(math.radians(plastic_unit.direction))+plastic_unit.x
                    plastic_unit.y = plastic_unit.velocity*math.cos(math.radians(plastic_unit.direction))+plastic_unit.y
    
    return None