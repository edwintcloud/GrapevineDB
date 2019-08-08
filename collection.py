from node import Node
from uuid import uuid4


class Collection(object):
    def __init__(self):
        """
        Initialize a graph object.

        Returns:
            (Graph): The initialized graph object.
        """
        self.nodes = {}
        self.num_nodes = 0
        self.num_labels = 0

    def __str__(self):
        nodes = [
            f"\n\t\t\t{k}: {{\n\t\t{str(v)}\n\t\t}}"
            for k, v in self.nodes.items()
        ]
        return "nodes: {{{}".format(",".join(nodes))

    def insert(self, data):
        """
        Insert an node into the collection

        Args:
            data (dict): The data of the node to create.

        Returns:
            (node): The node created.
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
