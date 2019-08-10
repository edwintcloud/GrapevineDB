from node import Node
from uuid import uuid4
from file_ops import FileOps


class Collection(FileOps):
    """
    A Collection is representative of a graph structure.
    """

    def __init__(self, file):
        """
        Initialize a Collection.

        Returns:
            (Collection): The initialized Collection object.
        """
        self.nodes = {}
        self.file = file

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

    @FileOps.save_on_update
    def insert(self, data, key=None):
        """
        Insert a node into this collection.

        Args:
            data (dict): The data of the node to create.
            key (any|None): If specified, the key of the Node inserted will
            be a key and not uuid.

        Returns:
            (Node): The node created.
        """

        # data must be of type dict
        if not isinstance(data, dict):
            raise Exception("data must be of type dict")

        # if key is specified, it must not already be in nodes
        if key is not None and key in self.nodes:
            raise Exception(f"key {key} already exists in nodes")

        # generate random uuid
        uuid = uuid4().hex

        # if the random uuid isn't so random (rare), try again until it is
        if uuid in self.nodes:
            while 1:
                uuid = uuid4().hex
                if uuid not in self.nodes:
                    break

        # create the node
        node = Node(uuid, data, self.file)

        # insert the node into nodes
        if key is None:
            self.nodes[uuid] = node
        else:
            self.nodes[key] = node

        # return the node
        return node
