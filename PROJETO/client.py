from __future__ import print_function, unicode_literals

def main(graphs):
	from random import choice, sample

	from distributed.ttypes import Edge, Node

	ids = sample(xrange(1, 26), 10)

	for node_id in ids:
		graphs.createNode( Node(node_id, 0, "", 0.0) )

	for _ in xrange(50):
		graphs.createEdge( Edge(choice(ids), choice(ids), 0.0, False, "") )

	for node_id in sample(ids, 5):
		graphs.updateNode(node_id, 1, "*", 1.0)

	for _ in xrange(25):
		graphs.updateEdge(choice(ids), choice(ids), 1.0, True, "*")

	for node_id in sample(ids, 5):
		graphs.deleteNode(node_id)

	for _ in xrange(10):
		graphs.deleteEdge(choice(ids), choice(ids))

	for node_id in sample(ids, 5):
		node = graphs.readNode(node_id)
		if node.id is not None: print(node)

	for _ in xrange(25):
		edge = graphs.readEdge(choice(ids), choice(ids))
		if edge.node1 is not None: print(edge)

	for _ in xrange(50):
		nodes = graphs.listNodesEdge(choice(ids), choice(ids))
		if nodes != []: print(nodes)

	for node_id in sample(ids, 5):
		edges = graphs.listEdgesNode(node_id)
		if edges != []: print(edges)

	for node_id in sample(ids, 5):
		neighbors = graphs.listNeighborNodes(node_id)
		if neighbors != []: print(neighbors)

if __name__ == '__main__':
	from thrift.transport.TSocket		 import TSocket
	from thrift.transport.TTransport	 import TBufferedTransport
	from thrift.protocol.TBinaryProtocol import TBinaryProtocol

	from distributed.Graph import Client

	transport	= TSocket('localhost', 13579)
	transport	= TBufferedTransport(transport)
	protocol	= TBinaryProtocol(transport)
	client		= Client(protocol)

	transport.open()
	main(client)
	transport.close()

	# from server import GraphDatabaseHandler

	# with GraphDatabaseHandler() as handler:
	# 	main(handler)
