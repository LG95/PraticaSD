from __future__ import absolute_import, print_function, unicode_literals

from distributed.ttypes import Edge, Node

from sqlite3 import connect, IntegrityError, OperationalError

class Database(object):
	def __init__(self, name):
		self.__name = name

	def __enter__(self):
		self.__connection = connect(self.__name)
		return self.__connection

	def __exit__(self, except_type, except_value, except_traceback):
		if except_type is None: self.__connection.commit()
		else: self.__connection.rollback()
		self.__connection.close()

class GraphDatabaseHandler(object):
	def __init__(self):
		self.__database = Database("graphs.db")

		try:
			with open("create.sql") as script, self.__database as db:
				db.executescript( script.read() )

		except OperationalError: pass

	def __str__(self):
		with self.__database as db:
			cursor = db.cursor()
			cursor.execute("SELECT id from nodes")
			nodes = [row[0] for row in cursor]
			cursor.execute("SELECT node1, node2 from edges")
			edges = list(cursor)
			return "Nodes: {}\nEdges: {}".format(nodes, edges)

	def createNode(self, node):
		try:
			with self.__database as db:
				db.execute("INSERT INTO nodes VALUES (?, ?, ?, ?)",
							(node.id, node.color, node.description, node.weight))

		except IntegrityError: pass

	def readNode(self, node_id):
		with self.__database as db:
			cursor = db.cursor()
			cursor.execute("SELECT * FROM nodes WHERE id = ?", [node_id])
			data = cursor.fetchone()

			if data is not None: return Node(*data)
			else: return Node()

	def updateNode(self, node_id, color, description, weight):
		with self.__database as db:
			db.execute("UPDATE nodes SET color = ?, description = ?, weight = ? WHERE id = ?",
						(color, description, weight, node_id))

	def deleteNode(self, node_id):
		with self.__database as db:
			db.execute("DELETE FROM nodes WHERE id = ?", [node_id])
			db.execute("DELETE FROM edges WHERE node1 = ? or node2 = ?", (node_id, node_id))

	def createEdge(self, edge):
		try:
			with self.__database as db:
				db.execute("INSERT INTO edges VALUES (?, ?, ?, ?, ?)",
							(edge.node1, edge.node2, edge.weight, edge.direction, edge.description))

		except IntegrityError: pass

	def readEdge(self, node1, node2):
		with self.__database as db:
			cursor = db.cursor()
			cursor.execute("SELECT * FROM edges WHERE node1 = ? and node2 = ?", (node1, node2))
			data = cursor.fetchone()

			if data is not None: return Edge(*data)
			else: return Edge()

	def updateEdge(self, node1, node2, weight, direction, description):
		with self.__database as db:
			db.execute("UPDATE edges SET weight = ?, direction = ?, description = ? WHERE node1 = ? and node2 = ?",
						(weight, direction, description, node1, node2))

	def deleteEdge(self, node1, node2):
		with self.__database as db:
			db.execute("DELETE FROM edges WHERE node1 = ? or node2 = ?", (node1, node2))

	def listNodesEdge(self, node1, node2):
		with self.__database as db:
			nodes = []
			cursor = db.cursor()
			cursor.execute("SELECT * FROM edges WHERE node1 = ? and node2 = ?", (node1, node2))

			if cursor.fetchone() is not None:
				cursor.execute("SELECT * FROM nodes WHERE id = ?", [node1])
				nodes.append( Node( *cursor.fetchone() ) )

				cursor.execute("SELECT * FROM nodes WHERE id = ?", [node2])
				nodes.append( Node( *cursor.fetchone() ) )

		return nodes

	def listEdgesNode(self, node_id):
		with self.__database as db:
			cursor = db.cursor()
			cursor.execute("SELECT * FROM edges WHERE node1 = ? or node2 = ?", (node_id, node_id))
			return [Edge(*data) for data in cursor]

	def listNeighborNodes(self, node_id):
		with self.__database as db:
			neighbors = []
			edge_cursor = db.cursor()
			node_cursor = db.cursor()
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

if __name__ == "__main__":
	from thrift.transport.TSocket 		 import TServerSocket
	from thrift.transport.TTransport 	 import TBufferedTransportFactory
	from thrift.protocol.TBinaryProtocol import TBinaryProtocolFactory
	from thrift.server.TServer 			 import TThreadedServer

	from distributed.Graph import Processor

	handler		= GraphDatabaseHandler()
	processor	= Processor(handler)
	transport	= TServerSocket(port = 13579)
	tfactory	= TBufferedTransportFactory()
	pfactory	= TBinaryProtocolFactory()
	server		= TThreadedServer(processor, transport, tfactory, pfactory)

	try: server.serve()
	except KeyboardInterrupt: pass
	finally: print(handler)
