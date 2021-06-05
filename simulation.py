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

def move(plastic_obj,direction,distance,node,neighbor):
    node.remove_plastic(plastic_obj)
    plastic_obj.dist_to_node=distance-plastic_obj.velocity
    x0=plastic_obj.x
    y0=plastic_obj.y
    plastic_obj.x = plastic_obj.velocity*math.cos(direction)+x0 #
    plastic_obj.y = plastic_obj.velocity*math.sin(direction)+y0 #
    plastic_obj.going_to = neighbor
    plastic_obj.direction = direction
    plastic_obj.prev_visit = node

def forces_prob(relative_angle):
    if relative_angle>=0 and relative_angle<=20:
        return 95
    elif relative_angle>20 and relative_angle <=45:
        return 60
    elif relative_angle>45 and relative_angle <=80:
        return 45   
    elif relative_angle>80 and relative_angle <=90:
        return 20
    else: return 0

def simulation(graph,nodes,plastics,wind,drift):
    
    #plastics = [pls_object1, pls_object2,...]
    #nodes = {(x1,y1):pls_object1, (x2,y2):node_object2} Both relevant and irrelevant
    #graph = Graph
    #graph.nodes(data=True) = [((x1,y1),{}),((x2,y2),{}),...]
    #graph.edges(data=True) = [((x_start,y_start),(x_end,y_end),{.......}),....]
    #wind = int #in degrees fron North CW
    #drift = int #in degrees from North CW

    active_pls = [p for p in plastics if p.is_active]
    #print(active_pls)

    wind_angle = wind+drift # +degrees based on rule-of-thumb (literature)
    while len(active_pls)>0: # for every minute in an hour 
        print(active_pls)
        #print("We are at the ",minute, "minute.")
        for plastic_unit in active_pls: #for every plastic unit
            #print("We are at plastic:",plastic_unit)
            is_in_node = plastic_unit.find_in_node(nodes)
            plastic_unit.activation_time+=1
            #print(is_in_node)
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

                    
                    plastic_unit.velocity=np.linalg.norm(vector_forces) # calculate velocity based on the combined forces vector
                    
                    distance = math.dist(node_coords,neigh)
    
                    chance = random.randint(1,100)
                    wind_flow = forces_prob(relative_angle)
                    decision = wind_flow
                    if chance <= decision:
                        move(plastic_unit, edge_dir, distance, is_in_node, neigh)
                    if decision<=0:
                        plastic_unit.is_active = False 
                    break
                    
            else: 
                
                plastic_unit.dist_to_node -= plastic_unit.velocity 
                
                if plastic_unit.dist_to_node <= 1:
                    nodes[plastic_unit.going_to].insert_plastic(plastic_unit)
                    
                    plastic_unit.x=plastic_unit.going_to[0]
                    plastic_unit.y=plastic_unit.going_to[1]
                else:
                    x0=plastic_unit.x
                    y0=plastic_unit.y
                    plastic_unit.x = plastic_unit.velocity*math.cos(plastic_unit.direction)+x0
                    plastic_unit.y = plastic_unit.velocity*math.sin(plastic_unit.direction)+y0
        active_pls = [p for p in plastics if p.is_active]
    
    return None