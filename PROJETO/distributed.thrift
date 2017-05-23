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
	oneway void createNode(1: Node node),
	Node readNode(1: i32 id),
	oneway void updateNode(1: i32 id, 2: i32 color, 3: string description,
					4: double weight),
	oneway void deleteNode(1: i32 id),
	oneway void createEdge(1: Edge edge),
	Edge readEdge(1: i32 node1, 2: i32 node2),
	oneway void updateEdge(1: i32 node1, 2: i32 node2, 3: double weight,
					4: bool direction, 5: string description),
	oneway void deleteEdge(1: i32 node1, 2: i32 node2),
	list<Node> listNodesEdge(1: i32 node1, 2: i32 node2),
	list<Edge> listEdgesNode(1: i32 id),
	list<Node> listNeighborNodes(1: i32 id)
}
