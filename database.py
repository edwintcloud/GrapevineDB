from collection import Collection
from uuid import uuid4
from node import Node
from queue import SimpleQueue


class Database:
    """
    Database represents the in-memory database object that will store
    references to all data contained in the Database itself.
    """

    def __init__(self):
        """
        Initialize a Database object.

        Returns:
            (Database): The initialized Database object.
        """
        self.nodes = {}
        self.collections = {}

    def __str__(self):
        """
        Return the str representation of this Database.

        Returns:
            (str): The str representation of this Database.
        """
        collections = [
            f"\n\t{k}: {{\n\t\t{str(v)}\n\t}}"
            for k, v in self.collections.items()
        ]
        nodes = [
            f"\n\t{k}: {{\n\t\t{str(v)}\n\t}}" for k, v in self.nodes.items()
        ]
        return "{{\ncollections: {{\n{}\n}}, \nnodes: {{\n{}\n}}\n}}".format(
            ",".join(collections), ",".join(nodes)
        )

    @property
    def num_nodes(self):
        """
        Return the number of nodes in this Database.

        Returns:
            (int): The number of nodes in this Database.
        """
        return len(self.nodes) + sum(
            len(c.nodes) for c in self.collections.values()
        )

    @property
    def num_associations(self):
        """
        Return the number of associations in this Database.

        Returns:
            (int): The number of associations in this Database.
        """
        return sum(len(i) for i in self.associations.values())

    @property
    def associations(self):
        """
        Return the associations in this Database.

        Returns:
            (dict): The associations in this Database organized by label as
            the key and a list of edges (tuple of nodes) as the value.
        """

        # create needed data structures
        result = {}
        queue = SimpleQueue()
        visited = set()

        # for each collection
        for collection in self.collections.values():
            # add nodes in collection to queue
            for node in collection.nodes.values():
                queue.put(node)
            # while there are nodes in the queue
            while queue.qsize() > 0:
                # dequeue a node
                node = queue.get()
                # if the node has not been visited
                if node not in visited:
                    # mark it as visited
                    visited.add(node)
                    # iterate over its relations
                    for relation, label in node.relations.items():
                        # add the relation to the queue
                        queue.put(relation)
                        # add the label to result
                        if label in result:
                            result[label].append((node, relation))
                        else:
                            result[label] = [(node, relation)]

        # return the resulting dict or relations
        return result

    def add(self, collection_name):
        """
        Add a Collection to this Database by name.

        Args:
            collection_name (str): The name of the Collection to be created and
            added to this Database.
    
        Returns:
            (Collection): The newly created Collection.
        
        Raises:
            Exception: If collection_name is less than 3 character in length.
            Exception: If collection_name is not of type str.
            Exception: If collection_name already exists in self.collections.
        """

        # collection name must be at least 3 characters
        if len(collection_name) < 3:
            raise Exception(
                "collection name must be at least 3 characters in length"
            )

        # collection must be a string
        if not isinstance(collection_name, str):
            raise Exception("collection name must be of type str")

        # collection must not already exist
        if collection_name in self.collections:
            raise Exception("collection already exists in database")

        # create the collection
        self.collections[collection_name] = Collection()

        # return the collection
        return self.collections[collection_name]

    def insert(self, data):
        """
        Insert a Node into this Database.

        Args:
            data (dict): The data to be added to the new Node that will
            be created and added to this Database.

        Returns:
            (Node): The newly created Node object.

        Raises:
            Exception: If data is not of type dict.
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

        # insert the node into nodes
        self.nodes[uuid] = Node(uuid, data)

        # return the node
        return self.nodes[uuid]

    def remove(self, name, type=None):
        """
        Remove a Collection or Node from this Database.

        Args:
            name (str): The name of the Collection or Node to be removed
            from this Database.
            type (str|None): Used to designate whether to remove a 'node', 
            'collection', or None which will remove both by name if they
            exist.

        Raises:
            Exception: If name is not a Node or Collection in this Database.
        """

        # name must exist in db
        if name not in self.nodes or name not in self.collections:
            raise Exception(
                f"name {name} not a node or collection in this database"
            )

        # remove from database
        if type is None:
            if name in self.collections:
                del self.collections[name]
            if name in self.nodes:
                del self.nodes[name]
        elif type == "collection" and name in self.collections:
            del self.collections[name]
        elif type == "node" and name in self.nodes:
            del self.nodes[name]

    def wipe(self):
        """
        Delete all Collection(s) and Node(s) in this Database.
        """
        for collection_name in self.collections:
            self.remove(collection_name)
        for node_name in self.nodes:
            self.remove(node_name)
