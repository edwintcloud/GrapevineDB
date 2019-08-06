class Vertex(object):
    """
    A vertex object representation.
    """

    def __init__(self, id):
        """
        Initialize a vertex object with an id.

        Args:
            id (any): The id of the vertex to be created.

        Returns:
            (Vertex): The initialized vertex object.
        """
        self.id = id
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

    def get_id(self):
        """
        Return the id of this vertex.

        Returns:
            (any): The id of this vertex.
        """
        return self.id

    def get_edge_weight(self, vertex):
        """
        Return the weight of the edge formed from this vertex to a given
        neighbor vertex.

        Args:
            vertex (Vertex): The neighboring vertex to draw the edge to.
        """
        return self.neighbors[vertex]
