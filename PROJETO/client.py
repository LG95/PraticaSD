from __future__ import print_function, unicode_literals

def main(graphs):
	from random import choice, sample

	from distributed.ttypes import Edge, Node

	raw_input("Create?")

	ids = sample(xrange(1, 26), 10)

	for node_id in ids:
		graphs.createNode( Node(node_id, 0, "", 0.0) )

	for _ in xrange(50):
		graphs.createEdge( Edge(choice(ids), choice(ids), 0.0, False, "") )

	raw_input("Update?")

	for node_id in sample(ids, 5):
		graphs.updateNode(node_id, 1, "*", 1.0)

	for _ in xrange(25):
		graphs.updateEdge(choice(ids), choice(ids), 1.0, True, "*")

	raw_input("Delete?")

	for node_id in sample(ids, 5):
		graphs.deleteNode(node_id)

	for _ in xrange(10):
		graphs.deleteEdge(choice(ids), choice(ids))

	raw_input("Read?")

	for node_id in sample(ids, 5):
		node = graphs.readNode(node_id)
		if node.id is not None: print(node)

	for _ in xrange(25):
		edge = graphs.readEdge(choice(ids), choice(ids))
		if edge.node1 is not None: print(edge)

	raw_input("List?")

	for _ in xrange(50):
		nodes = graphs.listNodesEdge(choice(ids), choice(ids))
		if nodes != []: print(nodes)

	for node_id in sample(ids, 5):
		edges = graphs.listEdgesNode(node_id)
		if edges != []: print(edges)

	for node_id in sample(ids, 5):
		neighbors = graphs.listNeighborNodes(node_id)
		if neighbors != []: print(neighbors)

def example(client):
	from distributed.ttypes import Edge, Node

	raw_input("Create?")

	client.createNode( Node(0, 0, "A", 0.0) )
	client.createNode( Node(1, 0, "B", 0.0) )
	client.createNode( Node(2, 0, "C", 0.0) )
	client.createNode( Node(3, 0, "D", 0.0) )
	client.createNode( Node(4, 0, "E", 0.0) )
	client.createNode( Node(5, 0, "F", 0.0) )

	client.createEdge( Edge(0, 1, 0.0, False, "A-B") )
	client.createEdge( Edge(0, 2, 0.0, False, "A-C") )
	client.createEdge( Edge(1, 2, 0.0, False, "B-C") )
	client.createEdge( Edge(2, 3, 0.0, False, "C-D") )
	client.createEdge( Edge(3, 4, 0.0, False, "D-E") )
	client.createEdge( Edge(3, 5, 0.0, False, "D-F") )
	client.createEdge( Edge(4, 5, 0.0, False, "E-F") )

	raw_input("Read?")

	for i in range(6):
		print( client.readNode(i) )

	raw_input("List?")

	for i in range(6):
		print( client.listNeighborNodes(i) )

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
	example(client)
	transport.close()
