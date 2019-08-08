from queue import SimpleQueue


class Node:
    """
    A node is representative of the vertices in a graph.
    """

    def __init__(self, uuid, data):
        """
        Initialize a Node object with uuid and data.

        Args:
            uuid (str): The uuid of the Node to be created.
            data (dict): The data to be assigned to the Node.

        Returns:
            (Node): The initialized Node object.
        """
        self.id = uuid
        self.data = data
        self.relations = {}

    def __str__(self):
        """
        Return the str representation of this Node object.

        Returns:
            (str): The str representation of this Node object.
        """
        return "id: {}, data: {}, relations: {}".format(
            self.id, str(self.data), str(self.relations)
        )

    def to_dict(self):
        """
        Return the dict representation of this Node object.

        Return:
            (dict): The dict representation of this Node object.
        """
        return {"id": self.id, "data": self.data, "relations": self.relations}

    def relate_to(self, node, by=None, bidirectional=False):
        """
        Create a relation between this Node and another Node object.

        Args:
            node (Node): The other Node object to create a relation to.
            by (any|None): The label to assign to the newly established
            relation.
            bidirectional (bool|False): If True, the relation will be created
            both ways (from this Node to node and from node to this Node).

        Raises:
            Exception: If node is not of type Node.
            Exception: If specified relation already exists on this Node.
        """
        # node must be of type Node
        if not isinstance(node, Node):
            raise Exception("node must be a node object")

        # edge must not already exist
        if node in self.relations:
            raise Exception(
                "{} is already related to {} by label {}".format(
                    self.id, node.id, by
                )
            )
        if self in node.relations and bidirectional:
            raise Exception(
                "{} is already related to {} by label {}".format(
                    node.id, self.id, by
                )
            )

        # add edge to node
        self.relations[node] = by
        if bidirectional:
            node.relations[self] = by

    def related_by(self, label):
        """
        Return a list of nodes related to this Node by
        label.

        Args:
            label (any): The label of the relation to search for.

        Returns:
            (list): List of Node objects related to this Node by label.
        """

        return [n for n, l in self.relations.items() if l == label]

    def related_difference(self, label_1, label_2):
        """
        Return a dict of nodes that are directly related by label_1
        and indirectly related by label_2. The value will be the
        number of times this indirect relation is found.

        Args:
            label_1 (any): The label of the direct relation to this Node.
            label_2 (any): The label of the indirect relations to find
            that are connected to this Node.
        
        Returns:
            (dict): A dict of Node(s) that are indirectly related by label_2
            and directly related by label_1. The value corresponding to each
            Node will be the number of times it is connected (degree of
            relation).
        """

        # build stack of nodes related to current
        # node by label_1
        stack = [n for n, l in self.relations.items() if l == label_1]

        # if stack is empty, no direct relation by label_1 exists,
        # return empty list
        if len(stack) == 0:
            return []

        # create needed structures
        result = {}
        visited = set([self])
        direct_relations = set([self] + stack)

        # while there are nodes in the stack
        while stack:
            # pop a node from the stack
            node = stack.pop()
            # if the node has not been visited
            if node not in visited:
                # mark it as visited
                visited.add(node)
                # iterate through its relations
                for relation, label in node.relations.items():
                    # add each relation to the stack
                    stack.append(relation)
                    # if the label is equal to label_2, add the node to result
                    if label == label_2 and relation not in direct_relations:
                        if relation in result:
                            result[relation] += 1
                        else:
                            result[relation] = 1

        # return resulting list of nodes
        return result
