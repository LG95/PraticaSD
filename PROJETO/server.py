from __future__ import print_function, unicode_literals

from distributed.ttypes import Edge, Node

from sqlite3 import connect, IntegrityError, OperationalError

class GraphDatabaseHandler(object):
	def __init__(self):
		from threading import Lock

		self.__database = connect(":memory:")
		self.__lock = Lock()

	def __enter__(self):
		from os.path import isfile

		try:
			if isfile("graph.db"):
				database = connect("graph.db")
				script = "\n".join( database.iterdump() )
				with self.__database: self.__database.executescript(script)
				database.close()

			else:
				with self.__database:
					with open("create.sql") as script:
						self.__database.executescript( script.read() )

		except OperationalError: pass	# as e: print(e)
		finally: return self

	def __exit__(self, *args):
		with open("graph.db", "w"): pass
		database = connect("graph.db")
		script = "\n".join( self.__database.iterdump() )
		with database: database.executescript(script)
		self.__database.close()
		database.close()

	def createNode(self, node):
		with self.__lock:
			try:
				with self.__database:
					self.__database.execute("INSERT INTO nodes VALUES (?, ?, ?, ?)",
											 (node.id, node.color, node.description, node.weight))
			except IntegrityError: pass	# as e: print(e)

	def readNode(self, node_id):
		with self.__lock:
			cursor = self.__database.cursor()
			cursor.execute("SELECT * FROM nodes WHERE id = ?", [node_id])
			data = cursor.fetchone()

			if data is not None: return Node(*data)
			else: return Node()

	def updateNode(self, node_id, color, description, weight):
		with self.__lock:
			with self.__database:
				self.__database.execute("UPDATE nodes SET color = ?, description = ?, weight = ? WHERE id = ?",
										(color, description, weight, node_id))

	def deleteNode(self, node_id):
		with self.__lock:
			with self.__database:
				self.__database.execute("DELETE FROM nodes WHERE id = ?", [node_id])
				self.__database.execute("DELETE FROM edges WHERE node1 = ? or node2 = ?",
										(node_id, node_id))

	def createEdge(self, edge):
		with self.__lock:
			try:
				with self.__database:
					self.__database.execute("INSERT INTO edges VALUES (?, ?, ?, ?, ?)",
											 (edge.node1, edge.node2, edge.weight, edge.direction, edge.description))
			except IntegrityError: pass	# as e: print(e)

	def readEdge(self, node1, node2):
		with self.__lock:
			cursor = self.__database.cursor()
			cursor.execute("SELECT * FROM edges WHERE node1 = ? and node2 = ?", (node1, node2))
			data = cursor.fetchone()

			if data is not None: return Edge(*data)
			else: return Edge()

	def updateEdge(self, node1, node2, weight, direction, description):
		with self.__lock:
			with self.__database:
				self.__database.execute("UPDATE edges SET weight = ?, direction = ?, description = ? WHERE node1 = ? and node2 = ?",
										(weight, direction, description, node1, node2))

	def deleteEdge(self, node1, node2):
		with self.__lock:
			with self.__database:
				self.__database.execute("DELETE FROM edges WHERE node1 = ? or node2 = ?",
										(node1, node2))

	def listNodesEdge(self, node1, node2):
		with self.__lock:
			nodes = []
			cursor = self.__database.cursor()
			cursor.execute("SELECT * FROM edges WHERE node1 = ? and node2 = ?", (node1, node2))

			if cursor.fetchone() is not None:
				for node in (node1, node2):
					cursor.execute("SELECT * FROM nodes WHERE id = ?", [node])
					nodes.append( Node( *cursor.fetchone() ) )

			return nodes

	def listEdgesNode(self, node_id):
		with self.__lock:
			cursor = self.__database.cursor()
			cursor.execute("SELECT * FROM edges WHERE node1 = ? or node2 = ?", (node_id, node_id))
			return [Edge(*data) for data in cursor]

	def listNeighborNodes(self, node_id):
		with self.__lock:
			neighbors = []
			cursor = self.__database.cursor()
			cursor.execute("SELECT node1, node2 FROM edges WHERE node1 = ? or node2 = ?",
								(node_id, node_id))

			for node1, node2 in list(cursor):
				if node_id == node1:
					cursor.execute("SELECT * FROM nodes WHERE id = ?", [node2])
					neighbors.append( Node( *cursor.fetchone() ) )

				elif node_id == node2:
					cursor.execute("SELECT * FROM nodes WHERE id = ?", [node1])
					neighbors.append( Node( *cursor.fetchone() ) )

			return neighbors

if __name__ == '__main__':
	from thrift.transport.TSocket 		 import TServerSocket
	from thrift.transport.TTransport 	 import TBufferedTransportFactory
	from thrift.protocol.TBinaryProtocol import TBinaryProtocolFactory
	from thrift.server.TServer 			 import TSimpleServer

	from distributed.Graph import Processor

	with GraphDatabaseHandler() as handler:
		processor	= Processor(handler)
		transport	= TServerSocket(port = 13579)
		tfactory	= TBufferedTransportFactory()
		pfactory	= TBinaryProtocolFactory()
		server		= TSimpleServer(processor, transport, tfactory, pfactory)

		try: server.serve()
		except KeyboardInterrupt: pass
