from pickle import load, dump
from pathlib import Path
from datetime import datetime
from functools import wraps
from graph import Graph


class Database:
    def __init__(self, db_file="data/db.p"):
        self.db_path = Path(db_file)
        self.db = {}
        try:
            # if database file exists, load it into memory
            if self.db_path.exists():
                self.db = load(self.db_path.open(mode="rb"))
                print(f"{self._current_dt}: Database loaded from file!")
            # otherwise, create the db file
            else:
                self.db_path.parent.mkdir()
                self.db_path.touch()
                dump(self.db, self.db_path.open(mode="wb"))
                print(f"{self._current_dt}: Database created!")
        except Exception as e:
            print(e)

    def __str__(self):
        return str(self.db)

    def __iter__(self):
        return iter(self.db.items())

    @property
    def collections(self):
        return list(self.db.keys())

    @property
    def _current_dt(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # pylint: disable=no-self-argument,not-callable,no-member
    def _save_on_update(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            # after function call, save db to file
            dump(self.db, self.db_path.open(mode="wb"))
            print(
                "{}: {} caused database to be saved to disk.".format(
                    self._current_dt, f.__name__
                )
            )
            return result

        return wrapper

    @_save_on_update
    def add_collection(self, collection_name):

        # collection name must be at least 3 characters
        if len(collection_name) < 3:
            raise Exception(
                "collection name must be at least 3 characters in length"
            )

        # collection must not already exist
        if collection_name in self.db:
            raise Exception("collection already exists in database")

        # create the collection
        self.db[collection_name] = Graph()

    @_save_on_update
    def remove_collection(self, collection_name):

        # collection must exist in db
        if collection_name not in self.db:
            raise Exception(
                "collection {} not found in database".format(collection_name)
            )

        # remove the collection
        del self.db[collection_name]

    @_save_on_update
    def insert(self, collection_name, data):

        # collection must exist in db
        if collection_name not in self.db:
            raise Exception(
                "collection {} not found in database".format(collection_name)
            )

        # add vertex to graph
        try:
            result = self.db[collection_name].add_vertex(data)
            print(
                "{}: Entry inserted into collection {} with id {}".format(
                    self._current_dt, collection_name, result.id
                )
            )
            return result.to_dict()
        except Exception as e:
            raise e

    def get(self, collection_name, query=None):

        # collection must exist in db
        if collection_name not in self.db:
            raise Exception(
                "collection {} not found in database".format(collection_name)
            )

        try:
            # if query is string, find by id
            if isinstance(query, str):
                return (
                    self.db[collection_name].get_vertex_by_id(query).to_dict()
                )
            # if query is None, return all vertices in collection as a list
            if query is None:
                return [
                    vertex.to_dict()
                    for vertex in self.db[collection_name].vertices.values()
                ]

        except Exception as e:
            raise e

    @_save_on_update
    def associate(self, collection_name, id_1, id_2, label):
        """
        Add an edge associating one vertex to another. Label will be saved as
        the weight of the edge.
        """

        # collection must exist in db
        if collection_name not in self.db:
            raise Exception(
                "collection {} not found in database".format(collection_name)
            )

        # label must be at least 3 characters
        if len(label) < 3:
            raise Exception("label must be at least 3 characters in length")

        try:
            # create edge from id_1 to id_2 (order matters)
            self.db[collection_name].add_edge(id_1, id_2, label)
            print(
                """{}: The association with label {} has been created from {} 
                     to {} in collection {}""".format(
                    self._current_dt, label, id_1, id_2, collection_name
                )
            )
        except Exception as e:
            raise e
