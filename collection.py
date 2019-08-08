from node import Node
from uuid import uuid4


class Collection:
    """
    A Collection is representative of a graph structure.
    """

    def __init__(self):
        """
        Initialize a Collection.

        Returns:
            (Collection): The initialized Collection object.
        """
        self.nodes = {}
        self.num_nodes = 0
        self.num_labels = 0

    def __str__(self):
        """
        Return the str representation of this Collection.

        Returns:
            (str): The str representation of this Collection.
        """
        nodes = [
            f"\n\t\t\t{k}: {{\n\t\t{str(v)}\n\t\t}}"
            for k, v in self.nodes.items()
        ]
        return "nodes: {{{}".format(",".join(nodes))

    def insert(self, data):
        """
        Insert an node into this collection.

        Args:
            data (dict): The data of the node to create.

        Returns:
            (Node): The node created.
        """

        # data must be of type dict
        if not isinstance(data, dict):
            raise Exception("data must be of type dict")

        # generate random uuid
        uuid = uuid4().hex

        # if the random uuid isn't so random (rare), try again until it is
        if uuid in self.nodes:
            while 1:
                uuid = uuid4().hex
                if uuid not in self.nodes:
                    break

        # insert the vertex into nodes
        self.nodes[uuid] = Node(uuid, data)

        # return the node
        return self.nodes[uuid]
