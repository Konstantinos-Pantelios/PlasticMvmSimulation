import math
import random
import numpy as np
import classes as cl
#import main
import matplotlib.pyplot as plt

def vectorize_byangle(angle, p, magnitude):
    x2 = magnitude*math.sin(angle)+p[0]
    y2 = magnitude*math.cos(angle)+p[1]
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
    plastic_obj.x = plastic_obj.velocity*math.sin(direction)+x0 #
    plastic_obj.y = plastic_obj.velocity*math.cos(direction)+y0 #
    plastic_obj.going_to = neighbor
    plastic_obj.direction = direction
    plastic_obj.prev_visit = node

def forces_prob(relative_angle):
    if 0 <= relative_angle <= 10:
        return 100
    elif 10 < relative_angle <= 20:
        return 95
    elif 20 < relative_angle <=45:
        return 60
    elif 45 < relative_angle <=80:
        return 45   
    elif 80 < relative_angle <=90:
        return 20
    else: return 0


def simulation(graph,nodes,plastics,wind,drift):
    
    #nodes = {(x1,y1):pls_object1, (x2,y2):node_object2} Both relevant and irrelevant
    #graph = Graph
    #graph.nodes(data=True) = [((x1,y1),{}),((x2,y2),{}),...]
    #graph.edges(data=True) = [((x_start,y_start),(x_end,y_end),{.......}),....]
    #plastics = [pls_object1, pls_object2,...]
    #wind = int #in degrees fron North CW
    #drift = int #in degrees from North CW


    active_plastics = [p for p in plastics if p.is_active]

    wind_angle = wind+drift # +degrees based on rule-of-thumb (literature)
    
                                           # IMPORTANT!:
    while len(active_plastics)>0:          # Comment/Uncomment this line to run until all plastics exit the simulation
    #for m in range(1,80):                 # Comment/Uncomment this line to set specific time extention to the simulation. NOTE: Might need some modification in order to write the output successfuly.
        #print("We are at the ",minute, "minute.")
        print(active_plastics[0].activation_time, "minutes have passed")
        # if active_plastics[0].activation_time%1 == 0:
        #     pass
        #     #main.plot_end(nodes,plastics)
        #     #plt.show()

        active_plastics = [p for p in plastics if p.is_active]
        #print(len(active_plastics))
        for plastic_unit in active_plastics: #for every plastic unit

            #print("We are at plastic:",plastic_unit)
            plastic_unit.activation_time+=1
            
            is_in_node = plastic_unit.find_in_node(nodes) # Plastic is in a specific node (Node object) OR is free roaming (None).
            if is_in_node:
                node_coords = is_in_node.coords()           # Coordinates of the node that the current plastic is in. 
                succ=tuple(graph.successors(node_coords))   # Tuple containing all Succesor nodes 
                pred=tuple(graph.predecessors(node_coords)) # Tuple containing all Predecessor nodes.
                
                
                neighbors={s:"S"for s in succ if s!=node_coords}    #ISSUE: Condition to exclude a neighboring node being the same as the current node. Checked and cleaned duplicate nodes but didnt fix the issue 
                neighbors.update({p:"P" for p in pred if p!=node_coords})     # Dictionary containing both Successor and Predecessor nodes {(x0,y0):"S",...}
                
                if is_in_node.fields['class'] == "Deadend" and plastic_unit.prev_visit: # Check if the plastic unit REACHED a deadend node. The condition doesn't include plastic STARTING from deadends.
                    plastic_unit.is_active = False # Exit the simulation from current node.
                    continue

                neigh_count = 0 # Number of neighbor checked for 0 probability of movement.
                for neigh in neighbors.keys():              # Checking all neighbors ( both Predecessors and Successors)
                    neigh_count_t = len(neighbors.keys())   # Number of neighbors

                    #print("we are at neighbor:", nodes[neigh])
                    pred_succ = neighbors[neigh]    # Value ("S" or "P") containg current neighbor (Predecessor or Successor) 
                    
                    vector_wind = vectorize_byangle(math.radians(wind_angle),node_coords,plastic_unit.wind_speed) #Vectorize the wind by its direction, velocity and current node origin point
                    
                    if graph.nodes[neigh]['has_flow'] == 'true':  # Precessors and Successor nodes are only relevant if there exist meaningfull directional information      
                        if pred_succ == "S":            # Successor node vector needs to be vectorized as an edge starting from current node and pointing to Successor node
                            vector_edge = vectorize_bycoords(node_coords,neigh) 
                            edge_dir = math.atan2(vector_edge[1],vector_edge[0]) 
                            vector_flow = vectorize_byangle(edge_dir,node_coords,plastic_unit.flow_speed)
                            vector_forces = np.add(vector_wind,vector_flow) # On water"lines" that have flow direction and thus velocity we use the combined forces
                            relative_angle = relative_angle_wind(vector_edge,vector_forces)
                        elif pred_succ == "P":          # Predecessor node vector needs to be vectorized as an edge starting from Predecessor node and pointing to current node. 
                            vector_edge = vectorize_bycoords(neigh,node_coords)
                            edge_dir = math.atan2(vector_edge[1],vector_edge[0]) 
                            vector_flow = vectorize_byangle(edge_dir,node_coords,plastic_unit.flow_speed)
                            vector_forces = np.add(vector_wind,vector_flow) # On water"lines" that have flow direction and thus velocity we use the combined forces
                            vector_edge= vectorize_bycoords(node_coords,neigh)
                            relative_angle = relative_angle_wind(vector_edge,vector_forces)
                        else:
                            print("Other value than S or P")

                  
                    else: 

                        vector_edge = vectorize_bycoords(node_coords,neigh)
                        vector_forces = vector_wind # On water"lines" that have NO flow direction we only account for the wind acting upon the plastics
                        edge_dir = math.atan2(vector_edge[1],vector_edge[0])
                        relative_angle = relative_angle_wind(vector_edge,vector_forces)

                    
                    plastic_unit.velocity=np.linalg.norm(vector_forces) # Calculate velocity based on the combined forces vector
                    distance = cl.distance(node_coords,neigh) # EU Distance betwwen current and neighbor nodes.
    

