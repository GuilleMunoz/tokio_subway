class Graph:

	def __init__(self):
		# graph[node] = {neighbour_1 : dist(node, neighbour), ...}
		self.graph = {}

	def get_neighbors(self, node):
		
		if node in self.graph:
			return self.graph[node]

		else:
			print('nodo %s no valido' % node)
			return -1

	def add_neighbor(self, node, neighbor, dist):
        
		self.graph[node][neighbor] = dist

	def set_neighbors(self, node, neighbors):

		self.graph[node] = neighbors

	def set_graph(self, graph):

		self.graph = graph

	def get_cost(self, node, next_node):
		return self.graph[node][next_node]

	def is_node(self, node):
		return node in self.graph