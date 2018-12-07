# Using here Kruskal Graph.
class KruskalGraph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = []  # creating an empty array to store the graph

    # this function adds an edge to graph
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # This method uses DSF with rank
    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        # high rank tree (Union by Rank)
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    # Here this is the main function that construct a minimum
    # spanning tree using Kruskal's algorithm

    def kruskal(self):

        result = []  # This will store the minimum spanning tree

        i = 0  # used for sorted edges
        val = 0

        # This sorts all the edges in non-decreasing
        # order of their weight.
        
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        # Creates V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while val < self.V - 1:

            # Picks the smallest edge and increments
            # the index for next iteration
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # If edge causes a cycle, don't keep
            if x != y:
                val = val + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
                # Edge that causes cycle is removed

        # prints what is in result[]
        print("Connected edges along with the weight")
        for u, v, weight in result:
            # print str(u) + " -- " + str(v) + " == " + str(weight)
            print("%d -- %d with weight %d" % (u, v, weight))


# Vertex class for topological sort
class Vertex:
    def __init__(self, label):
        self.label = label


# Graph created for topological sort
class TopologicalGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)


# This method gets the count for the number of edges coming in
def incoming_edge_count(edge_list, vertex):
    count = 0
    for (from_vertex, to_vertex) in edge_list:
        if to_vertex is vertex:
            count = count + 1
    return count


def topological_sort(graph):
    result_list = []

    # make list of vertices with no incoming edges.
    no_incoming_edges = []
    for vertex in graph.adjacency_list.keys():
        if incoming_edge_count(graph.edge_weights.keys(), vertex) == 0:
            no_incoming_edges.append(vertex)

    # remaining_edges starts with all edges in the graph.
    # A set is used for removal
    remaining_edges = set(graph.edge_weights.keys())
    while len(no_incoming_edges) != 0:
        # select the next vertex for the final result.
        current_vertex = no_incoming_edges.pop()
        result_list.append(current_vertex)
        outgoing_edges = []

        # removes current_vertex outgoing edges from remaining_edges
        for to_vertex in graph.adjacency_list[current_vertex]:
            outgoing_edge = (current_vertex, to_vertex)
            if outgoing_edge in remaining_edges:
                outgoing_edges.append(outgoing_edge)
                remaining_edges.remove(outgoing_edge)

        # checks to see if removing outgoing edges creates any new vertices
        for (from_vertex, to_vertex) in outgoing_edges:
            in_count = incoming_edge_count(remaining_edges, to_vertex)
            if in_count == 0:
                no_incoming_edges.append(to_vertex)

    return result_list