#################### Decision making #######################################    
                    chance = random.randint(1,100)  # Rolling the 100-sided dice
                    
                    # Probability based on the relative angle between the forces acting upon plastics and the canal direction
                    wind_flow = forces_prob(relative_angle) 
                    
                    # Probability based on hard_turn               
                    decision = wind_flow # Overall probaility of the plastic moving towards neighboring node or staying apeak
                    
                    if chance <= decision:
                        move(plastic_unit, edge_dir, distance, is_in_node, nodes[neigh]) # Plastics moves towards neighboring node
                        break
                    if decision<=0: # Plastic stays on current node.
                        neigh_count+=1
                        if neigh_count == neigh_count_t:
                            plastic_unit.is_active = False # Plastics that probability of moving to any neighboring node was found to be 0 exits the simulation 
                        else: continue # Probability was found to be 0 but there are other routes to check before determining the plastic stack.
#############################################################################
            else: 
                
                if plastic_unit.dist_to_node <= 1: # Plastic has reached or almost reached its destination 
                    # plastic_unit.x=plastic_unit.going_to[0]
                    # plastic_unit.y=plastic_unit.going_to[1]
                    # Updating the coordinates happens in "insert_plastic" method.
                    plastic_unit.going_to.insert_plastic(plastic_unit)

                else:
                    plastic_unit.dist_to_node -= plastic_unit.velocity
                    if not plastic_unit.dist_to_node <= 1: # Plastic HASN'T reached its destination
                        # Update plastic position based on its current position, its velocity and the direction of the canal on which it floats.
                        x0=plastic_unit.x
                        y0=plastic_unit.y
                        plastic_unit.x = plastic_unit.velocity*math.sin(plastic_unit.direction)+x0
                        plastic_unit.y = plastic_unit.velocity*math.cos(plastic_unit.direction)+y0
        
    return None