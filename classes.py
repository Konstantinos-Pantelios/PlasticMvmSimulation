class plastic:

    def __init__(self, id, x ,y):
        """ This is an object corresponding to units of plastic. 
        Currently (29-05-2021) its attributes are:
            id: An identification of the unit (it is NOT a primary key)
            x: X coordinate
            y: Y coordinate

        The clase has the following methods:
            coords: Returns the coordinates of the object as a tuple.
            find_in_node: Returns the node id that the plastic unit is currently in."""

        self.id = id
        self.x = x
        self.y = y
        self.prev_visit = None
        self.velocity = 5 # m per min

    def __str__(self):
        return ("<Plastic unit No"+str(self.id)+" (OBJECT stored in "+str(hex(id(self)))+")>")

    def coords(self):
        #print("The plastic unit "+str(self.id)+" is currently located at x:"+str(self.x)+", y:"+str(self.y)+".\n")
        return (self.x,self.y)

    def find_in_node(self, nodes):
        for node in nodes:
            if self in node.plastic_list:
                #print("Plastic unit with id:"+str(self.id)+" is in node:"+str(node.id)+"\n")
                return node.id 

    def has_visited(self,node):
        self.prev_visit = node
        return node            



class node:
    characteristics = ["Deadends","Junction"]
    def __init__(self, id, x, y, f):
        """ This is an object corresponding to nodes in a water network (or other).
        Currently (29-05-2021) its attributes are:
            id: An identification of the node (it is NOT a primary key)
            x: X coordinate
            y: Y coordinate
            plastic_list: a pre-empty list of plastic objects inside current node.

        The class has the following methods:
            coords: Returns the coordinates of the node in tuple format
            insert_plastic: Inserts a plastic object into the "plastic_list" list
            has_plastics_num: Returns the amount of plastic objects in the "plastic_list" list. 
            has_plastics: Return a list containing all the plastic unit objects that are inside the node.

        The class has the following attributes:
            characteristics = ["Deadends","Junction"]
        """

        self.id = id
        self.x = x
        self.y = y
        self.plastic_list=[]
        self.fields=f
        
    def __str__(self):
        return ("<Node No"+str(self.id)+" (OBJECT stored in "+str(hex(id(self)))+")>")

    def coords(self):
        #print("The node "+str(self.id)+" is located at x:"+str(self.x)+", y:"+str(self.y)+".\n")
        return (self.x,self.y)

    def insert_plastic(self, plastic):
        #print("Plastic of id:"+str(plastic.id)+" has been inserted to node:"+ str(self.id)+"\n")
        plastic.x = self.x
        plastic.y = self.y
        self.plastic_list.append(plastic)

    def has_plastics_num(self):
        pls_num = len(self.plastic_list)
        #print("The node "+str(self.id)+" has "+str(pls_num)+ " pieces of plastic in it.\n")
        return pls_num

    def has_plastics(self):
        pls = []
        for p in self.plastic_list: pls.append(p)
       # print("The node "+str(self.id)+" has the following pieces of plastic in it.")
        #print(pls)
        return pls


def show_fields(graph):
    """ The function shows and all of the availiable field stored in the edges and nodes of a graph.
            Input: A Graph
            Output: A tuple of lists of the fields of edges in position 0 and fields of nodes in position 1."""

    gr_fields=[]
    n_fields=[]
    print("The edges of the graph (from shp) have the following fields-attributes:")
    if graph.number_of_edges() != 0 : #It means that the graph contains edges
        for datadict in graph.edges.items():
            for key in datadict[1]:
                gr_fields.append(key)
            break
        print(gr_fields[:],"\n")
    else: print("There are NO fields-attributes stored in the edges. (EMPTY)\n")

    print("The nodes of the graph (from shp) have the following fields-attributes:")    
    if graph.number_of_nodes() != 0: #It means that the graph contains nodes
        for datadict in graph.nodes.items():
            for key in datadict[1]:
                n_fields.append(key)
            break
        if len(n_fields) == 0:
            print("There are NO fields-attributes stored in the nodes. (EMPTY)\n")
        else: print(n_fields[:],"\n")
    return (gr_fields, n_fields)

def create_plastics(amount):
    """ This function instantiates "amount" number of plastic unit objects.
    Input: Amount 
    Output: List of plastic unit objects"""
    pls=[]
    for i in range(amount):        
        pls.append(plastic(i,0,0))
    return pls

