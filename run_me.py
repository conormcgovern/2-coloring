import copy
import os

class Node:
    def __init__(self, id):
        self.id = id
        self.next = None


class Vertex:
    def __init__(self, id):
        self.id = id
        self.color = None
        # adj is a list containing the id's of the vertices neighbors
        self.adj = Queue()
        self.next = None
        # Parent is used to backtrack when getting the odd cycle
        self.parent = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.head == None

    def enqueue(self, node):
        if self.isEmpty():
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size+=1

    def dequeue(self):
        node = self.head
        if node.next == None:
            self.head = None
            self.tail = None
        else:
            self.head = node.next
        self.size-=1
        return node

# Creates an adjacency list.
# Each element in adj_list is a Vertex object.
# Each Vertex has a list of vertices that are adjacent to it. The list does not contain the actual Vertex objects.
# Instead, the list contains Node objects that hold the id of the vertex.
def initialize_graph(fname):
    fname_in = fname
    with open(fname_in, 'r') as f:
        n_vertices = int(f.readline().strip())
        adj_list = [None]*(n_vertices+1)
        for i in range(0, n_vertices+1):
            adj_list[i] = Vertex(i)
        for line in f:
            line = line.split()
            u = int(line[0])
            v = int(line[1])
            # Add v to u's list of adjacent vertices
            adj_list[u].adj.enqueue(Node(v))
            # Add u to v's list of adjacent vertices
            adj_list[v].adj.enqueue(Node(u))
    f.close()
    return adj_list


# Returns (False, v, u) if graph is not two colorable. Otherwise returns true
# v and u are the vertices where the cycle is found
def bfs(graph, source):
    # Initialize the queue
    q = Queue()
    # Initialize the source vertex
    s = graph[source]
    # Set source vertex color
    s.color = 0
    q.enqueue(s)
    while(q.isEmpty() == False):
        u = q.dequeue()
        u_color = u.color
        # Color to use for v (opposite color of u)
        v_color = (u_color + 1)%2
        # v = first node in u's list of adjacency vertices
        v = u.adj.head
        while(v != None):
            actual_node = graph[v.id]
            # If v has not yet been colored, color it with the opposite of u's color
            if actual_node.color == None:
                actual_node.color = v_color
                # Set v's parent to u. This will be used to backtrack when printing an odd cycle
                actual_node.parent = u
                q.enqueue(actual_node)
            # If v has already been colored with the same color as u, there exists an off cycle and the graph is not two colorable
            elif actual_node.color == u_color:
                return (False, actual_node, u)
            v = v.next
    # Return true if there are no odd cycles
    return (True, None, None)

# In case the graph is disconnected
# If the graph is connected then bfs will only be called once
def bfs_util(graph):
    for i in range(1, len(graph)):
        if graph[i].color == None:
            # Run the bfs with vertex i as the source if vertex i has not been discovered
            colorable, v, u = bfs(graph, i)
            if colorable == False:
                return (False, graph, v, u)
    return (True, graph, None, None)

# This is the main function
def color_graph(fname_in):
    # Initialize the adjacency list
    adj_list = initialize_graph(fname_in)
    # v and u are the vertices where the odd cycle (if exists) was found
    colorable, graph, v, u = bfs_util(adj_list)
    path = fname_in.split('/')
    # Output file name
    fname_out = 'results/' + path[len(path)-1] + 'output'
    with open(fname_out, 'w') as f:
        if colorable == True:
            f.write('True\n')
            # Write the coloring of each vertex to file
            for i in range(1, len(graph)):
                color = 'red' if graph[i].color == 0 else 'blue'
                f.write(str(graph[i].id) + ' ' + color + '\n')
        else:
            f.write('False\n')
            # Need these copies for the second while loop
            v_copy = copy.copy(v)
            u_copy = copy.copy(u)
            # Back track until reaching the common ancestor of u and v
            # Print v's path back to to common ancestor
            while v != u_copy:
                f.write(str(v.id) + ' -> ')
                v = v.parent
                u_copy = u_copy.parent
            f.write(str(v.id) + '\n')
            # Print u's path back to common ancestor
            while u != v_copy:
                f.write(str(u.id) + ' <- ')
                v_copy = v_copy.parent
                u = u.parent
            f.write('/')
    f.close()


# This exucutes the algorithm on each input graph
for file in os.listdir('./graphs'):
    color_graph('./graphs/' + file)
