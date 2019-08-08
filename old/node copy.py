from queue import SimpleQueue


class Node(object):
    def __init__(self, uuid, data):
        """
        Initialize a node object with an uuid and data.

        Args:
            uuid (str): The uuid of the node to be created.
            data (dict): The data to be assigned to the node

        Returns:
            (Node): The initialized Node object.
        """
        self.id = uuid
        self.data = data
        self.neighbors = {}

    def add_neighbor(self, vertex, weight):
        """
        Add a neighboring vertex to the dict of neighbors for this vertex.

        Args:
            vertex (Vertex): The vertex object to add as a neighbor.
            weight (any): The weight to be assigned to the edge created
            by this association.
        """
        if vertex not in self.neighbors:
            self.neighbors[vertex] = weight

    def __str__(self):
        """
        Return a formatted string representation of this vertex.

        Returns:
            (string): The formatted string representation of this vertex.
        """
        return f'{self.id} adjacent to {[x.id for x in self.neighbors]}'

    def to_dict(self):
        return {"id": self.id, "data": self.data, "neighbors": self.neighbors}

    def get_neighbors(self, as_string=False):
        """
        Return the neighbors of this vertex.

        Args:
            as_string (bool): if True, returns iterable of ids instead of
            vertex objects

        Returns:
            (iter): An iterator over the neighbors of this vertex.
        """
        if as_string:
            iter(i.id for i in self.neighbors.keys())
        return iter(self.neighbors.keys())

    def get_edge_weight(self, vertex):
        """
        Return the weight of the edge formed from this vertex to a given
        neighbor vertex.

        Args:
            vertex (Vertex): The neighboring vertex to draw the edge to.
        """
        return self.neighbors[vertex]

    def associated_by(self, label):
        """
        Return the list of vertices associated to this vertex by label
        directly.
        """
        return [
            vtx for vtx, weight in self.neighbors.items() if weight == label
        ]

    def associations_with(self, label):
        """
        Find nodes that are connected directly or indirectly with a
        specific label. Result will be a dictionary with the key as
        how many levels deep and the value a list of vertices at that
        level that match the label.
        """

        # create needed structures
        result = {}
        visited = set([self])
        queue = SimpleQueue()
        level = 1

        # initialize queue with self
        queue.put(self)

        # while there are vertices in the queue
        while queue.qsize() > 0:
            # dequeue a vertex
            vtx = queue.get()
            # if the vertex has not been visited
            if vtx not in visited:
                # add it to visited set
                visited.add(vtx)
                # iterate through its neighbors
                for neighbor in vtx.get_neighbors():
                    # put the neighbor in the queue
                    queue.put(neighbor)
                    # if the weight of the edge from vtx to neighbor
                    # matches label, add to result
                    if vtx.get_edge_weight(neighbor) == label:
                        if level in result:
                            result[level].append(neighbor)
                        else:
                            result[level] = [neighbor]
                # increment level
                level += 1

        # return result
        return result

    # def depth_to(self, vtx):
    #     """
    #     Find the level of relation from this vertex to another.
    #     """

    #     # create needed structures
    #     result = {}
    #     visited = set([self])
    #     stack = [self]
    #     level = 1

    #     # while there are vertices in the stack
    #     while stack:
    #         # dequeue a vertex
    #         vtx = stack.pop()
    #         # if the vertex has not been visited
    #         if vtx not in visited:
    #             # add it to visited set
    #             visited.add(vtx)
    #             # iterate through its neighbors
    #             for neighbor in vtx.get_neighbors():
    #                 # put the neighbor in the queue
    #                 queue.put(neighbor)
    #                 # if the weight of the edge from vtx to neighbor
    #                 # matches label, add to result
    #                 if vtx.get_edge_weight(neighbor) == label:
    #                     if level in result:
    #                         result[level].append(neighbor)
    #                     else:
    #                         result[level] = [neighbor]
    #             # increment level
    #             level += 1

    #     # return result
    #     return result
