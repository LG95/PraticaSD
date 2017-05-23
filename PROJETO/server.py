from __future__ import print_function, unicode_literals

from distributed.ttypes import Edge, Node

class GraphDatabaseHandler(object):
	def __init__(self):
		self.__nodes = dict()
		self.__edges = dict()

	def __repr__(self):
		return "Nodes = {}\nEdges = {}".format(self.__nodes, self.__edges)

	def createNode(self, node):
		if node.id not in self.__nodes:
			self.__nodes[node.id] = node
			return True

		else: return False

	def readNode(self, node_id):
		try: return self.__nodes[node_id]
		except KeyError: return Node()

	def updateNode(self, node_id, color, description, weight):
		if node_id in self.__nodes:
			self.__nodes[node_id].color = color
			self.__nodes[node_id].description = description
			self.__nodes[node_id].weight = weight
			return True

		else: return False

	def deleteNode(self, node_id):
		try:
			self.__nodes.pop(node_id)

			for edge in self.__edges.keys():
				if node_id in edge:
					self.__edges.pop(edge)

			return True

		except KeyError: return False

	def createEdge(self, edge):
		key = (edge.node1, edge.node2)

		if edge.node1 in self.__nodes and edge.node2 in self.__nodes and key not in self.__edges:
			self.__edges[key] = edge
			return True

		else: return False

	def readEdge(self, node1, node2):
		try: return self.__edges[ (node1, node2) ]
		except KeyError: return Edge()

	def updateEdge(self, node1, node2, weight, direction, description):
		key = (node1, node2)

		if key in self.__edges:
			self.__edges[key].description = description
			self.__edges[key].direction = direction
			self.__edges[key].weight = weight
			return True

		else: return False

	def deleteEdge(self, node1, node2):
		try:
			self.__edges.pop( (node1, node2) )
			return True

		except KeyError: return False

	def listNodesEdge(self, node1, node2):
		key = (node1, node2)
		if key in self.__edges: return [self.__nodes[node1], self.__nodes[node2]]
		else: return []

	def listEdgesNode(self, node_id):
		return [self.__edges[edge] for edge in self.__edges.keys() if node_id in edge]

	def listNeighborNodes(self, node_id):
		neighbors = []

		for node1, node2 in self.__edges.keys():
			if node_id == node1:
				neighbors.append(node2)

			elif node_id == node2:
				neighbors.append(node1)

		return neighbors

if __name__ == '__main__':
	from thrift.transport.TSocket 			import TServerSocket
	from thrift.transport.TTransport 		import TBufferedTransportFactory
	from thrift.protocol.TBinaryProtocol 	import TBinaryProtocolFactory
	from thrift.server.TServer 				import TSimpleServer

	from distributed.Graph import Processor

	processor = Processor( GraphDatabaseHandler() )
	transport = TServerSocket(port = 13579)
	tfactory = TBufferedTransportFactory()
	pfactory = TBinaryProtocolFactory()
	server = TSimpleServer(processor, transport, tfactory, pfactory)

	try: server.serve()
	except KeyboardInterrupt: pass
	finally: print('Good bye!')
