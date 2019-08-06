from vertex import Vertex
import random
from queue import SimpleQueue, PriorityQueue
from collections import defaultdict
from uuid import uuid4


class Graph(object):
    """
    A graph object representation.
    """

    def __init__(self):
        """
        Initialize a graph object.

        Returns:
            (Graph): The initialized graph object.
        """
        self.vertices = {}
        self.num_vertices = 0
        self.num_edges = 0

    @property
    def num_associations(self):
        return self.num_edges

    @property
    def num_nodes(self):
        return self.num_vertices

    def add_vertex(self, data):
        """
        Add a vertex to the graph by id and return the created vertex object.

        Args:
            id (any): The id of the vertex to create.

        Returns:
            (Vertex): The vertex created.
        """
        id = uuid4().hex
        if id not in self.vertices:
            self.num_vertices += 1
            self.vertices[id] = Vertex(id, data)
        else:
            raise Exception(
                "fatal error: duplicate random hex generated for vertex uuid"
            )
        return self.vertices[id]

    def get_vertex_by_id(self, id):
        """
        Return a vertex by id.

        Args:
            id (any): The id of the vertex to return.

        Returns:
            (Vertex|None): The vertex by id or None if not exists.
        """
        return None if id not in self.vertices else self.vertices[id]

    def add_edge(self, vtx_A, vtx_B, weight=1):
        """
        Add an edge from a start vertex to an end vertex.

        Args:
            vtx_A (any): The start vertex in the edge.
            vtx_B (any): The end vertex in the edge.
            weight (any): The weight to be assigned to the edge.
        """
        if (
            self.get_vertex_by_id(vtx_A) is None
            or self.get_vertex_by_id(vtx_B) is None
        ):
            raise Exception(
                "unable to create edge, one or more vertices are missing\
                    from the list of vertices"
            )
        self.num_edges += 1
        self.vertices[vtx_A].add_neighbor(self.vertices[vtx_B], weight)

    def get_vertices(self):
        """
        Return a list of vertices.

        Returns:
            ([string]): An list of vertices keys.
        """

        return self.vertices.keys()

    def __iter__(self):
        """
        Return an iterator to iterate over vertex values.

        Returns:
            (iterable): An iterator over vertices values.
        """
        return iter(self.vertices.values())

    def get_edges(self, weighted=False):
        """
        Return a list of edges in the graph.

        Args:
            weighted (bool): if True, resulting list will also contain the
            edge weights
        """
        result = []
        for v in self.vertices.values():
            for w in v.neighbors:
                if weighted:
                    result.append(
                        (v.get_id(), w.get_id(), v.get_edge_weight(w))
                    )
                else:
                    result.append((v.get_id(), w.get_id()))
        return result

    def breadth_first_search(self, start_vertex, num_traversals):
        """
        Perform bfs on the graph.

        Args:
            start_vtx (any): The vertex data to start the search from.
            num_traversals (int): The number of bfs traversals to make.

        Returns:
            result ([any]): List of vertex ids in order of traversal.

        Raises:
            Exception: If start_vertex not in graph.
        """

        # if the start vertex is not in graph, raise exception
        if start_vertex not in self.vertices:
            raise Exception(f"Vertex {start_vertex} not in graph.")

        # create needed structures
        result = []
        visited = set()
        queue = SimpleQueue()

        # initialize queue with start vertex
        queue.put(self.vertices[start_vertex])

        # while there are vertices in the queue
        while queue.qsize() > 0 or len(result) < num_traversals:
            # dequeue a vertex
            curVtx = queue.get()
            # if the vertex has not been visited
            if curVtx not in visited:
                # add it to visited set and result list
                visited.add(curVtx)
                result.append(curVtx.id)
                # iterate through its neighbors
                for neighbor in curVtx.get_neighbors():
                    # put the neighbor in the queue
                    queue.put(neighbor)

        # return result list of vertex ids
        return result

    def find_shortest_path(self, vtx_A, vtx_B):
        """
        Use bfs to find the shortest path from a start vertex
        to an end vertex.

        Args:
            vtx_A (any): The start vertex.
            vtx_B (any): The end vertex.

        Returns:
            result ([any]): List of vertex ids in order of traversal.

        Raises:
            Exception: If vtx_A or vtx_B not in graph.
        """

        # ensure that vtxA and vtxB are in graph
        if vtx_A not in self.vertices or vtx_B not in self.vertices:
            raise Exception(
                f"One or both of the supplied vertices {vtx_A}, {vtx_B} \
                is not in this graph."
            )

        # create our needed structures
        result = []
        visited = set()
        queue = SimpleQueue()

        # initialize queue with start vertex
        queue.put(self.vertices[vtx_A])

        # while there are vertices in the queue
        while queue.qsize() > 0:
            # dequeue a vertex
            curVtx = queue.get()
            # if the vertex has not been visited
            if curVtx not in visited:
                # add it to visited set and result list
                visited.add(curVtx)
                result.append(curVtx.id)
                # iterate through its neighbors
                for neighbor in curVtx.get_neighbors():
                    # if the neighbor is the vertex we are looking for, we are
                    # done append the neighbor to the result and return
                    if neighbor.id == vtx_B:
                        result.append(neighbor.id)
                        return result
                    # otherwise, put the neighbor in the queue
                    queue.put(neighbor)

        # return result list of vertex ids
        return result

    def clique(self):
        """
        Find a clique in the graph.

        Returns:
            clique ({any}): A set of vertex ids in the clique.
        """

        # create needed structures and variables
        rand_key = random.choice(self.vertices.keys())
        clique = set(rand_key)
        vertices = [(k, v) for k, v in self.vertices.items() if k != rand_key]

        # iterate over remaining vertices
        for id, vtx in vertices:
            for neighbor in vtx.get_neighbors(as_string=True):
                if neighbor in clique:
                    clique.add(id)

        # return clique
        return clique

    def prims(self):
        start_vtx = random.choice(list(self.vertices.keys()))
        mst = defaultdict(set)
        visited = set([start_vtx])
        pq = PriorityQueue()

        # initialize pq
        for neighbor, weight in self.vertices[start_vtx].neighbors.items():
            pq.put((weight, start_vtx, neighbor.id))

        while pq.qsize() > 0:
            _, vtx_A, vtx_B = pq.get()
            if vtx_B not in visited:
                visited.add(vtx_B)
                mst[vtx_A].add(vtx_B)
                for neighbor, weight in self.vertices[vtx_B].neighbors.items():
                    if neighbor.id not in visited:
                        pq.put((weight, vtx_B, neighbor.id))
        return mst

    def dijkstra(self, start_vtx):
        distances = {v: float('inf') for v in self.vertices}
        distances[start_vtx] = 0
        pq = PriorityQueue()
        pq.put((0, start_vtx))

        while pq.qsize() > 0:
            cur_dist, cur_vtx = pq.get()

            if cur_dist > distances[cur_vtx]:
                continue

            for neighbor, weight in self.vertices[cur_vtx].neighbors.items():
                dist = cur_dist + weight

                if dist < distances[neighbor.id]:
                    distances[neighbor.id] = dist
                    pq.put((dist, neighbor.id))

        return distances
