from __future__ import print_function, unicode_literals

from distributed.ttypes import Edge, Node

from sqlite3 import connect, IntegrityError, OperationalError

class GraphDatabaseHandler(object):
	def __init__(self):
		self.__database = connect("graphs.db")

		try:
			with open("create.sql") as script:
				self.__database.executescript( "".join(script) )

		except OperationalError: pass
		finally: self.__database.commit()

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.__database.close()

	def createNode(self, node):
		try:
			self.__database.execute("INSERT INTO nodes VALUES (?, ?, ?, ?)",
									 (node.id, node.color, node.description, node.weight))
		except IntegrityError: pass
		finally: self.__database.commit()

	def readNode(self, node_id):
		cursor = self.__database.cursor()
		cursor.execute("SELECT * FROM nodes WHERE id = ?", [node_id])
		data = cursor.fetchone()

		if data is not None: return Node(*data)
		else: return Node()

	def updateNode(self, node_id, color, description, weight):
		try:
			self.__database.execute("UPDATE nodes SET color = ?, description = ?, weight = ? WHERE id = ?",
									(color, description, weight, node_id))
		finally: self.__database.commit()

	def deleteNode(self, node_id):
		try:
			self.__database.execute("DELETE FROM nodes WHERE id = ?", [node_id])
			self.__database.execute("DELETE FROM edges WHERE node1 = ? or node2 = ?",
									(node_id, node_id))
		finally: self.__database.commit()

	def createEdge(self, edge):
		try:
			self.__database.execute("INSERT INTO edges VALUES (?, ?, ?, ?, ?)",
									 (edge.node1, edge.node2, edge.weight, edge.direction, edge.description))
		except IntegrityError: pass
		finally: self.__database.commit()

	def readEdge(self, node1, node2):
		cursor = self.__database.cursor()
		cursor.execute("SELECT * FROM edges WHERE node1 = ? and node2 = ?", (node1, node2))
		data = cursor.fetchone()

		if data is not None: return Edge(*data)
		else: return Edge()

	def updateEdge(self, node1, node2, weight, direction, description):
		try:
			self.__database.execute("UPDATE edges SET weight = ?, direction = ?, description = ? WHERE node1 = ? and node2 = ?",
									(weight, direction, description, node1, node2))
		finally: self.__database.commit()

	def deleteEdge(self, node1, node2):
		try:
			self.__database.execute("DELETE FROM edges WHERE node1 = ? or node2 = ?",
									(node1, node2))
		finally: self.__database.commit()

	def listNodesEdge(self, node1, node2):
		nodes = []
		cursor = self.__database.cursor()
		cursor.execute("SELECT * FROM edges WHERE node1 = ? and node2 = ?", (node1, node2))

		if cursor.fetchone() is not None:
			cursor.execute("SELECT * FROM nodes WHERE id = ?", [node1])
			nodes.append( Node( *cursor.fetchone() ) )

			cursor.execute("SELECT * FROM nodes WHERE id = ?", [node2])
			nodes.append( Node( *cursor.fetchone() ) )

		return nodes

	def listEdgesNode(self, node_id):
		cursor = self.__database.cursor()
		cursor.execute("SELECT * FROM edges WHERE node1 = ? or node2 = ?", (node_id, node_id))
		return [Edge(*data) for data in cursor]

	def listNeighborNodes(self, node_id):
		neighbors = []
		node_cursor = self.__database.cursor()
		edge_cursor = self.__database.cursor()
		edge_cursor.execute("SELECT node1, node2 FROM edges WHERE node1 = ? or node2 = ?",
							(node_id, node_id))

		for node1, node2 in edge_cursor:
			if node_id == node1:
				node_cursor.execute("SELECT * FROM nodes WHERE id = ?", [node2])
				neighbors.append( Node( *node_cursor.fetchone() ) )

			elif node_id == node2:
				node_cursor.execute("SELECT * FROM nodes WHERE id = ?", [node1])
				neighbors.append( Node( *node_cursor.fetchone() ) )

		return neighbors

if __name__ == '__main__':
	from thrift.transport.TSocket 		 import TServerSocket
	from thrift.transport.TTransport 	 import TBufferedTransportFactory
	from thrift.protocol.TBinaryProtocol import TBinaryProtocolFactory
	from thrift.server.TServer 			 import TForkingServer

	from distributed.Graph import Processor

	with GraphDatabaseHandler() as handler:
		processor	= Processor(handler)
		transport	= TServerSocket(port = 13579)
		tfactory	= TBufferedTransportFactory()
		pfactory	= TBinaryProtocolFactory()
		server		= TForkingServer(processor, transport, tfactory, pfactory)

		try: server.serve()
		except KeyboardInterrupt: pass
