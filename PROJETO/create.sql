CREATE TABLE nodes (
	id INTEGER PRIMARY KEY,
	color INTEGER,
	description TEXT,
	weight REAL
);

CREATE TABLE edges (
	node1 INTEGER,
	node2 INTEGER,
	weight REAL,
	direction INTEGER,
	description TEXT,
	FOREIGN KEY(node1) REFERENCES nodes(id),
	FOREIGN KEY(node2) REFERENCES nodes(id),
	PRIMARY KEY(node1, node2)
);
