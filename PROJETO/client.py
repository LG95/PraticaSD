from __future__ import absolute_import, print_function, unicode_literals

from distributed.ttypes import Edge, Node

def test(graphs):
	from random import choice, sample

	raw_input("Create?")

	ids = sample(range(1, 26), 10)

	for node_id in ids:
		graphs.createNode( Node(node_id, 0, "", 0.0) )

	for _ in range(50):
		graphs.createEdge( Edge(choice(ids), choice(ids), 0.0, False, "") )

	raw_input("Update?")

	for node_id in sample(ids, 5):
		graphs.updateNode(node_id, 1, "*", 1.0)

	for _ in range(25):
		graphs.updateEdge(choice(ids), choice(ids), 1.0, True, "*")

	raw_input("Delete?")

	for node_id in sample(ids, 5):
		graphs.deleteNode(node_id)

	for _ in range(10):
		graphs.deleteEdge(choice(ids), choice(ids))

	raw_input("Read?")

	for node_id in sample(ids, 5):
		node = graphs.readNode(node_id)
		if node.id is not None: print(node)

	for _ in range(25):
		edge = graphs.readEdge(choice(ids), choice(ids))
		if edge.node1 is not None: print(edge)

	raw_input("List?")

	for _ in range(50):
		nodes = graphs.listNodesEdge(choice(ids), choice(ids))
		if nodes != []: print(nodes)

	for node_id in sample(ids, 5):
		edges = graphs.listEdgesNode(node_id)
		if edges != []: print(edges)

	for node_id in sample(ids, 5):
		neighbors = graphs.listNeighborNodes(node_id)
		if neighbors != []: print(neighbors)

def example(graphs):
	raw_input("Create?")

	graphs.createNode( Node(0, 0, "A", 0.0) )
	graphs.createNode( Node(1, 0, "B", 0.0) )
	graphs.createNode( Node(2, 0, "C", 0.0) )
	graphs.createNode( Node(3, 0, "D", 0.0) )
	graphs.createNode( Node(4, 0, "E", 0.0) )
	graphs.createNode( Node(5, 0, "F", 0.0) )

	graphs.createEdge( Edge(0, 1, 0.0, False, "A-B") )
	graphs.createEdge( Edge(0, 2, 0.0, False, "A-C") )
	graphs.createEdge( Edge(1, 2, 0.0, False, "B-C") )
	graphs.createEdge( Edge(2, 3, 0.0, False, "C-D") )
	graphs.createEdge( Edge(3, 4, 0.0, False, "D-E") )
	graphs.createEdge( Edge(3, 5, 0.0, False, "D-F") )
	graphs.createEdge( Edge(4, 5, 0.0, False, "E-F") )

	raw_input("Read?")

	for i in range(6):
		print( graphs.readNode(i) )

	raw_input("List?")

	for i in range(6):
		print( graphs.listNeighborNodes(i) )

if __name__ == "__main__":
	from thrift.transport.TSocket		 import TSocket
	from thrift.transport.TTransport	 import TBufferedTransport
	from thrift.protocol.TBinaryProtocol import TBinaryProtocol

	from distributed.Graph import Client

	transport	= TSocket("localhost", 13579)
	transport	= TBufferedTransport(transport)
	protocol	= TBinaryProtocol(transport)
	client		= Client(protocol)

	transport.open()
	try: example(client)
	finally: transport.close()
