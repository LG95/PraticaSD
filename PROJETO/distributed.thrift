namespace py distributed

struct Node {
	1: i32 id,
	2: i32 color,
	3: string description,
	4: double weight
}

struct Edge {
	1: i32 node1,
	2: i32 node2,
	3: double weight,
	4: bool direction,
	5: string description
}

service Graph {
	bool createNode(1: Node node),
	Node readNode(1: i32 id),
	bool updateNode(1: i32 id, 2: i32 color, 3: string description,
					4: double weight),
	bool deleteNode(1: i32 id),
	bool createEdge(1: Edge edge),
	Edge readEdge(1: i32 node1, 2: i32 node2),
	bool updateEdge(1: i32 node1, 2: i32 node2, 3: double weight,
					4: bool direction, 5: string description),
	bool deleteEdge(1: i32 node1, 2: i32 node2),
	list<Node> listNodesEdge(1: i32 node1, 2: i32 node2),
	list<Edge> listEdgesNode(1: i32 id),
	list<Node> listNeighborNodes(1: i32 id)
}
