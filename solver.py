"""
Implementation of Dijkstra's pathfinding algorithm for Python 2.x
Author: Stephen Thoma, 2012
"""

import os
import sys
import Queue as queue

INFINITY = 100000000
UNDEFINED = -1

class Node:
    """A connectable component in a graph representing a location."""
    def __init__(self, name):
        self.__cost = UNDEFINED # Cost to get to this node
        self.__connections = [] # List of connections leading from this node
        self.__name = name # String representing name identifier of node
        self.__edge_to_me = None # The edge taken to get to me

    def get_cost(self):
        """Get the cost associated with a Node."""
        return self.__cost

    def set_cost(self, cost):
        """Set the cost associated with a Node."""
        self.__cost = cost

    def get_connections(self):
        """Get the edges connected to a Node."""
        return self.__connections

    def add_connection(self, edge):
        """Add edges to a node"""
        self.__connections.append(edge)

    def compute_cost(self, edge_to_me):
        """Determine cost with the cost of the previous node and the 
        connecting edge.

        @param edge_to_me: The edge to be considered
        @type edge_to_me: Edge
        """
        node_that_got_to_me = edge_to_me.get_other_node(self)
        self.__cost = edge_to_me.get_cost() + node_that_got_to_me.get_cost()

    def get_name(self):
        """Get the name of the node.

        @return: The node's name
        @rtype: String
        """
        return self.__name

    def get_edge_to_me(self):
        """Retrieves edges connected to the node."""
        return self.__edge_to_me

    def set_edge_to_me(self, edge):
        """Connects an edge to a node.

        @param edge: The edge to be connected
        @type edge: Edge
        """
        self.__edge_to_me = edge

class Edge:
    """A connecting component between two nodes representing a path."""
    def __init__(self, start_node, end_node, cost):
        self.__start_node = start_node # The starting node of an edge
        self.__end_node = end_node # The ending node of an edge
        self.__cost = cost # The cost of going from an edge's start to its end

    def get_start_node(self):
        """Retrieves the starting node of the edge."""
        return self.__start_node

    def get_end_node(self):
        """Retrieves the ending node of an edge."""
        return self.__end_node

    def get_other_node(self, node):
        """Retrieves the node on the other side of the edge.

        @param node: The node on the starting side
        @type node: Node
        @return: The node on the ending side
        @rtype: Node
        """
        if node == self.get_start_node():
            return self.get_end_node()
        else:
            return self.get_start_node()

    def get_cost(self):
        """Retrieves the cost of traveling from the edge's start node to its
         end."""
        return self.__cost


class PossibleMove:
    """A move that could be taken, within the graph, from one node to another."""
    def __init__(self, start_node, edge):
        self.__start_node = start_node # The potential starting place
        self.__edge = edge # The edge that would be taken
        self.__cost = edge.get_cost() + start_node.get_cost() #The cost of the
        # edge and the starting node

    def start_node(self):
        """Returns the starting node of the possible move."""
        return self.__start_node

    def get_edge(self):
        """Returns the edge to be taken."""
        return self.__edge

    def get_cost(self):
        """Returns the cost of the possible move."""
        return self.__cost

    def __lt__(self, other):
        """Set the stack behavior."""
        return self.get_cost() < other.get_cost()


def ensure_node(graph, name):
    """Adds nodes not yet in graph to graph.

    @param graph: The object to be checked
    @type graph: Dictionary
    @param name: The name of node to be checked
    @type name: String
    @return: The node associated with the name
    @rtype: Node
    """
    if not name in graph:
        node = Node(name)
        graph[name] = node
    else:
        node = graph[name]

    return node


def get_graph_from_file(filename):
    """Retrieves the graph from a comma delimited file

    @param filename: The name of the file to be retrieved
    @type filename: String
    @return: Retrieved graph
    @rtype: Dictionary
    """
    with open(filename) as f:
        lines = list(f)

    graph = {}

    for line in lines:
        (start_city_name, end_city_name, cost) = line.split(",")

        start_city = ensure_node(graph, start_city_name)
        end_city = ensure_node(graph, end_city_name)

        start_city.add_connection(Edge(start_city, end_city, int(cost)))

    return graph


if __name__ == "__main__":

    # Check arguments
    if len(sys.argv) < 4:
        print("Usage: python solver.py [filename] [start city name]"
        + "[end city name]")
        sys.exit(0)

    start_node_name = sys.argv[2] # Strings
    end_node_name = sys.argv[3] # Strings

    try:
        graph = get_graph_from_file(sys.argv[1]) # Returns dictionary of
        # {String name : Node instance}
    except ValueError:
        print("Improperly formatted file.")
        sys.exit(0)
    except IOError:
        print("File not found.")
        sys.exit(0)

    for node in graph:
        graph[node].set_cost(INFINITY)

    start_node = graph[start_node_name]
    end_node = graph[end_node_name]

    start_node.set_cost(0)
    current_node = start_node

    possible_moves_queue = queue.PriorityQueue()

    while not current_node == end_node:

        # Add the current node's edges to the list of possible next edges
        for edge in current_node.get_connections():
            possible_moves_queue.put(PossibleMove(current_node, edge))

        # Get the edge and the node on the other side of the edge we are taking
        next_move = possible_moves_queue.get()
        next_edge = next_move.get_edge()
        next_node = next_edge.get_other_node(current_node)

        # Compute cost to the next node
        next_node.set_edge_to_me(next_edge)
        next_node.compute_cost(next_edge)

        current_node = next_node

    node_stack = []
    while current_node.get_edge_to_me() != None:
        node_stack.append(current_node)
        current_node = current_node.get_edge_to_me().get_other_node(current_node)

    while len(node_stack) > 0:
        current_node = node_stack.pop()
        print(current_node.get_name())
